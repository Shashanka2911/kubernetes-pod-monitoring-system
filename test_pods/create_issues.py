
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

# Connect to Kubernetes
config.load_kube_config()
v1 = client.CoreV1Api()

NAMESPACE = "default"


def create_pod(pod):
    """Create a test Pod, without duplicating existing Pods."""
    try:
        v1.create_namespaced_pod(
            namespace=NAMESPACE,
            body=pod
        )
        print(f"CREATED: {pod.metadata.name}")

    except ApiException as e:
        if e.status == 409:
            print(f"ALREADY EXISTS: {pod.metadata.name}")
        else:
            print(f"ERROR creating {pod.metadata.name}: {e.reason}")


# 1. Normal Pod
normal_pod = client.V1Pod(
    metadata=client.V1ObjectMeta(name="normal-test-pod"),
    spec=client.V1PodSpec(
        containers=[
            client.V1Container(
                name="nginx",
                image="nginx:latest"
            )
        ]
    )
)
create_pod(normal_pod)


# 2. CrashLoopBackOff test
crash_pod = client.V1Pod(
    metadata=client.V1ObjectMeta(name="crashloop-pod"),
    spec=client.V1PodSpec(
        containers=[
            client.V1Container(
                name="crash-container",
                image="busybox:1.36",
                command=["sh", "-c", "exit 1"]
            )
        ],
        restart_policy="Always"
    )
)
create_pod(crash_pod)


# 3. ImagePullBackOff test
image_pod = client.V1Pod(
    metadata=client.V1ObjectMeta(name="imagepull-pod"),
    spec=client.V1PodSpec(
        containers=[
            client.V1Container(
                name="image-container",
                image="this-image-does-not-exist-123456:v999"
            )
        ]
    )
)
create_pod(image_pod)


# 4. Pending test: deliberately impossible memory request
pending_pod = client.V1Pod(
    metadata=client.V1ObjectMeta(name="pending-pod"),
    spec=client.V1PodSpec(
        containers=[
            client.V1Container(
                name="pending-container",
                image="nginx:latest",
                resources=client.V1ResourceRequirements(
                    requests={"memory": "1000Gi"}
                )
            )
        ]
    )
)
create_pod(pending_pod)


# 5. OOMKilled test: deliberately low memory limit
oom_pod = client.V1Pod(
    metadata=client.V1ObjectMeta(name="oom-pod"),
    spec=client.V1PodSpec(
        containers=[
            client.V1Container(
                name="oom-container",
                image="python:3.11-slim",
                command=[
                    "python", "-c",
                    "a=[]\nwhile True:\n a.append('x'*1024*1024)"
                ],
                resources=client.V1ResourceRequirements(
                    requests={"memory": "16Mi"},
                    limits={"memory": "32Mi"}
                )
            )
        ],
        restart_policy="Never"
    )
)
create_pod(oom_pod)

print("\nFinished submitting the five test Pods.")

"""
yaml:file for creating issues 
apiVersion: v1
kind: Pod
metadata:
  name: normal-test-pod
  namespace: default
spec:
  containers:
  - name: nginx
    image: nginx:latest

    """