# Monitor Unencrypted S3 Buckets - Complete Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Code Explanation](#code-explanation)
6. [Testing and Verification](#testing-and-verification)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Introduction

### Project Goal
Enhance AWS security posture by automatically detecting S3 buckets without server-side encryption enabled. This Lambda function scans all S3 buckets in your account and reports those lacking proper encryption configuration.

### Why This Matters
- **Data Security**: Unencrypted S3 buckets pose security risks
- **Compliance**: Many regulations require data encryption at rest
- **Best Practice**: AWS recommends enabling encryption on all S3 buckets
- **Cost**: No additional cost for S3 encryption
- **Automation**: Manual checking is time-consuming and error-prone

### Use Cases
- Security compliance auditing
- Regular security posture assessment
- Automated security monitoring
- Infrastructure security validation
- Compliance reporting

### Technologies Used
- **AWS Lambda**: Serverless compute service
- **AWS S3**: Object storage service
- **Boto3**: AWS SDK for Python
- **AWS IAM**: Identity and Access Management
- **CloudWatch Logs**: Logging and monitoring

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          AWS Account                            │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  S3 Bucket 1 │  │  S3 Bucket 2 │  │  S3 Bucket 3 │           │
│  │  (Encrypted) │  │ (Unencrypted)│  │ (Unencrypted)│           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│         ↓                  ↓                  ↓                 │
│  ┌────────────────────────────────────────────────────────┐     │
│  │           Lambda Function: S3-Encryption-Monitor       │     │
│  │                                                        │     │
│  │  1. List all S3 buckets                                │     │
│  │  2. For each bucket:                                   │     │
│  │     - Get encryption configuration                     │     │
│  │     - Check if encryption is enabled                   │     │
│  │  3. Categorize buckets:                                │     │
│  │     - Encrypted (SSE-S3, SSE-KMS, SSE-C)               │     │
│  │     - Unencrypted (no config found)                    │     │
│  │  4. Log all findings                                   │     │
│  │  5. Return audit report                                │     │
│  └────────────────────────────────────────────────────────┘     │
│                           ↓                                     │
│  ┌────────────────────────────────────────────────────────┐     │
│  │              CloudWatch Logs                           │     │
│  │                                                        │     │
│  │  - Total buckets scanned                               │     │
│  │  - Encrypted bucket names                              │     │
│  │  - Unencrypted bucket names (WARNINGS)                 │     │
│  │  - Encryption types used                               │     │
│  │  - Audit summary                                       │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow:**
1. Lambda function is invoked (manually or scheduled)
2. Function lists all S3 buckets in the account
3. For each bucket, function checks encryption configuration
4. Buckets are categorized as encrypted or unencrypted
5. Results are logged to CloudWatch
6. Function returns comprehensive audit report

---

## Prerequisites

### AWS Account Requirements
- Active AWS account with console access
- At least 3-4 S3 buckets for testing
- Permissions to create Lambda functions and IAM roles

### Knowledge Requirements
- Basic understanding of S3 buckets
- Familiarity with encryption concepts
- Python basics
- AWS IAM understanding

### Understanding S3 Encryption
**Server-Side Encryption (SSE)** - Three types:
- **SSE-S3**: Amazon S3-managed keys (AES-256)
- **SSE-KMS**: AWS Key Management Service keys
- **SSE-C**: Customer-provided keys

This function detects the presence of any server-side encryption configuration.

---

## Step-by-Step Implementation

### Step 1: Create S3 Buckets for Testing

#### 1.1 Navigate to S3 Service

1. Log in to [AWS Management Console](https://console.aws.amazon.com)
2. In the search bar at the top, type **"S3"**
3. Click on **"S3"** under Services
4. You'll see the S3 Dashboard with "Buckets" view


#### 1.2 Understand S3 Bucket Naming Rules

Before creating buckets, note these rules:
- Bucket names must be **globally unique** across all AWS accounts
- Must be 3-63 characters long
- Only lowercase letters, numbers, hyphens, and periods
- Cannot start/end with hyphens or periods
- Should not look like IP addresses

**Recommended naming pattern**: `yourname-projectname-purpose-randomnumber`
- Example: `john-doe-encryption-test-12345`

#### 1.3 Create First Bucket (Without Encryption)

1. Click **"Create bucket"** button (orange button)

2. **Bucket name**: 
   - Enter a unique name: `your-name-unencrypted-test-001`
   - Example: `john-encryption-test-unencrypted-001`
   - Replace "your-name" with your initials or name

3. **AWS Region**: 
   - Select your preferred region (e.g., US East (N. Virginia) us-east-1)
   - Keep the same region for all buckets

4. **Object Ownership**:
   - Keep default: "ACLs disabled (recommended)"

5. **Block Public Access settings**:
   - Keep default: "Block all public access" ✓ checked
   - This is a security best practice

6. **Bucket Versioning**:
   - Keep default: "Disable"

7. **Default encryption**:
   - This is the critical setting!
   - **Select**: "Disable" 
   - This creates an unencrypted bucket for testing

8. **Advanced settings**:
   - Keep defaults

9. Click **"Create bucket"** button at the bottom

10. You should see success message: "Successfully created bucket 'your-bucket-name'"


#### 1.4 Create Second Bucket (Without Encryption)

1. Click **"Create bucket"** again

2. **Bucket name**: `your-name-unencrypted-test-002`

3. **Use same settings** as previous bucket:
   - Same region
   - Block all public access
   - **Disable encryption**

4. Click **"Create bucket"**


#### 1.5 Create Third Bucket (With Encryption - SSE-S3)

1. Click **"Create bucket"** again

2. **Bucket name**: `your-name-encrypted-test-001`

3. **Same basic settings** as before (same region, block public access)

4. **Default encryption**:
   - **Select**: "Enable"
   - **Encryption type**: "Server-side encryption with Amazon S3 managed keys (SSE-S3)"
   - This is the default and recommended option

5. Click **"Create bucket"**


#### 1.6 Create Fourth Bucket (With Encryption - SSE-KMS)

1. Click **"Create bucket"** again

2. **Bucket name**: `your-name-encrypted-test-002`

3. **Same basic settings**

4. **Default encryption**:
   - **Enable**: Checked
   - **Encryption type**: "Server-side encryption with AWS Key Management Service keys (SSE-KMS)"
   - **AWS KMS key**: "AWS managed key (aws/s3)"

5. Click **"Create bucket"**


#### 1.7 Verify All Buckets Created

1. In the S3 Dashboard, you should now see all 4 buckets listed

2. Review the list:
   - 2 buckets without encryption
   - 2 buckets with encryption


#### 1.8 Verify Encryption Settings

For each bucket, let's verify the encryption status:

1. Click on the first **unencrypted bucket name**

2. Click on **"Properties"** tab

3. Scroll down to **"Default encryption"** section

4. It should show: **"Disabled"** or **"Server-side encryption: Disabled"**

5. Go back to buckets list

6. Repeat for all buckets and verify:
   - 2 buckets show encryption: Disabled
   - 2 buckets show encryption: Enabled (SSE-S3 or SSE-KMS)


**✅ Checkpoint**: You should have:
- ✓ 4 S3 buckets created with unique names
- ✓ 2 buckets without encryption enabled
- ✓ 2 buckets with encryption enabled (SSE-S3 and/or SSE-KMS)
- ✓ All buckets in the same region

---

### Step 2: Create IAM Role for Lambda

#### 2.1 Navigate to IAM Service

1. In AWS Console search bar, type **"IAM"**
2. Click on **"IAM"** under Services

#### 2.2 Create New Role

1. In left sidebar, click **"Roles"**
2. Click **"Create role"** button

#### 2.3 Select Trusted Entity

1. **Trusted entity type**: Select **"AWS service"**
2. **Use case**: Select **"Lambda"**
3. Click **"Next"**


#### 2.4 Attach Permissions Policy

1. In the search box, type: `AmazonS3ReadOnlyAccess`

2. **Check the checkbox** next to **"AmazonS3ReadOnlyAccess"**

3. This policy provides:
   - `s3:ListAllMyBuckets` - List all buckets
   - `s3:GetBucketEncryption` - Check encryption settings
   - `s3:GetObject` - Read objects (not needed but included)
   - Read-only access to S3

4. Click **"Next"**

**Important Note**: This is a read-only policy. The Lambda function will NOT modify any buckets.

#### 2.5 Name and Create Role

1. **Role name**: `Lambda-S3-ReadOnly-Role`
2. **Description**: `Allows Lambda to read S3 bucket configurations and check encryption status`
3. Review settings:
   - Trusted entities: lambda.amazonaws.com
   - Permissions: AmazonS3ReadOnlyAccess
4. Click **"Create role"**

#### 2.6 Verify Role

1. Search for your role: `Lambda-S3-ReadOnly-Role`
2. Click on the role name
3. Verify:
   - **Permissions tab**: Shows AmazonS3ReadOnlyAccess
   - **Trust relationships tab**: Shows lambda.amazonaws.com

**✅ Checkpoint**: 
- ✓ IAM role created with read-only S3 permissions
- ✓ Trust relationship configured for Lambda

---

### Step 3: Create Lambda Function

#### 3.1 Navigate to Lambda Service

1. In AWS Console search bar, type **"Lambda"**
2. Click on **"Lambda"** under Services

#### 3.2 Create Function

1. Click **"Create function"** button
2. Select **"Author from scratch"**

#### 3.3 Configure Basic Settings

1. **Function name**: `S3-Encryption-Monitor`
2. **Runtime**: Select **"Python 3.12"** (or latest Python 3.x)
3. **Architecture**: x86_64

#### 3.4 Configure Execution Role

1. Expand **"Change default execution role"**
2. Select **"Use an existing role"**
3. **Existing role**: Select `Lambda-S3-ReadOnly-Role`

#### 3.5 Create Function

1. Review all settings
2. Click **"Create function"**
3. Wait for success message

**✅ Checkpoint**:
- ✓ Lambda function created: S3-Encryption-Monitor
- ✓ Python 3.12 runtime
- ✓ Read-only IAM role attached

---

### Step 4: Add Lambda Function Code

#### 4.1 Access Code Editor

1. You should be on the Lambda function page
2. Scroll to **"Code source"** section
3. You'll see `lambda_function.py` with default code

#### 4.2 Replace Code

1. Select all default code (Ctrl+A or Cmd+A)
2. Delete it
3. Copy and paste the following code:

```python
import boto3
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    Lambda function to monitor S3 buckets for encryption status.
    
    This function performs the following operations:
    - Lists all S3 buckets in the AWS account
    - Checks each bucket for server-side encryption
    - Identifies buckets without encryption
    - Logs detailed findings to CloudWatch
    
    Args:
        event (dict): Lambda event object (not used in this function)
        context (object): Lambda context object (not used in this function)
    
    Returns:
        dict: Response containing status code and audit results
    """
    
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    # Lists to track bucket encryption status
    encrypted_buckets = []
    unencrypted_buckets = []
    
    print("Scanning S3 buckets for encryption status...")
    
    try:
        # List all S3 buckets in the account
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        
        total_buckets = len(buckets)
        print(f"Total buckets found: {total_buckets}")
        
        # Check each bucket for encryption
        for bucket in buckets:
            bucket_name = bucket['Name']
            print(f"Checking bucket: {bucket_name}")
            
            try:
                # Attempt to get bucket encryption configuration
                encryption_response = s3_client.get_bucket_encryption(
                    Bucket=bucket_name
                )
                
                # If we reach here, encryption is enabled
                encrypted_buckets.append(bucket_name)
                print(f"  ✓ Bucket has server-side encryption enabled")
                
                # Optional: Log encryption details
                rules = encryption_response.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
                for rule in rules:
                    sse_algorithm = rule.get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm', 'Unknown')
                    print(f"    Encryption type: {sse_algorithm}")
                
            except ClientError as e:
                # If error code is ServerSideEncryptionConfigurationNotFoundError,
                # the bucket does not have encryption enabled
                error_code = e.response['Error']['Code']
                
                if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                    unencrypted_buckets.append(bucket_name)
                    print(f"  ✗ WARNING: Bucket does NOT have server-side encryption")
                else:
                    # Some other error occurred (e.g., access denied)
                    print(f"  ! Error checking bucket: {error_code}")
                    # We'll treat this as unencrypted to be safe
                    unencrypted_buckets.append(bucket_name)
        
        # Print summary
        print("\n=== AUDIT SUMMARY ===")
        print(f"Total buckets: {total_buckets}")
        print(f"Encrypted: {len(encrypted_buckets)}")
        print(f"Unencrypted: {len(unencrypted_buckets)}")
        
        if unencrypted_buckets:
            print(f"Unencrypted buckets: {unencrypted_buckets}")
        else:
            print("All buckets have encryption enabled! ✓")
        
        # Return success response with audit results
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'S3 bucket encryption audit completed',
                'total_buckets': total_buckets,
                'encrypted_buckets': len(encrypted_buckets),
                'unencrypted_buckets': len(unencrypted_buckets),
                'unencrypted_bucket_names': unencrypted_buckets,
                'encrypted_bucket_names': encrypted_buckets
            })
        }
        
    except Exception as e:
        # Log and return error if something goes wrong
        print(f"Error during S3 bucket audit: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error auditing S3 buckets',
                'error': str(e)
            })
        }
```

#### 4.3 Deploy Code

1. Click **"Deploy"** button
2. Wait for "Changes deployed" success message

#### 4.4 Configure Timeout (Optional)

1. Click **"Configuration"** tab
2. Click **"General configuration"**
3. Click **"Edit"**
4. **Timeout**: Set to **1 min 0 sec**
5. Click **"Save"**

**✅ Checkpoint**:
- ✓ Lambda code deployed
- ✓ Timeout configured
- ✓ Ready for testing

---

### Step 5: Test Lambda Function

#### 5.1 Create Test Event

1. Click **"Test"** tab
2. Click **"Create new event"**
3. **Event name**: `TestEvent`
4. **Template**: hello-world
5. Keep default JSON:
```json
{
  "key1": "value1",
  "key2": "value2",
  "key3": "value3"
}
```
6. Click **"Save"**

#### 5.2 Execute Test

1. Click **"Test"** button (orange)
2. Wait for execution to complete

#### 5.3 Review Execution Results

1. Check **Status**: Should be **"Succeeded"**

2. **Response** should look like:
```json
{
  "statusCode": 200,
  "body": "{\"message\": \"S3 bucket encryption audit completed\", \"total_buckets\": 4, \"encrypted_buckets\": 2, \"unencrypted_buckets\": 2, \"unencrypted_bucket_names\": [\"john-encryption-test-unencrypted-001\", \"john-encryption-test-unencrypted-002\"], \"encrypted_bucket_names\": [\"john-encryption-test-encrypted-001\", \"john-encryption-test-encrypted-002\"]}"
}
```

#### 5.4 Review CloudWatch Logs

1. In execution results, expand the **"Logs"** section

2. You should see detailed output like:
```
START RequestId: xxxxx
Scanning S3 buckets for encryption status...
Total buckets found: 4
Checking bucket: john-encryption-test-encrypted-001
  ✓ Bucket has server-side encryption enabled
    Encryption type: AES256
Checking bucket: john-encryption-test-unencrypted-001
  ✗ WARNING: Bucket does NOT have server-side encryption
Checking bucket: john-encryption-test-encrypted-002
  ✓ Bucket has server-side encryption enabled
    Encryption type: aws:kms
Checking bucket: john-encryption-test-unencrypted-002
  ✗ WARNING: Bucket does NOT have server-side encryption

=== AUDIT SUMMARY ===
Total buckets: 4
Encrypted: 2
Unencrypted: 2
Unencrypted buckets: ['john-encryption-test-unencrypted-001', 'john-encryption-test-unencrypted-002']
END RequestId: xxxxx
```

#### 5.5 Access Full CloudWatch Logs

1. Click **"Monitor"** tab
2. Click **"View CloudWatch logs"**
3. Click on the latest log stream
4. View complete logs

**✅ Checkpoint - Testing Complete**:
- ✓ Lambda executed successfully
- ✓ All 4 buckets scanned
- ✓ Encrypted buckets identified correctly (2)
- ✓ Unencrypted buckets identified correctly (2)
- ✓ Detailed logs in CloudWatch
- ✓ Status code 200 returned

---

## Code Explanation

### Imports

```python
import boto3
import json
from botocore.exceptions import ClientError
```

- **boto3**: AWS SDK for Python
- **json**: For JSON serialization in responses
- **ClientError**: Exception class for handling AWS API errors

### S3 Client Initialization

```python
s3_client = boto3.client('s3')
```

- Creates S3 client to interact with S3 service
- Uses Lambda function's IAM role for authentication

### Listing All Buckets

```python
response = s3_client.list_buckets()
buckets = response.get('Buckets', [])
```

- **list_buckets()**: Returns all S3 buckets in the account
- Returns dictionary with 'Buckets' key containing list of bucket info
- Each bucket has 'Name' and 'CreationDate'

### Checking Bucket Encryption

```python
encryption_response = s3_client.get_bucket_encryption(
    Bucket=bucket_name
)
```

- **get_bucket_encryption()**: Retrieves encryption configuration
- If encryption is enabled, returns configuration details
- If NOT enabled, raises `ServerSideEncryptionConfigurationNotFoundError`

### Error Handling for Unencrypted Buckets

```python
except ClientError as e:
    error_code = e.response['Error']['Code']
    
    if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
        unencrypted_buckets.append(bucket_name)
```

- Catches the specific error for missing encryption
- This is NOT a failure - it's expected for unencrypted buckets
- We use exception handling as the detection mechanism

### Logging Encryption Type

```python
rules = encryption_response.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
for rule in rules:
    sse_algorithm = rule.get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm', 'Unknown')
    print(f"    Encryption type: {sse_algorithm}")
```

- Extracts encryption algorithm type
- Common values:
  - "AES256" = SSE-S3
  - "aws:kms" = SSE-KMS

### Audit Summary

```python
print("\n=== AUDIT SUMMARY ===")
print(f"Total buckets: {total_buckets}")
print(f"Encrypted: {len(encrypted_buckets)}")
print(f"Unencrypted: {len(unencrypted_buckets)}")
```

- Provides clear summary in logs
- Easy to review in CloudWatch

### Response Structure

```python
return {
    'statusCode': 200,
    'body': json.dumps({
        'message': 'S3 bucket encryption audit completed',
        'total_buckets': total_buckets,
        'encrypted_buckets': len(encrypted_buckets),
        'unencrypted_buckets': len(unencrypted_buckets),
        'unencrypted_bucket_names': unencrypted_buckets,
        'encrypted_bucket_names': encrypted_buckets
    })
}
```

- Returns comprehensive audit report
- Includes both counts and bucket names
- Can be parsed by other systems

---

## Testing and Verification

### Test Scenarios

#### Scenario 1: All Buckets Encrypted
- **Setup**: Enable encryption on all buckets
- **Expected**: unencrypted_buckets = 0
- **Status**: ✅ Pass

#### Scenario 2: All Buckets Unencrypted
- **Setup**: Disable encryption on all buckets
- **Expected**: encrypted_buckets = 0
- **Status**: ✅ Pass

#### Scenario 3: Mixed Status (Current Test)
- **Setup**: 2 encrypted, 2 unencrypted
- **Expected**: Correctly categorize each
- **Status**: ✅ Pass

#### Scenario 4: No Buckets in Account
- **Setup**: Delete all buckets
- **Expected**: total_buckets = 0
- **Status**: ✅ Pass

### Verification Checklist

- [ ] Function deploys without errors
- [ ] All buckets are scanned
- [ ] Encrypted buckets identified correctly
- [ ] Unencrypted buckets identified correctly
- [ ] Encryption types logged (AES256, aws:kms)
- [ ] Audit summary is clear
- [ ] Status code 200 returned
- [ ] No errors in CloudWatch logs

---

## Troubleshooting

### Issue 1: "Access Denied" Error

**Symptoms**: Cannot read bucket encryption

**Solutions**:
1. Verify IAM role has `AmazonS3ReadOnlyAccess`
2. Check Lambda is using correct role
3. If buckets in different account, need cross-account permissions

### Issue 2: Buckets Not Found

**Symptoms**: total_buckets = 0 but buckets exist

**Solutions**:
1. Check Lambda and buckets are in same AWS account
2. Verify IAM permissions include `s3:ListAllMyBuckets`
3. Check region - S3 is global but function must have permissions

### Issue 3: All Buckets Showing as Unencrypted

**Symptoms**: Encrypted buckets appear unencrypted

**Solutions**:
1. Verify buckets actually have encryption enabled:
   - Go to S3 Console
   - Check bucket Properties → Default encryption
2. Ensure IAM role has `s3:GetBucketEncryption` permission
3. Wait a few minutes after enabling encryption

### Issue 4: Function Timeout

**Symptoms**: Function times out with many buckets

**Solutions**:
1. Increase timeout in Configuration → General → Edit
2. Set to 1-2 minutes
3. For 100+ buckets, consider pagination or splitting logic

---

## Best Practices

### Security

1. **Least Privilege IAM Policy**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets",
        "s3:GetBucketEncryption"
      ],
      "Resource": "*"
    }
  ]
}
```

2. **Add SNS Notifications**
```python
# After finding unencrypted buckets
if unencrypted_buckets:
    sns_client.publish(
        TopicArn='arn:aws:sns:region:account:topic',
        Subject='Unencrypted S3 Buckets Found',
        Message=json.dumps(unencrypted_buckets)
    )
```

3. **Schedule Regular Scans**
- Use EventBridge to run daily/weekly
- Cron: `cron(0 9 * * ? *)` - Daily at 9 AM UTC

### Operational

1. **Store Results in DynamoDB**
- Track encryption status over time
- Historical compliance records

2. **Create Dashboard**
- Use CloudWatch Dashboard
- Visualize encryption compliance

3. **Auto-Remediation**
- Enable encryption automatically
- Require approval for production buckets

---

## Summary

### What We Built
- ✅ Automated S3 encryption monitoring
- ✅ Read-only security audit function
- ✅ CloudWatch logging for compliance
- ✅ Comprehensive reporting

### Skills Learned
- S3 bucket encryption concepts
- Boto3 S3 API usage
- Read-only Lambda operations
- Exception handling for AWS APIs
- Security compliance automation

### Production Enhancements
- Add SNS notifications
- Schedule with EventBridge
- Store results in DynamoDB
- Create compliance dashboard
- Implement auto-remediation
- Export audit reports

---

**Congratulations!** You've completed the Project. This solution helps maintain AWS security best practices by ensuring all S3 buckets have encryption enabled.
