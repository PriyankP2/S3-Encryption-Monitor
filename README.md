# Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3

## 📋 Project Overview

This project demonstrates automated security monitoring of S3 buckets using AWS Lambda and Boto3. The Lambda function scans all S3 buckets in your AWS account and identifies those without server-side encryption enabled, helping maintain security compliance.

## 🎯 Objectives

- Automate S3 bucket security auditing
- Detect buckets without server-side encryption
- Implement read-only security monitoring
- Practice AWS security best practices
- Use Boto3 for S3 operations

## 🏗️ Architecture

```
S3 Buckets (Multiple) → Lambda Function (Boto3) → S3 API
                              ↓
                   Check Encryption Status
                              ↓
                        CloudWatch Logs
                              ↓
                    Report Unencrypted Buckets
```

## 📦 Prerequisites

- AWS Account (Free Tier eligible)
- Basic understanding of AWS S3
- Python 3.x knowledge
- Understanding of encryption concepts
- AWS IAM permissions

## 🚀 Features

- **Automated scanning**: Checks all S3 buckets in account
- **Encryption detection**: Identifies buckets without server-side encryption
- **Read-only operations**: No modifications to buckets
- **Comprehensive logging**: Detailed CloudWatch logs for audit
- **Security compliance**: Helps maintain security standards
- **Easy integration**: Can be scheduled or triggered by events

## 📁 Repository Structure

```
assignment3-s3-encryption-monitor/
├── README.md                          # This file
├── lambda_function.py                 # Lambda function code
├── documentation.md                   # Detailed step-by-step guide
└── screenshots/                       # Project screenshots
```

## 🔧 Setup Instructions

### Step 1: Create S3 Buckets

1. Create 3-4 S3 buckets with unique names
2. Enable server-side encryption on 1-2 buckets
3. Leave 1-2 buckets without encryption (for testing)

### Step 2: Create IAM Role

1. Create IAM role: `Lambda-S3-ReadOnly-Role`
2. Attach policy: `AmazonS3ReadOnlyAccess`
3. Trust entity: Lambda service

### Step 3: Create Lambda Function

1. Function name: `S3-Encryption-Monitor`
2. Runtime: Python 3.12
3. Execution role: `Lambda-S3-ReadOnly-Role`
4. Deploy the code from `lambda_function.py`

### Step 4: Test

1. Create test event in Lambda
2. Execute the function
3. Review CloudWatch logs for unencrypted buckets

## 💻 Lambda Function Code

The Lambda function performs the following operations:

1. Initializes Boto3 S3 client
2. Lists all S3 buckets in the account
3. Checks encryption configuration for each bucket
4. Identifies buckets without server-side encryption
5. Logs all findings to CloudWatch
6. Returns list of unencrypted buckets

See `lambda_function.py` for complete implementation.

## 📊 Expected Results

- ✅ All S3 buckets are scanned
- ✅ Encrypted buckets are identified and logged
- ✅ Unencrypted buckets are clearly reported
- ✅ CloudWatch logs show detailed information
- ✅ Lambda returns HTTP 200 status code
- ✅ No errors in execution

## 📸 Screenshots

All screenshots documenting the implementation process are available in the `screenshots/` directory.

## 🔍 Testing

### Manual Testing

```bash
# Test event (use Lambda console)
{}
```

### Expected Output

```json
{
  "statusCode": 200,
  "body": {
    "message": "S3 bucket encryption audit completed",
    "total_buckets": 4,
    "encrypted_buckets": 2,
    "unencrypted_buckets": 2,
    "unencrypted_bucket_names": [
      "my-test-bucket-unencrypted-1",
      "my-test-bucket-unencrypted-2"
    ]
  }
}
```

## 📝 CloudWatch Logs Sample

```
Scanning S3 buckets for encryption status...
Total buckets found: 4
Checking bucket: my-test-bucket-encrypted-1
  ✓ Bucket has server-side encryption enabled
Checking bucket: my-test-bucket-unencrypted-1
  ✗ WARNING: Bucket does NOT have server-side encryption
Checking bucket: my-test-bucket-encrypted-2
  ✓ Bucket has server-side encryption enabled
Checking bucket: my-test-bucket-unencrypted-2
  ✗ WARNING: Bucket does NOT have server-side encryption

=== AUDIT SUMMARY ===
Total buckets: 4
Encrypted: 2
Unencrypted: 2
Unencrypted buckets: ['my-test-bucket-unencrypted-1', 'my-test-bucket-unencrypted-2']
```

## 🔐 Security Considerations

### Current Implementation
- Uses `AmazonS3ReadOnlyAccess` for read-only access

### Production Recommendations
- Use least privilege IAM policies
- Restrict to specific S3 operations
- Add SNS notifications for unencrypted buckets
- Implement automated remediation
- Enable AWS Config rules for continuous monitoring

### Recommended IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets",
        "s3:GetBucketEncryption",
        "s3:GetEncryptionConfiguration"
      ],
      "Resource": "*"
    }
  ]
}
```

## 🎓 Learning Outcomes

- S3 bucket security best practices
- Server-side encryption concepts
- Read-only Lambda operations
- Boto3 S3 client usage
- Security compliance automation
- CloudWatch logging patterns
- Error handling in AWS services

## 🔄 Future Enhancements

- [ ] Add SNS notifications for unencrypted buckets
- [ ] Schedule daily/weekly scans with EventBridge
- [ ] Store results in DynamoDB for historical tracking
- [ ] Add email reports with detailed findings
- [ ] Implement auto-remediation (enable encryption)
- [ ] Check for other security configurations (public access, versioning)
- [ ] Create dashboard for visualization
- [ ] Export reports to S3 as CSV/JSON

## 🧹 Cleanup

To avoid unnecessary AWS charges:

```bash
# Delete S3 buckets (empty them first)
# Delete Lambda function
# Delete IAM role
# Remove CloudWatch log groups
```

## ⚠️ Important Notes

### S3 Bucket Naming
- S3 bucket names must be globally unique
- Use your initials or random numbers in bucket names
- Example: `john-doe-test-bucket-12345`

### Encryption Types
This function checks for **server-side encryption**, which includes:
- SSE-S3 (Amazon S3-managed keys)
- SSE-KMS (AWS KMS-managed keys)
- SSE-C (Customer-provided keys)

### Read-Only Access
- This function only reads bucket configurations
- It does NOT modify any buckets
- Safe to run in production environments

## 📚 References

- [AWS S3 Server-Side Encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html)
- [Boto3 S3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)

## 📄 License

This project is created for educational purposes as part of AWS Lambda automation assignment.

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to open an issue or submit a pull request.

---

**Note**: This project is part of AWS Lambda and Boto3 automation assignments. For detailed implementation steps, refer to `documentation.md`.
