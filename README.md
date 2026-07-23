# easymovies


/opt/miniconda3/bin/python -m pip install boto3 botocore     # Install boto3 into that Python

aws configure        #  Get AWS credentials from Simplilearn Lab page => Access Key Details 
aws sts get-caller identity # confirm if the access keys are working

ansible-galaxy collection install -r requirements.yml  # 4.	Install the required Ansible collections and provision both EC2 instances.

ansible-playbook -i inventory.ini 1.provision.yml    # This created jenkins controller and worker node. Attaches a Security Group which allows access on port 22(ssh) and 5000-32767 for jenkins(8080) or any other nodeport which you would like to expose in kubernetes ervice.

<img width="1107" height="185" alt="image" src="https://github.com/user-attachments/assets/136e3949-05bf-464d-8d00-54fd848c98e8" />

This step should auto update the inventory.ini file with new nodes IP details as well as vars.yml with new admin_password. 
<img width="1108" height="124" alt="image" src="https://github.com/user-attachments/assets/4128127c-aaff-40c6-a245-44da00f14d9f" />
<img width="559" height="328" alt="image" src="https://github.com/user-attachments/assets/03b1829b-e460-4966-94ed-f14bb725e793" />

Use this password to login to the Jenkins UI @ <<CONTROLLER-NODE-PUBLIC-IP>>:8080 
It also generates the SSH key at ~/.ssh/jenkins-ci-generated-key so you can login to the Jenkins Server (or worker nodes)  using its Public IP :  ssh -i .ssh/jenkins-ci-generated-key ubuntu@<<CONTROLLER/WORKER-NODE-PUBLIC-IP>>

Login to the Jenkins Controller Node : ssh -i .ssh/jenkins-ci-generated-key ubuntu@<<CONTROLLER-NODE-PUBLIC-IP>>
Same Admin password can be retrieved from below command :  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
Check the status of Jenkins service : sudo systemctl status jenkins

Open the Web browser using <<CONTROLLER-NODE-PUBLIC-I>>:8080 and enter the password : 
<img width="1107" height="424" alt="image" src="https://github.com/user-attachments/assets/62b8c1ed-0ba8-4c3d-b63e-d6ea8323c6e9" />

Upon verification Jenkins UI will be accessible. Select INSTALL SUGGESTED PLUGINS 
<img width="1107" height="570" alt="image" src="https://github.com/user-attachments/assets/a18c8d4e-c740-4969-99d6-9a085aae0db7" />
You can create a new user or continue using admin user : 
<img width="1107" height="916" alt="image" src="https://github.com/user-attachments/assets/0656bacd-4b96-4127-9f0f-e01c8b07aebc" />
<img width="1107" height="407" alt="image" src="https://github.com/user-attachments/assets/c4f06743-16fd-4b72-9875-89e22b184096" />


From Local/Lab VM : ansible-playbook -i inventory.ini 2.install_plugins.yml
This should install below plugins : 
    jenkins_plugins:
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

ansible-playbook -i inventory.ini 3.configure_worker.yml    : Configures worker node to get atached to Jenkins controller node. 
<img width="1107" height="496" alt="image" src="https://github.com/user-attachments/assets/42fb64eb-2796-41bd-b2a8-6558d2077867" />
Go to Jenkins UI -> Configure Jenkins => Nodes : You should see worker node registered and healthy state.
<img width="1107" height="217" alt="image" src="https://github.com/user-attachments/assets/08a2bf60-7a40-4edb-9a55-bdc3d3ab4316" />


Ansible configuration part completes here. Now we need to setup jenkins pipeline and related stuff. Switch to jenkins applciation directory <<<>>>> 

We will first try to build container image Locally and run it  Then use docker compose and finally use jenkins pipelie to build ->test->deploy on worker node. 

Deploy-Verify Applciation locally :  We will directly run the application on our lab/local VM ( Without Docker ).
pip install -r requirements.txt              # Install requird python modules/libraries locally
<img width="1107" height="497" alt="image" src="https://github.com/user-attachments/assets/bd6c644e-48fc-404e-88de-9f88cef1568c" />

python app.py         # Deploy the app.py applciation . It will start on port 8081 ( configurable in app.py)
<img width="1107" height="431" alt="image" src="https://github.com/user-attachments/assets/d47d888a-c4fb-4705-8267-a32901277eeb" />
Use  <<LAB-VM-PUBLIC-IP>>:8081  to access locally running  application : 
<img width="784" height="408" alt="image" src="https://github.com/user-attachments/assets/6e1808e6-a30c-4300-a1fa-50261764f71d" />
Navigate the website and verify. Once testing done, you can stop the container using CTRL+C


