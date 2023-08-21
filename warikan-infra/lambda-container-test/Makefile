# AWS ECR Makefile Boilerplate

# 設定項目
AWS_PROFILE := default
AWS_REGION := ap-northeast-1
REPO_NAME := warikan-san-lambda-container
IMAGE_NAME := warikan-san-lambda-container
TAG := $(shell md5 -q ./lambda_function.py)

# ECR リポジトリのURLを取得
REPO_URL := $(shell aws ecr describe-repositories --repository-names $(REPO_NAME) --profile $(AWS_PROFILE) --region $(AWS_REGION) --query 'repositories[0].repositoryUri' --output text)

# Dockerイメージをビルド
build:
	docker build -t $(IMAGE_NAME):$(TAG) .
	docker build -t $(IMAGE_NAME):latest .

# AWS ECRへのログイン
login:
	aws ecr get-login-password --region $(AWS_REGION) --profile $(AWS_PROFILE) | docker login --username AWS --password-stdin $(REPO_URL)

# DockerイメージをECRへプッシュ
push: build login
	docker tag $(IMAGE_NAME):$(TAG) $(REPO_URL):$(TAG)
	docker tag $(IMAGE_NAME):$(TAG) $(REPO_URL):latest
	docker push $(REPO_URL):$(TAG)
	docker push $(REPO_URL):latest

# ローカルのDockerイメージを削除
clean:
	docker rmi -f $(IMAGE_NAME):$(TAG)
	docker rmi -f $(REPO_URL):$(TAG)
	docker rmi -f $(IMAGE_NAME):latest
	docker rmi -f $(REPO_URL):latest

.PHONY: build login push clean
