
def detect_oom(pod):
    """Detect a container terminated due to memory exhaustion."""

    if not pod.status.container_statuses:
        return None

    for container in pod.status.container_statuses:
        states = [container.state, container.last_state]

        for state in states:
            if state and state.terminated:
                if state.terminated.reason == "OOMKilled":
                    return {
                        "pod": pod.metadata.name,
                        "issue": "OOMKilled"
                    }

    return None