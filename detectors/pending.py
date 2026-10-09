
def detect_pending(pod):
    """Detect a Pod in Pending phase."""

    if pod.status.phase == "Pending":
        return {
            "pod": pod.metadata.name,
            "issue": "Pending"
        }

    return None