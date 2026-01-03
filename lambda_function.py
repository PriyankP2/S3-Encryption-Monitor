import boto3
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    Lambda function to monitor S3 buckets for encryption status.
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
