
from kubernetes_client import get_kubernetes_client

from detectors.crashloop import detect_crashloop
from detectors.pending import detect_pending
from detectors.image_pull import detect_image_pull
from detectors.oom import detect_oom
from detectors.readiness import detect_not_ready

from notifications.console import send_console_notification
from notifications.email import send_email_notification


# All five Kubernetes Pod detectors
DETECTORS = [
    detect_crashloop,
    detect_pending,
    detect_image_pull,
    detect_oom,
    detect_not_ready,
]

NAMESPACE = "default"


def main():
    print("=" * 50)
    print("       KUBERNETES MONITORING SYSTEM")
    print("=" * 50)

    # Connect to Kubernetes
    try:
        v1 = get_kubernetes_client()
        print("Connected to Kubernetes API")

    except Exception as error:
        print(f"Monitoring failed: {error}")
        return

    # Retrieve Pods
    try:
        pods = v1.list_namespaced_pod(
            namespace=NAMESPACE
        )
        print(f"Pods found: {len(pods.items)}")

    except Exception as error:
        print(f"Failed to retrieve Pods: {error}")
        return

    alerts_found = 0

    # Run each detector against each Pod
    for pod in pods.items:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace or NAMESPACE

        for detector in DETECTORS:
            try:
                result = detector(pod)

                if not result:
                    continue

                alerts_found += 1

                issue = result["issue"]

                print(
                    f"\nALERT: {pod_name} -> {issue}"
                )

                # Send console notification
                send_console_notification(
                    pod_name,
                    issue,
                    namespace
                )

                # Send email notification
                send_email_notification(
                    pod_name,
                    issue,
                    namespace
                )

            except Exception as error:
                print(
                    f"Detector {detector.__name__} failed "
                    f"for Pod {pod_name}: {error}"
                )

    print("\n" + "=" * 50)
    print("MONITORING SCAN COMPLETE")
    print(f"Total alerts detected: {alerts_found}")
    print("=" * 50)


if __name__ == "__main__":
    main()