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

# 🛠 Prerequisites ( To Be Run on Lab/local VM ) 

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

# 🚀 Step 1 - Provision Jenkins Infrastructure ( To Be Run on Lab/local VM ) 

Run:

```bash
ansible-playbook -i inventory.ini 1.provision.yml
```

This creates:

- Jenkins Controller Node
- Jenkins Worker Node
- Security Group allowing:
  - SSH (22)
  - Port Range (5000-32767) covering jenkisn port 8080 and all nodeports ( 30000 to 32767 ) 

It also updates:

- `inventory.ini`  with details of both nodes
- `vars.yml`      with jenkins_admin_password

and generates:

- Jenkins admin password
- SSH key (`~/.ssh/jenkins-ci-generated-key`)

<img width="1107" height="185" alt="image" src="https://github.com/user-attachments/assets/136e3949-05bf-464d-8d00-54fd848c98e8" />

This step should auto update the inventory.ini file with new nodes IP details as well as vars.yml with new admin_password.

<img width="1108" height="124" alt="image" src="https://github.com/user-attachments/assets/4128127c-aaff-40c6-a245-44da00f14d9f" />

<img width="559" height="328" alt="image" src="https://github.com/user-attachments/assets/03b1829b-e460-4966-94ed-f14bb725e793" />

---

# 🔑 Access Jenkins Nodes via CLI ( From Local Laptop Web Browser )

SSH to Jenkins Controller Node:

```bash
ssh -i ~/.ssh/jenkins-ci-generated-key ubuntu@<CONTROLLER-NODE-PUBLIC-IP>
sudo cat /var/lib/jenkins/secrets/initialAdminPassword      # To Retrieve Jenkins UI Admin password
systemctl status jenkins                                    # To check jenkins service status
exit
```

SSH to Jenkins Worker Node ( If Needed ) :

```bash
ssh -i ~/.ssh/jenkins-ci-generated-key ubuntu@<WORKER-NODE-PUBLIC-IP>
```

# 🔑 Access Jenkins UI Via Browser ( From Local Laptop Web Browser )

Login URL

```
http://<CONTROLLER-NODE-PUBLIC-IP>:8080
```
Enter Jenkins admin password ( get from previous step or fetch it from vars.yml ( which shoul dnow have updated password).

<img width="1107" height="424" alt="image" src="https://github.com/user-attachments/assets/62b8c1ed-0ba8-4c3d-b63e-d6ea8323c6e9" />

Install Suggested Plugins.

<img width="1107" height="570" alt="image" src="https://github.com/user-attachments/assets/a18c8d4e-c740-4969-99d6-9a085aae0db7" />

Create a user or continue with admin.

<img width="1107" height="916" alt="image" src="https://github.com/user-attachments/assets/0656bacd-4b96-4127-9f0f-e01c8b07aebc" />

<img width="1107" height="407" alt="image" src="https://github.com/user-attachments/assets/c4f06743-16fd-4b72-9875-89e22b184096" />
Jenkins Server is now up and running. 
---

# 🔌 Step 2 - Install Jenkins Plugins ( To Be Run on Lab/local VM )

```bash
ansible-playbook -i inventory.ini 2.install_plugins.yml
```

This playbook will install below Plugins. Jenkins has a lot of supported plugins specific to different tools and requirements.:

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

# 👷 Step 3 - Configure Jenkins Worker ( To Be Run on Lab/local VM )

```bash
ansible-playbook -i inventory.ini 3.configure_worker.yml
```

<img width="1107" height="496" alt="image" src="https://github.com/user-attachments/assets/42fb64eb-2796-41bd-b2a8-6558d2077867" />

Verify under **Manage Jenkins → Nodes**.

<img width="1107" height="217" alt="image" src="https://github.com/user-attachments/assets/08a2bf60-7a40-4edb-9a55-bdc3d3ab4316" />

---

# 🖥 Run Application Locally ( To Be Run on Lab/local VM )

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

# 🐳 Docker Deployment ( To Be Run on Lab/local VM )

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

# 🐳 Docker Compose ( To Be Run on Lab/local VM )

```bash
docker compose up -d
```

<img width="1107" height="99" alt="image" src="https://github.com/user-attachments/assets/70a3fcb2-a5f7-419b-9a8c-cf38da02509b" />

Application is again available @
```bash 
http://<LAB-VM-PUBLIC-IP>:8081 
```

<img width="784" height="408" alt="image" src="https://github.com/user-attachments/assets/de8a6064-8d30-4311-b359-a318408aa38e" />

---

# ⚙ Jenkins Pipeline
 
Create a new **Pipeline**. Go to Jenkins -> New Item -> Pipeline -> Give it a Name and NEXT 

<img width="1107" height="270" alt="image" src="https://github.com/user-attachments/assets/eec92272-3271-4f34-9fcc-124e7f76c197" />

Enable GitHub Project and provide your public repository URI.

<img width="1107" height="642" alt="image" src="https://github.com/user-attachments/assets/ba20b7ee-f6be-4636-a2fb-f33316698843" />

Enable **GitHub hook trigger for GITScm Polling** so that Jenkins pipeline is triggered as soon as you change/commit anything in your repo to create a CICD setup.

<img width="1107" height="146" alt="image" src="https://github.com/user-attachments/assets/6d62b327-c956-40dc-8ac3-84f52b9a402c" />

Configure SCM and ensure to choose correct branch ( main or master or dev ) and also relative path of Jenkinsfile as compare to root directory of your repo.

<img width="1107" height="741" alt="image" src="https://github.com/user-attachments/assets/83fd3cb3-55cf-47ea-a294-56c1f82d017d" />

---

# 🔗 GitHub Webhook Configuration For Jenkins

navigate to GitHub Repo → Settings → Webhooks → Add Webhook

<img width="1107" height="198" alt="image" src="https://github.com/user-attachments/assets/44ebf94a-8d38-4472-a7fb-c1f5078d34e9" />

Payload needs to provide in below format. Also choose SSL Verification as DISABLE ( not recommended for production but OK for testing) :

```
http://<JENKINS-CONTROLLER-NODE-PUBLIC-IP>:8080/github-webhook/
```

<img width="1107" height="892" alt="image" src="https://github.com/user-attachments/assets/64faf8b3-e34b-45f6-ba7b-ea6b35a00164" />

---

# ✅ Verify CI/CD From Jenkisn UI 

Make a dummy change in README.md, Dockerfile or application code and push to GitHub.

Jenkins should automatically trigger a build else you can always run BUILD NOW to pull code from Repo and build->deploy.

<img width="564" height="1020" alt="image" src="https://github.com/user-attachments/assets/85d2e8e4-80be-4a1c-9e7c-799435947ece" />

So the whole Pipeline Flow is :

```text
GitHub Push
      ↓
Webhook ( If setup Correctly ) 
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
Application ready @ port 8081
```

Application:

```
http://<JENKINS-WORKER-NODE-PUBLIC-IP>:8081
```
You can see the build details at the bottom of the website, which should change after every build.

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

