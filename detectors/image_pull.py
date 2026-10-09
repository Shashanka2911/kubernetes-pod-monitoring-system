
def detect_image_pull(pod):
    """Detect a container image-pull failure."""

    if not pod.status.container_statuses:
        return None

    for container in pod.status.container_statuses:
        state = container.state

        if state and state.waiting:
            reason = state.waiting.reason

            if reason in ("ImagePullBackOff", "ErrImagePull"):
                return {
                    "pod": pod.metadata.name,
                    "issue": reason
                }

    return None