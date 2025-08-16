# Graph

## 1. Prepare Docker Image

Login:

```sh
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 058264469194.dkr.ecr.ap-southeast-1.amazonaws.com
```

Build & Push:

```sh
REPO=058264469194.dkr.ecr.ap-southeast-1.amazonaws.com
IMAGE=ai-elevate/graph
TAG=

docker build --network=host -t ${REPO}/${IMAGE}:${TAG} .
docker push ${REPO}/${IMAGE}:${TAG}
```
