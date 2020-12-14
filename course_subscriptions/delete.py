import json
import os
import sys
import boto3
from helper import Helper

def lambda_handler(event, context):
    # Read environment variables from template.yaml
    environment = os.environ['ENVIRONMENT']
    dynamodb_dev_uri = os.environ['DYNAMODB_DEV_URI']

    # Create helper object (see helper.py)
    hlp = Helper()

    # Choose database connection depending on Dev or Prod environment
    if environment == "AWS_SAM_LOCAL":
        dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_dev_uri)
    else:
        dynamodb = boto3.resource('dynamodb')

    # Check if the right http method is used, if not then return Forbidden status code
    if event['httpMethod'] != "POST":
        return hlp.json_error("Wrong request method!")

    # Transform http body into a json_map
    json_map = hlp.body_to_json(event['body'])

    # Validate the json payload
    if not hlp.validate_payload(json_map):
        return hlp.json_error("Validation failed!")

    # Execute delete query on DynamoDB table
    table = dynamodb.Table('CourseSubscriptions')
    deleted_item = table.delete_item(
        Key={
            'PK': json_map['PK'],
            'SK': json_map['SK']
        },
    )

    # If DynamoDB could delete the record, we will receive a 200 status code, and can return success.
    if deleted_item['ResponseMetadata']['HTTPStatusCode'] == 200:
        return hlp.json_success(json_map)
    else:
        return hlp.json_error("An error occurred. The item could not be deleted!")