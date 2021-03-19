# README.


# App
at `echo-server` folder.

Locally:
```bash
docker build -t echo .
docker run -p 5000:5000 echo
```
or `python app.py` , but don't forget to `pip install -r requirements.txt` before.


Any path except `index.html` can be used to get an echo back,with any method. GET,POST,PATCH,DELETE.

example:
```bash
curl -d '{"key":"value"' -H "Content-Type: application/json" -X POST HOST:5000/
```

```bash
curl -d "key=value" -X POST HOST:5000/
```

Template folder used only for local development, in Dockerfile we don't use it, since it going to be passed as ConfigMap on deployment.

Used alpine since `Slim docker image` was required.


# Terraform
* Created ami user with programmatic access on my AWS account.
`brew install awlcli`
* Configurated awscli with ami user.
`aws configure`
* Instal terraform
```bash
brew install tfenv
tfenv install 0.12.19
tfenv use 0.12.19
```

* `cd terraform` 
```bash
terraform init
terraform apply
```

It will create ECR repo,
vpc, eks with node pool. 
Used `t3.small`, micro wasn't enough :(

Output would be a kube config, you should use it as kube context, locate it at `.kube/config`
 `brew install aws-iam-authenticator` will be required.

# Upload docker image after all Infrastracture is created

```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 528977880076.dkr.ecr.eu-central-1.amazonaws.com

docker build -t echo .

docker tag echo:latest 528977880076.dkr.ecr.eu-central-1.amazonaws.com/echo:v1

docker push 528977880076.dkr.ecr.eu-central-1.amazonaws.com/echo:v1
```

# Kubernetes deployment
All deployment needed files located at `deployment` folder.

Create new namespace for deployment.
`kubectl create namespace echo-server`

`kubectl apply -f . -n echo-server` - will apply all files.

`configmap.yaml` - Contains `index.html` data.
`service.yaml` - Loadbalancer that will create ELB.
`deployment.yaml` - Contains deployment configuration , image, ports and sets ConfigMap as volume for deployment.

To get number host of service, `kubectl get svc -n echo-server`  it will appear under `EXTERNAL-IP`
