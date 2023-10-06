import os
import boto3
import json

def get_secret_dict(secret_name, region_name="ap-northeast-1"):
    """
    Retrieve a secret from AWS Secrets Manager.
    """
    client = boto3.client('secretsmanager', region_name=region_name)

    response = client.get_secret_value(SecretId=secret_name)

    # Assuming the secret is a JSON object
    assert 'SecretString' in response
    secret = response['SecretString']
    return json.loads(secret)
