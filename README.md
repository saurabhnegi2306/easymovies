# 🎬 EasyMovies

> End-to-end CI/CD pipeline using **Ansible**, **AWS EC2**, **Jenkins**, **Docker**, **Docker Compose**, **GitHub Webhooks**, and **Python**.

---

# 📑 Table of Contents

- Prerequisites
- Provision Infrastructure
- Access Jenkins
- Install Jenkins Plugins
- Configure Jenkins Worker
- Run Application Locally
- Run with Docker
- Run with Docker Compose
- Configure Jenkins Pipeline
- Configure GitHub Webhook
- Verify CI/CD Pipeline

---

# 🛠 Prerequisites

Install boto3:

```bash
/opt/miniconda3/bin/python -m pip install boto3 botocore
```

Configure AWS credentials:

```bash
aws configure
```

Verify credentials:

```bash
aws sts get-caller-identity
```

Install Ansible collections:

```bash
ansible-galaxy collection install -r requirements.yml
```

---

# 🚀 Step 1 - Provision Jenkins Infrastructure

Run:

```bash
ansible-playbook -i inventory.ini 1.provision.yml
```

This creates:

- Jenkins Controller
- Jenkins Worker
- Security Group allowing:
  - SSH (22)
  - Jenkins (8080)
  - NodePort Range (5000-32767)

It also updates:

- `inventory.ini`
- `vars.yml`

and generates:

- Jenkins admin password
- SSH key (`~/.ssh/jenkins-ci-generated-key`)

<img width="1107" height="185" alt="image" src="https://github.com/user-attachments/assets/136e3949-05bf-464d-8d00-54fd848c98e8" />

This step should auto update the inventory.ini file with new nodes IP details as well as vars.yml with new admin_password.

<img width="1108" height="124" alt="image" src="https://github.com/user-attachments/assets/4128127c-aaff-40c6-a245-44da00f14d9f" />

<img width="559" height="328" alt="image" src="https://github.com/user-attachments/assets/03b1829b-e460-4966-94ed-f14bb725e793" />

---

# 🔑 Access Jenkins

Login URL

```
http://<CONTROLLER-NODE-PUBLIC-IP>:8080
```

SSH:

```bash
ssh -i ~/.ssh/jenkins-ci-generated-key ubuntu@<CONTROLLER-NODE-PUBLIC-IP>
```

Worker:

```bash
ssh -i ~/.ssh/jenkins-ci-generated-key ubuntu@<WORKER-NODE-PUBLIC-IP>
```

Retrieve password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Check Jenkins:

```bash
sudo systemctl status jenkins
```

<img width="1107" height="424" alt="image" src="https://github.com/user-attachments/assets/62b8c1ed-0ba8-4c3d-b63e-d6ea8323c6e9" />

Install Suggested Plugins.

<img width="1107" height="570" alt="image" src="https://github.com/user-attachments/assets/a18c8d4e-c740-4969-99d6-9a085aae0db7" />

Create a user or continue with admin.

<img width="1107" height="916" alt="image" src="https://github.com/user-attachments/assets/0656bacd-4b96-4127-9f0f-e01c8b07aebc" />

<img width="1107" height="407" alt="image" src="https://github.com/user-attachments/assets/c4f06743-16fd-4b72-9875-89e22b184096" />

---

# 🔌 Step 2 - Install Jenkins Plugins

```bash
ansible-playbook -i inventory.ini 2.install_plugins.yml
```

Plugins installed:

- workflow-aggregator
- workflow-multibranch
- git
- github
- github-branch-source
- ssh-slaves
- docker-workflow
- credentials-binding
- ws-cleanup
- junit

---

# 👷 Step 3 - Configure Jenkins Worker

```bash
ansible-playbook -i inventory.ini 3.configure_worker.yml
```

<img width="1107" height="496" alt="image" src="https://github.com/user-attachments/assets/42fb64eb-2796-41bd-b2a8-6558d2077867" />

Verify under **Manage Jenkins → Nodes**.

<img width="1107" height="217" alt="image" src="https://github.com/user-attachments/assets/08a2bf60-7a40-4edb-9a55-bdc3d3ab4316" />

