# Remote Docker Image Builder using AWS EC2

I created this repository because network status of my Macbook is too bad to build Docker image.... :D 

## Scenario

1. __main__.py clones Github repository which contains Dockerfile (on EC2 Instance using SSH)
2. Build from that Dockerfile of the repository, and push to Docker Hub. That's all.

## Prerequisite

Python with pip version 3.+ 

## How to Use

1. Clone this repository.

   ```
   $ git clone https://github.com/alicek106/aws-docker-image-builder.git
   $ cd aws-docker-image-builder
   ```

2. [Optional] Create virtualenv 

   ```
   $ virtualenv aws-docker-image-builder
   $ source aws-docker-image-builder/bin/activate
   ```

3. Install dependencies

   ```
   $ pip install -r requirements.txt
   ```

4. Export AWS credentials : Access and Secret Keys

   ```
   $ export AWS_ACCESS_KEY_ID=...
   $ export AWS_SECRET_ACCESS_KEY=...
   ```

5. Set variables in ```config.ini``` 

   ```
   [CONFIG]
   AWS_INSTANCE_NAME = Test
   EC2_SSH_PRIVATE_KEY = /Users/alice/Desktop/book/dev/DockerEngineTestInstance.pem
   GITHUB_URL = https://github.com/alicek106/nginx-ingress-annotation-text.git
   DOCKER_IMAGE_NAME = alicek106/ingress-annotation-test:test-version
   DOCKER_HUB_USER = alicek106
   DOCKER_HUB_PASSWORD = kageroudays
   ```

- **AWS_INSTANCE_NAME** : The EC2 Instance name that build Docker image
- **EC2_SSH_PRIVATE_KEY** : SSH Private key path to access the instance
- **GITHUB_URL** : Github repository URL that contains Dockerfile
- **DOCKER_IMAGE_NAME** : Image name to be built and pushed
- **DOCKER_HUB_USER** and **DOCKER_HUB_PASSWORD** : Docker Hub access information

6. Execute python script. Docker image will be built and pushed to Docker Hub.

   ```
   $ python3.6 __main__.py
   ```



Happy Docker Image!
