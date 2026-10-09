\# Kubernetes Pod Monitoring and Alert System



A Python-based Kubernetes monitoring project that detects common Pod failures and sends alerts through the console and email. The system uses the Kubernetes Python client to inspect Pod status and identify issues that may require attention.



\## Project Overview



Kubernetes Pods can fail for several reasons, including application crashes, scheduling problems, incorrect container images, and memory limits. This project automates the detection of five common Kubernetes Pod issues and helps administrators identify problems quickly.



\## Key Features



\* Detects CrashLoopBackOff errors.

\* Detects Pods stuck in the Pending state.

\* Detects ImagePullBackOff and ErrImagePull errors.

\* Detects containers terminated due to out-of-memory (OOM) errors.

\* Detects Pods that are not ready.

\* Displays alerts in the terminal.

\* Sends email notifications for detected issues.

\* Uses Python and the Kubernetes API to inspect Pod status.



\## Kubernetes Issues Detected



| Issue            | Description                                                                          |

| ---------------- | ------------------------------------------------------------------------------------ |

| CrashLoopBackOff | A container repeatedly crashes and Kubernetes attempts to restart it.                |

| Pending          | A Pod cannot yet be scheduled or started successfully.                               |

| ImagePullBackOff | Kubernetes cannot pull the required container image.                                 |

| OOMKilled        | A container was terminated because it exceeded its memory limit or available memory. |

| Not Ready        | A Pod is running or exists but is not reporting readiness.                           |



\## Technology Stack



\* Python

\* Kubernetes

\* Kubernetes Python Client

\* Minikube

\* Docker

\* SMTP and Gmail for email alerts

\* PowerShell (Windows development environment)



\## Project Structure



```text

K8 Monitoring System/

├── main.py

├── kubernetes\_client.py

├── requirements.txt

├── test\_email.py

├── detectors/

│   ├── \_\_init\_\_.py

│   ├── crashloop.py

│   ├── pending.py

│   ├── image\_pull.py

│   ├── oom.py

│   └── readiness.py

└── notifications/

&#x20;   ├── \_\_init\_\_.py

&#x20;   ├── console.py

&#x20;   └── email.py

```



\## Prerequisites



Before running the project, install or configure:



\* Python 3

\* Docker Desktop

\* Minikube

\* kubectl

\* Git

\* A Kubernetes cluster accessible through your local kubeconfig



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/YOUR-USERNAME/kubernetes-pod-monitoring-system.git

cd kubernetes-pod-monitoring-system

```



Replace `YOUR-USERNAME` with your GitHub username.



\### 2. Create and activate a Python virtual environment



On Windows PowerShell:



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```powershell

pip install -r requirements.txt

```



\### 4. Start the local Kubernetes cluster



```powershell

minikube start --driver=docker

kubectl config current-context

kubectl get nodes

```



Ensure that the current context is `minikube` and the node is Ready.



\### 5. Configure email notifications



Set the following environment variables in PowerShell:



```powershell

$env:SMTP\_HOST = "smtp.gmail.com"

$env:SMTP\_PORT = "587"

$env:SMTP\_USERNAME = "your-email@gmail.com"

$env:SMTP\_PASSWORD = "your-google-app-password"

$env:ALERT\_EMAIL = "recipient@example.com"

```



Use a Google App Password if your Gmail account supports it. Replace the example values with your own credentials. Never commit passwords, App Passwords, or other secrets to GitHub.



These variables apply to the current PowerShell session. Set them again in a new session if needed.



\### 6. Run the monitoring script



```powershell

python main.py

```



The script connects to the configured Kubernetes cluster, scans Pods in the configured namespace, and reports detected issues. Email alerts depend on valid SMTP configuration.



\## Testing



Check the Kubernetes cluster and Pods:



```powershell

kubectl get nodes

kubectl get pods -A

```



To test detection logic, create test workloads that reproduce the relevant failure conditions in a local development cluster. Use caution when testing resource exhaustion or crash loops.



To test email notifications:



```powershell

python test\_email.py

```



\## Future Improvements



\* Continuous monitoring with a configurable polling interval.

\* Monitoring multiple namespaces.

\* Avoiding repeated notifications for the same issue.

\* Logging alerts to a file.

\* Adding Prometheus and Grafana integration.

\* Adding unit tests for all detector functions.

\* Supporting configurable alert thresholds.



\## Learning Outcomes



This project demonstrates practical experience with Python automation, Kubernetes Pod troubleshooting, container orchestration, API integration, and email-based alerting.





commands to Run this project:

Step 1: Start Kubernetes and check the cluster

cmd:cd "D:\\K8 Monitoring System"

.\\venv\\Scripts\\Activate.ps1

minikube start --driver=docker

kubectl get nodes



Step 2: Create the five Kubernetes test issues



1\. CrashLoopBackOff



kubectl run crashloop-test --image=busybox:1.36 --restart=Never -- /bin/sh -c "exit 1"



2\. Pending Pod



kubectl run pending-test --image=busybox:1.36 --requests=cpu=100 --command -- sleep 3600



3\. ImagePullBackOff



kubectl run imagepull-test --image=invalid-image-name-xyz:latest



4\. OOMKilled



kubectl run oom-test --image=busybox:1.36 --restart=Never --limits=memory=10Mi -- /bin/sh -c "x=; while true; do x=${x}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx; done"



5\. Not Ready



kubectl run notready-test --image=busybox:1.36 --restart=Never --command -- /bin/sh -c "sleep 3600"

kubectl patch pod notready-test -p '{"spec":{"containers":\[{"name":"notready-test","image":"busybox:1.36","command":\["/bin/sh","-c","sleep 3600"],"readinessProbe":{"exec":{"command":\["/bin/sh","-c","exit 1"]},"initialDelaySeconds":2,"periodSeconds":3}}]}}'



Step 3: Check the Pod statuses

kubectl get pods

kubectl get pods -o wide



Step 4: Run your Python monitoring project

python main.py



Output:







\## Author



\*\*Shashanka\*\*



GitHub: https://github.com/Shashanka2911/kubernetes-pod-monitoring-system

