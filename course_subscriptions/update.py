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

    # Execute update query on DynamoDB table 
    table = dynamodb.Table('CourseSubscriptions')
    updated_item = table.update_item(
        Key={
            'PK': json_map['PK'],
            'SK': json_map['SK']
        },
        UpdateExpression="set #N=:n, #D=:d, #A=:a",
        ExpressionAttributeNames={
            '#N': 'Name',
            '#D': 'Description',
            '#A': 'Author'
        },
        ExpressionAttributeValues={
            ':n': json_map['Name'],
            ':d': json_map['Description'],
            ':a': json_map['Author']
        },
        ReturnValues="UPDATED_NEW"
    )

    # If DynamoDB could update the record, we will receive a 200 status code, and can return success.
    if updated_item['ResponseMetadata']['HTTPStatusCode'] == 200:
        return hlp.json_success(json_map)
    else:
        return hlp.json_error("An error occurred. The item could not be updated!")