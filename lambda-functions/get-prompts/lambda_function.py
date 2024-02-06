import boto3
import json
import os

def lambda_handler(event, context):
    print(json.dumps(event))
    # Initialize DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    
    # Get the node from the event
    node = event['Details']['Parameters']['FlowName']
    
    # Get Table
    table = dynamodb.Table(os.getenv('PROMPT_TABLE'))
    
    try:
        # Retrieve item from DynamoDB table
        response = table.get_item(
            Key={
                'node': node
            }
        )
        
        # Check if the item was found
        if 'Item' in response:
            # Extract the payload from the item and convert it to JSON
            item = response['Item']
            payload = item['payload']
            payload['statusCode'] = 200
            
            return payload
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Item not found'})
            }
    
    except Exception as e:
        raise e
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
