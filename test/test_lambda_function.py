import boto3
import json
import sys
import os
from moto import mock_dynamodb2
import pytest

# Ensure the path to lambda_function.py is correct
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lambda_function import lambda_handler

@pytest.fixture
def dynamodb_mock():
    with mock_dynamodb2():
        yield

def test_lambda_handler(dynamodb_mock):
    # Mock DynamoDB setup
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table_name = "VisitorCount"
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    table.put_item(Item={"id": "123", "visitor_count": 0})

    # Mock event
    event = {"id": "123"}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["visitor_count"] == 1
