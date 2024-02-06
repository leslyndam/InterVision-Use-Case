import json
import random
import string

def lambda_handler(event, context):
    # Password length
    length = 12

    # Characters to generate password from
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate random password
    password = ''.join(random.choice(characters) for i in range(length))

    # Return password in Lambda response
    return {
        'statusCode': 200,
        'password': password
    }
