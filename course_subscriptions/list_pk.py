import json
import os
import sys
import boto3
from boto3.dynamodb.conditions import Key
from helper import Helper


def lambda_handler(event, context):
    # Read environment variables from template.yaml
    environment = os.environ['ENVIRONMENT']
    dynamodb_dev_uri = os.environ['DYNAMODB_DEV_URI']
    path_parameters = event['pathParameters']

    # Create helper object (see helper.py)
    hlp = Helper()

    # Choose database connection depending on Dev or Prod environment
    if environment == "AWS_SAM_LOCAL":
        dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_dev_uri)
    else:
        dynamodb = boto3.resource('dynamodb')

    # Validate the pk id passed through the url
    if not hlp.validate_pk(path_parameters['pk']):
        return hlp.json_error("An error occurred.") 

    # Execute table scan query on DynamoDB table 
    table = dynamodb.Table('CourseSubscriptions')
    response = table.query(
        KeyConditionExpression=Key('PK').eq(path_parameters['pk'])
    )
    data = response['Items']

    # If DynamoDB could scan the table, we will receive a 200 status code, and can return success.
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return hlp.json_success(json.dumps(data))
    else:
        return hlp.json_error("An error occurred. The table could not be scanned!")