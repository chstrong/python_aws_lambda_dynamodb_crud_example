import boto3
import sys

# Create the course_subscriptions table in the database.
def create_course_subscriptions_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='CourseSubscriptions',
        KeySchema=[
            {
                'AttributeName': 'PK', # User
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'SK', # Course
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PK',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SK',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

# Delete the course_subscriptions table in the database
def delete_course_subscriptions_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    try:
        table = dynamodb.Table('CourseSubscriptions')
        table.delete()
        return "Table has been deleted"
    except:
        return "Table wasn't found"

# Add an item to the course_subscriptions table
def add_item_to_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('CourseSubscriptions')
    added_item = table.put_item(
        Item={
            'PK': 'U12345',
            'SK': 'C001',
            'Name': 'My first course',
            'Description': 'This is my first course.',
            'Author': 'Chris'
        }
    )
    return added_item

# Scans the course_subscriptions table for all entries
def get_items_from_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:8000")

    table = dynamodb.Table('CourseSubscriptions')
    response = table.scan()
    data = response['Items'] 

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data

# The main method.
if __name__ == '__main__':

    # Get the first parameter provided on the command line when executing the script
    cmd = sys.argv[1]

    # Create the dynamodb object
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    # Execute the function based on provided first argument when executing the script
    if cmd == "create-table":
        table = create_course_subscriptions_table(dynamodb)
        print("Table status:", table.table_status)
    elif cmd == "delete-table":
        message = delete_course_subscriptions_table(dynamodb)
        print("Status: ", message)
    elif cmd == "add-item":
        added_item = add_item_to_table(dynamodb)
        print("Added Item:", added_item)
    elif cmd == "list-items":
        items_list = get_items_from_table(dynamodb)
        print("Items List:", items_list)      