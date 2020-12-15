import json
import os
import sys
import boto3
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

    # Check if the right http method is used, if not then return Forbidden status code
    if event['httpMethod'] != "DELETE":
        return hlp.json_error("Wrong request method!")

    print(path_parameters)

    # Validate the pk id passed through the url
    if not hlp.validate_pk(path_parameters['pk']):
        return hlp.json_error("An error occurred.")

    # Validate the sk id passed through the url
    if not hlp.validate_sk(path_parameters['sk']):
        return hlp.json_error("An error occurred.")    

    # Execute delete query on DynamoDB table
    table = dynamodb.Table('CourseSubscriptions')
    deleted_item = table.delete_item(
        Key={
            'PK': path_parameters['pk'],
            'SK': path_parameters['sk']
        },
    )

    # If DynamoDB could delete the record, we will receive a 200 status code, and can return success.
    if deleted_item['ResponseMetadata']['HTTPStatusCode'] == 200:
        return hlp.json_success({"message": "success"})
    else:
        return hlp.json_error("An error occurred. The item could not be deleted!")