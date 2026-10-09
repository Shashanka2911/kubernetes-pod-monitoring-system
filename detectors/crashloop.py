
def detect_crashloop(pod):
    """Detect a container in CrashLoopBackOff."""

    if not pod.status.container_statuses:
        return None

    for container in pod.status.container_statuses:
        state = container.state

        if state and state.waiting:
            if state.waiting.reason == "CrashLoopBackOff":
                return {
                    "pod": pod.metadata.name,
                    "issue": "CrashLoopBackOff"
                }

    return None