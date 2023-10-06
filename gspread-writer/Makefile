# AWS ECR Makefile Boilerplate

# 設定項目
AWS_PROFILE := default
AWS_REGION := ap-northeast-1
REPO_NAME := warikan-san-gspread-writer
IMAGE_NAME := warikan-san-gspread-writer
TAG := $(shell git ls-files . | xargs cat | md5)

# ECR リポジトリのURLを取得
REPO_URL := $(shell aws ecr describe-repositories --repository-names $(REPO_NAME) --profile $(AWS_PROFILE) --region $(AWS_REGION) --query 'repositories[0].repositoryUri' --output text)

# Dockerイメージをビルド
build: test
	docker build -t $(IMAGE_NAME):$(TAG) .

runlocal:
	docker run -itp 8080:8080 --rm -v ${PWD}:/var/task  warikan-san-gspread-writer:latest "lambda_function.lambda_handler_local"

# AWS ECRへのログイン
login:
	aws ecr get-login-password --region $(AWS_REGION) --profile $(AWS_PROFILE) | docker login --username AWS --password-stdin $(REPO_URL)

# DockerイメージをECRへプッシュ
push: build login
	docker tag $(IMAGE_NAME):$(TAG) $(REPO_URL):$(TAG)
	docker push $(REPO_URL):$(TAG)

# ローカルのDockerイメージを削除
clean:
	docker rmi -f $(IMAGE_NAME):$(TAG)
	docker rmi -f $(REPO_URL):$(TAG)

test:
	pipenv run python -m pytest

.PHONY: build runlocal login push clean test
