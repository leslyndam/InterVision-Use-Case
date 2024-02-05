import json
import os
import boto3
import random


def delegate(session_attributes, slots):

    return {
        'sessionState': {
            'dialogAction': {
                'type': 'Delegate'
            },
            'intent': {
                'name': "authenticate",
                'state': 'InProgress',
                'slots': slots
            },
            'sessionAttributes': session_attributes
        }
    }
    
def fetch_employee(employee_id):
    dynamodb = boto3.resource('dynamodb')
    EMPLOYEE_TABLE_NAME = os.getenv('EMPLOYEE_TABLE_NAME')
    employee_table = dynamodb.Table(EMPLOYEE_TABLE_NAME)

    response = employee_table.get_item(
        Key={
            'employee_id': employee_id
        }
        )
    employee_item = response.get('Item', {})
    return employee_item
    
def send_verification_email_with_template(email_address, verification_code):
    client = boto3.client('pinpoint')

    APPLICATION_ID = os.getenv('APPLICATION_ID')
    TEMPLATE_NAME = os.getenv('TEMPLATE_NAME')
    SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')
    

    message_request = {
        'Addresses': {
            email_address: {
                'ChannelType': 'EMAIL'
            }
        },
        'TemplateConfiguration': {
            'EmailTemplate': {
                'Name': TEMPLATE_NAME,
                'Version': '1'
            }
        },
        'MessageConfiguration': {
            'EmailMessage': {
                'FromAddress': SENDER_ADDRESS,
                'Substitutions': {
                    'VerificationCode': [
                        verification_code,
                    ]
                }
            }
        }
    }

    try:
        response = client.send_messages(
            ApplicationId=APPLICATION_ID,
            MessageRequest=message_request
        )
        print(f"Email sent using template '{TEMPLATE_NAME}'! Message ID: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")


def lambda_handler(event, context):

    print("Event: ", json.dumps(event))
    session_attributes = event['sessionState'].get('sessionAttributes', {})
    validated = session_attributes.get("validated")
    valid = session_attributes.get("valid", False)
    employee_searched = session_attributes.get("employee_searched", False)
    slots = event['sessionState']['intent']['slots']
    employee_id_confirmation = slots.get('employee_id_confirmation')
    
    if not employee_searched and employee_id_confirmation:
        print("Validating")
        if employee_id_confirmation['value']['interpretedValue'] == 'Yes':
            employee_id = slots['employee_id']['value']['interpretedValue']
            employee_item = fetch_employee(employee_id)
            session_attributes['employee_searched'] = True
            if employee_item != {}:
                session_attributes['email_start'] = ".".join(employee_item['personal_email'][:4].upper())
                session_attributes['email'] = employee_item['personal_email']
                session_attributes['employee_found'] = True
                verification_code = ''.join([str(random.randint(0, 9)) for _ in range(5)])
                session_attributes['verification_code'] = verification_code
                send_verification_email_with_template(employee_item['personal_email'], verification_code)
            else:
                session_attributes['employee_found'] = False
    
    if slots.get('confirmation_code') and not validated:
        print("Verification")
        verification_code = slots['confirmation_code']['value']['interpretedValue']
        if verification_code == session_attributes['verification_code']:
            session_attributes['valid'] = True
        else:
            session_attributes['valid'] = False
        
        
    response = delegate(session_attributes, slots)
    print(response)
    
    return response
