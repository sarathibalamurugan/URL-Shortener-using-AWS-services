# URL Shortener using AWS Lambda & DynamoDB

This project implements a serverless URL shortener using AWS Lambda, DynamoDB, and API Gateway.

## 🛠 Steps Overview
1. **Create a DynamoDB Table** (to store URLs)
2. **Create IAM Role** (for Lambda access)
3. **Create Two Lambda Functions** (Shorten & Redirect)
4. **Set up API Gateway** (to expose endpoints)
5. **Test using Postman**

---

## 🔹 Step 1: Create DynamoDB Table
1. Go to **AWS Console** → **DynamoDB** → **Create Table**
2. **Table name**: `URLShortener`
3. **Partition key**: `short_code` (String)
4. Click **Create Table**

---

## 🔹 Step 2: Create IAM Role for Lambda
1. Go to **AWS IAM** → **Roles** → **Create Role**
2. Select **AWS Service** → **Lambda**
3. Attach these policies:
   - `AmazonDynamoDBFullAccess`
   - `AWSLambdaBasicExecutionRole`
4. Name it: `LambdaDynamoDBRole`
5. Click **Create Role**

---

## 🔹 Step 3: Create AWS Lambda Functions

### 1️⃣ Create Lambda Function for URL Shortening
This function generates a short URL and stores it in DynamoDB.

#### Create the Function:
1. Go to **AWS Console** → **Lambda** → **Create Function**
2. **Function name**: `shorten_url`
3. **Runtime**: Python 3.9
4. **Execution role**: Select `LambdaDynamoDBRole`
5. Click **Create Function**
6. Replace the default code with the following:

```python
import json
import boto3
import hashlib

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('URLShortener')

BASE_URL = "https://your-api-id.execute-api.region.amazonaws.com/"  # Replace this later

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
```

7. Click **Deploy**

### 2️⃣ Create Lambda Function for Redirection
This function retrieves the long URL from DynamoDB and redirects users.

#### Create the Function:
1. Go to **AWS Console** → **Lambda** → **Create Function**
2. **Function name**: `redirect_url`
3. **Runtime**: Python 3.9
4. **Execution role**: Select `LambdaDynamoDBRole`
5. Click **Create Function**
6. Replace the default code with:

```python
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('URLShortener')

def lambda_handler(event, context):
    short_code = event["pathParameters"]["short_code"]

    response = table.get_item(Key={"short_code": short_code})

    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"error": "URL not found"})}

    long_url = response["Item"]["long_url"]

    return {
        "statusCode": 301,
        "headers": {"Location": long_url}
    }
```

7. Click **Deploy**

---

## 🔹 Step 4: Create API Gateway

### 1️⃣ Create the API
1. Go to **AWS Console** → **API Gateway** → **Create API**
2. Select **"HTTP API"**
3. Click **Build**
4. **Name**: `URLShortenerAPI`
5. Click **Create API**

### 2️⃣ Add Shorten URL Endpoint
1. Go to **Routes** → Click **Create**
2. **Method**: `POST`
3. **Path**: `/shorten`
4. Click **Create**
5. Go to **Integrations** → Attach a **Lambda Function**
6. Select `shorten_url`
7. Click **Deploy**
8. Copy **API Gateway URL** and update `BASE_URL` in `shorten_url` Lambda function.

### 3️⃣ Add Redirect Endpoint
1. Go to **Routes** → Click **Create**
2. **Method**: `GET`
3. **Path**: `/{short_code}`
4. Click **Create**
5. Go to **Integrations** → Attach a **Lambda Function**
6. Select `redirect_url`
7. Click **Deploy**

---

## 🔹 Step 5: Test Using Postman

### 1️⃣ Shorten a URL
- **Method**: `POST`
- **URL**: `https://your-api-id.execute-api.region.amazonaws.com/shorten`
- **Headers**:
  ```json
  { "Content-Type": "application/json" }
  ```
- **Body (JSON)**:
  ```json
  {
    "long_url": "https://www.google.com"
  }
  ```

✅ **Response (Example)**:
```json
{"short_url": "https://your-api-id.execute-api.region.amazonaws.com/abc123"}
```

### 2️⃣ Test Redirection
- **Method**: `GET`
- **URL**: `https://your-api-id.execute-api.region.amazonaws.com/abc123`

✅ If successful, it should redirect to `https://www.google.com`.

---

## 🎯 Summary
✅ **DynamoDB Table** → Stores `short_code` → `long_url`
✅ **Lambda Functions** →
   - `shorten_url` (POST `/shorten`) → Generates & stores short URLs
   - `redirect_url` (GET `/{short_code}`) → Fetches & redirects
✅ **API Gateway** → Exposes the endpoints
✅ **Postman Testing** → Confirm endpoints work

🚀 **Your URL shortener is now live!** 🎉

---
