import json
import boto3
import hashlib

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('URLShortener')

BASE_URL = "https://z5akcn0ob0.execute-api.us-east-1.amazonaws.com/"  # Replace this later

def lambda_handler(event, context):
    body = json.loads(event['body'])
    long_url = body.get("long_url")

    if not long_url:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing long_url"})}

    short_code = hashlib.md5(long_url.encode()).hexdigest()[:6]

    table.put_item(Item={"short_code": short_code, "long_url": long_url})

    short_url = BASE_URL + short_code
    return {
        "statusCode": 200,
        "body": json.dumps({"short_url": short_url})
    }