---

# 🖥 Run Application Locally

```bash
pip install -r requirements.txt
python app.py
```

Browse:

```
http://<LAB-VM-PUBLIC-IP>:8081
```

<img width="1107" height="497" alt="image" src="https://github.com/user-attachments/assets/bd6c644e-48fc-404e-88de-9f88cef1568c" />

<img width="1107" height="431" alt="image" src="https://github.com/user-attachments/assets/d47d888a-c4fb-4705-8267-a32901277eeb" />

<img width="784" height="408" alt="image" src="https://github.com/user-attachments/assets/6e1808e6-a30c-4300-a1fa-50261764f71d" />

Stop using CTRL+C.

---

# 🐳 Docker Deployment

Build:

```bash
docker build -t easymovies:v1 .
```

<img width="1107" height="384" alt="image" src="https://github.com/user-attachments/assets/2abc0ab4-d735-4815-8f61-fea398367a29" />

Run:

```bash
docker run -d --name easymovies -p 8081:8081 easymovies:v1
```

<img width="784" height="408" alt="image" src="https://github.com/user-attachments/assets/de8a6064-8d30-4311-b359-a318408aa38e" />

Remove:

```bash
docker stop easymovies && docker rm easymovies
```

or

```bash
docker rm -f easymovies
```

---

# 🐳 Docker Compose

```bash
docker compose up -d
```

<img width="1107" height="99" alt="image" src="https://github.com/user-attachments/assets/70a3fcb2-a5f7-419b-9a8c-cf38da02509b" />

<img width="1107" height="99" alt="image" src="https://github.com/user-attachments/assets/b390a90a-eb16-49d7-b6dc-2cdec9228559" />

---

# ⚙ Jenkins Pipeline

Create a new **Pipeline**.

<img width="1107" height="270" alt="image" src="https://github.com/user-attachments/assets/eec92272-3271-4f34-9fcc-124e7f76c197" />

Enable GitHub Project.

<img width="1107" height="642" alt="image" src="https://github.com/user-attachments/assets/ba20b7ee-f6be-4636-a2fb-f33316698843" />

Enable **GitHub hook trigger for GITScm Polling**.

<img width="1107" height="146" alt="image" src="https://github.com/user-attachments/assets/6d62b327-c956-40dc-8ac3-84f52b9a402c" />

Configure SCM.

<img width="1107" height="741" alt="image" src="https://github.com/user-attachments/assets/83fd3cb3-55cf-47ea-a294-56c1f82d017d" />

---

# 🔗 GitHub Webhook

GitHub → Settings → Webhooks → Add Webhook

<img width="1107" height="198" alt="image" src="https://github.com/user-attachments/assets/44ebf94a-8d38-4472-a7fb-c1f5078d34e9" />

Payload:

```
http://<JENKINS-CONTROLLER-NODE-PUBLIC-IP>:8080/github-webhook/
```

<img width="1107" height="892" alt="image" src="https://github.com/user-attachments/assets/64faf8b3-e34b-45f6-ba7b-ea6b35a00164" />

---

# ✅ Verify CI/CD

Make a dummy change in README.md, Dockerfile or application code and push to GitHub.

Jenkins should automatically trigger.

<img width="564" height="1020" alt="image" src="https://github.com/user-attachments/assets/85d2e8e4-80be-4a1c-9e7c-799435947ece" />

Pipeline Flow:

```text
GitHub Push
      ↓
Webhook
      ↓
Jenkins Pipeline
      ↓
Checkout
      ↓
Docker Build
      ↓
Pytest
      ↓
Deploy to Worker
      ↓
Application
```

Application:

```
http://<JENKINS-WORKER-NODE-PUBLIC-IP>:8081
```

<img width="1107" height="361" alt="image" src="https://github.com/user-attachments/assets/d64f1cdd-f647-4fda-a570-4af0da69d809" />

---

# 🎉 CI/CD Completed

Whenever code is pushed to GitHub:

- GitHub triggers Jenkins
- Jenkins pulls latest code
- Builds Docker image
- Runs Pytest
- Deploys to Worker Node
- Application is automatically updated

