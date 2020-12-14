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

    # Execute table scan query on DynamoDB table 
    table = dynamodb.Table('CourseSubscriptions')
    response = table.scan()
    data = response['Items'] 

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    # If DynamoDB could scan the table, we will receive a 200 status code, and can return success.
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return hlp.json_success(json.dumps(data))
    else:
        return hlp.json_error("An error occurred. The table could not be scanned!")