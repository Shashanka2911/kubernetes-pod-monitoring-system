
def detect_not_ready(pod):
    """Detect a Pod whose Ready condition is False."""

    conditions = pod.status.conditions or []

    for condition in conditions:
        if condition.type == "Ready" and condition.status != "True":
            return {
                "pod": pod.metadata.name,
                "issue": "NotReady"
            }

    return None