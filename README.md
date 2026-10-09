# Kubernetes Pod Monitoring and Alert System

A Python-based Kubernetes monitoring project that detects five common Pod issues and sends alerts through the console and email. The project uses the Kubernetes Python client to inspect Pod status and help identify failures in a local Kubernetes cluster.

## Project Overview

Kubernetes applications can experience failures due to application crashes, scheduling problems, invalid container images, memory limits, and readiness probe failures.

This project automates the detection of five common Kubernetes Pod issues and provides notifications to help developers troubleshoot problems.

## Key Features

* Detects CrashLoopBackOff errors.
* Detects Pods stuck in the Pending state.
* Detects ImagePullBackOff and ErrImagePull errors.
* Detects containers terminated due to OOMKilled.
* Detects Pods that are not Ready.
* Displays alerts in the terminal.
* Supports email notifications through SMTP.
* Connects to Kubernetes using the Python client.

## Kubernetes Issues Detected

| Issue            | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| CrashLoopBackOff | A container repeatedly crashes and Kubernetes retries it.           |
| Pending          | A Pod cannot be scheduled or has not progressed to running.         |
| ImagePullBackOff | Kubernetes cannot pull the required container image.                |
| OOMKilled        | A container was terminated after exceeding its memory allowance.    |
| Not Ready        | A Pod fails its readiness checks and is not ready to serve traffic. |

## Technology Stack

* **Programming Language:** Python
* **Container Orchestration:** Kubernetes
* **Local Kubernetes Environment:** Minikube
* **Container Runtime:** Docker
* **Kubernetes API:** Kubernetes Python Client
* **Notifications:** Console alerts and SMTP email
* **Development Environment:** Windows PowerShell

## Project Structure

```text
K8 Monitoring System/
├── main.py
├── kubernetes_client.py
├── requirements.txt
├── test_email.py
├── detectors/
│   ├── __init__.py
│   ├── crashloop.py
│   ├── pending.py
│   ├── image_pull.py
│   ├── oom.py
│   └── readiness.py
├── notifications/
│   ├── __init__.py
│   ├── console.py
│   └── email.py
└── screenshots/
    ├── monitoring-output.png
    └── email-alert.png
```

## Prerequisites

Install the following tools before running the project:

* Python 3
* Docker Desktop
* Minikube
* kubectl
* Git

## Installation and Setup

### 1. Clone the repository

```powershell
git clone https://github.com/Shashanka2911/kubernetes-pod-monitoring-system.git
cd kubernetes-pod-monitoring-system
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start Minikube

```powershell
minikube start --driver=docker
kubectl config current-context
kubectl get nodes
```

Confirm that the current context is `minikube` and the node is Ready.

## Create Test Kubernetes Issues

Run the following commands in PowerShell to create test Pods in your development cluster.

### 1. CrashLoopBackOff

```powershell
kubectl run crashloop-test --image=busybox:1.36 --restart=Never -- /bin/sh -c "exit 1"
```

### 2. Pending Pod

```powershell
kubectl run pending-test --image=busybox:1.36 --requests=cpu=100 --command -- sleep 3600
```

The CPU request is deliberately very high and should leave the Pod unschedulable on a typical local Minikube node.

### 3. ImagePullBackOff

```powershell
kubectl run imagepull-test --image=invalid-image-name-xyz:latest
```

This uses a deliberately invalid image name to exercise image-pull error detection.

### 4. OOMKilled

```powershell
kubectl run oom-test --image=busybox:1.36 --restart=Never --limits=memory=10Mi -- /bin/sh -c 'x=; while true; do x=${x}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx; done'
```

**Warning:** This test intentionally consumes memory. Run it only in your development cluster and delete the Pod afterward.

### 5. Not Ready

First create the Pod:

```powershell
kubectl run notready-test --image=busybox:1.36 --restart=Never --command -- /bin/sh -c "sleep 3600"
```

Then configure a readiness probe that fails:

```powershell
kubectl patch pod notready-test --type=strategic -p '{"spec":{"containers":[{"name":"notready-test","readinessProbe":{"exec":{"command":["/bin/sh","-c","exit 1"]},"initialDelaySeconds":2,"periodSeconds":3}}]}}'
```

## Run the Monitoring System

### 1. Check Pod status

```powershell
kubectl get pods
kubectl get pods -o wide
```

### 2. Run the Python monitoring script

```powershell
python main.py
```

The script scans the configured namespace and reports issues detected by the implemented detector functions. The current implementation performs a single scan each time it is run.

### 3. Test email notifications

Configure these environment variables in PowerShell using your own credentials:

```powershell
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USERNAME = "your-email@gmail.com"
$env:SMTP_PASSWORD = "your-google-app-password"
$env:ALERT_EMAIL = "recipient@example.com"
```

Use a Google App Password when required by your Gmail configuration. Never commit real passwords or credentials to GitHub.

Run the email test:

```powershell
python test_email.py
```

Email delivery requires valid SMTP credentials and working network access.

## Verify and Clean Up Test Pods

View Pod states:

```powershell
kubectl get pods
kubectl describe pods
```

After testing, delete the test Pods:

```powershell
kubectl delete pod crashloop-test pending-test imagepull-test oom-test notready-test --ignore-not-found
```

## Project Output Screenshots

Add screenshots of your actual program output to the `screenshots/` folder.

### Kubernetes Monitoring Console Output

![Kubernetes Monitoring Console Output](screenshots/monitoring-output.png)

### Email Alert Notification

![Email Alert Notification](screenshots/email-alert.png)

Replace the example screenshot filenames with the actual names of your images if they differ.

## Future Improvements

* Continuous monitoring with a configurable polling interval.
* Support for monitoring multiple namespaces.
* Duplicate alert suppression.
* File-based logging and alert history.
* Prometheus and Grafana integration.
* Automated unit tests for all detector functions.

## Learning Outcomes

This project demonstrates practical experience with Python automation, Kubernetes Pod troubleshooting, container orchestration, API integration, and email notifications.

## Author

**Shashanka**

GitHub: [Shashanka2911](https://github.com/Shashanka2911)

Project Repository: [Kubernetes Pod Monitoring and Alert System](https://github.com/Shashanka2911/kubernetes-pod-monitoring-system)
