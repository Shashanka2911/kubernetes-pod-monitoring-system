from kubernetes import client, config


def get_kubernetes_client():
    config.load_kube_config() #Reads the standard Kubernetes configuration file from your local system (by default, ~/.kube/config).
    return client.CoreV1Api()
    return v1