# AWS Lambdaの公式Pythonイメージをベースとして使用
FROM public.ecr.aws/lambda/python:3.11

# 必要なライブラリや依存関係がある場合、ここでpipを使ってインストールします
# RUN pip install -r requirements.txt

# Pythonスクリプトをコンテナにコピー
COPY lambda_function.py  /var/task/

# ハンドラの設定
CMD ["lambda_function.handler"]