Build-Test-Deploy-Verify Containerized Applciation locally :  Now we will create a docker container and then deploy on our lab/local VM.
docker build -t easymovies:v1 .             : It will use Dockerfile in same directory and build a docker image with name easymovies and tag v1.
<img width="1107" height="384" alt="image" src="https://github.com/user-attachments/assets/2abc0ab4-d735-4815-8f61-fea398367a29" />

docker run -d   --name easymovies   -p 8081:8081   easymovies:v1               # Since image is ready we can now launch the container so that application is running on our VM a s a container.
Use  <<LAB-VM-PUBLIC-IP>>:8081  to access locally running containerized applciation : 
<img width="784" height="408" alt="image" src="https://github.com/user-attachments/assets/de8a6064-8d30-4311-b359-a318408aa38e" />

Once testing is done you can stop & remove the container  : docker stop easymovies && docker rm easymovies ( or Directly via docker rm -f easymovies )


Build-Test-Deploy-Verify Containerized Applciation via Docker Compose :  
Now we will create a docker container and then deploy on our lab/local VM using docker compose. docker compose give us flexibilty to deploy/manage multi container applciation instead of managing those individually.
docker compose up -d    # bring up the service(s) in compose.yml file. 
<img width="1107" height="99" alt="image" src="https://github.com/user-attachments/assets/70a3fcb2-a5f7-419b-9a8c-cf38da02509b" />
Use  <<LAB-VM-PUBLIC-IP>>:8081  to access locally running containerized applciation : 
<img width="1107" height="99" alt="image" src="https://github.com/user-attachments/assets/b390a90a-eb16-49d7-b6dc-2cdec9228559" />

So now we have tested out application locally using 3 different ways. Its time to make it automated via CICD pipeline via Jenkins. 


Clone the repository 


jenkins Pipeline COnfiguration : 

Configure Jenkins Pipeline :      New Item -> Pipeline 
Use your own name and Click Next : 
<img width="1107" height="270" alt="image" src="https://github.com/user-attachments/assets/eec92272-3271-4f34-9fcc-124e7f76c197" />


Check On Github Project and provide your public Repo URL : 
<img width="1107" height="642" alt="image" src="https://github.com/user-attachments/assets/ba20b7ee-f6be-4636-a2fb-f33316698843" />

Also Check "GitHub hook trigger for GITScm Pollin" as it will allow our pipeline to trigger automatically whenever we are changing something in github repo.
<img width="1107" height="146" alt="image" src="https://github.com/user-attachments/assets/6d62b327-c956-40dc-8ac3-84f52b9a402c" />
Choose SCM as git and provide Repo URL and Branch Name main/master. NOTE : Ensure you choose relaive path of youer Jenkinsfile related to root path of your directory. 
<img width="1107" height="741" alt="image" src="https://github.com/user-attachments/assets/83fd3cb3-55cf-47ea-a294-56c1f82d017d" />



Github Configuration For SCM Webhook Trigger : 

Go to your github repo => Settings => Webhooks => Add Webhook  
<img width="1107" height="198" alt="image" src="https://github.com/user-attachments/assets/44ebf94a-8d38-4472-a7fb-c1f5078d34e9" />

Enter payload URL as  :  http://<<JENKINS-CONTROLLER-NODE-PUBLIC-IP>>:8080/github-webhook/       like http://54.211.213.242:8080/github-webhook/
Use SSL verification Disbaled ( not recommended) which is fine for testing purpose. Add the webhook. 
<img width="1107" height="892" alt="image" src="https://github.com/user-attachments/assets/64faf8b3-e34b-45f6-ba7b-ea6b35a00164" />


Make a dummy change in Readme.md or Dockerfile or any html file.  It should trigger the Jenkins pipeline and you can check the build status in Jenkins UI : 

<img width="564" height="1020" alt="image" src="https://github.com/user-attachments/assets/85d2e8e4-80be-4a1c-9e7c-799435947ece" />


So now our CICD Setup is complete where wheenever there is a code change in Applciation Repo, it sends a trigger to jenkins pipeline.
Jenkins will pull the latest code -> Build the image -> Test the image using pytest => Deploy the image on worrker node port 8081 and applciation is visible on <<JENKINS-WORKER-NODE-PUBLIC-IP>>:8081.
If you scroll to the bottom of the Easymovies website page, you will see currently deployed build details and it will update with every deployment : 
<img width="1107" height="361" alt="image" src="https://github.com/user-attachments/assets/d64f1cdd-f647-4fda-a570-4af0da69d809" />



