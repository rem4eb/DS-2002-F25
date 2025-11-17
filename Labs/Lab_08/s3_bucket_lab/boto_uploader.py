import boto3
import requests
import argparse
import os
from urllib.parse import urlparse
from botocore.exceptions import ClientError
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Download a file and upload it to S3 with a presigned URL."
    )
    
    # 3 required arguments
    parser.add_argument("url", help="The full URL of the file to download.")
    parser.add_argument("bucket", help="The S3 bucket name to upload to.")
    parser.add_argument("expires_in", type=int, help="Expiration time for the URL in seconds.")
    
    args = parser.parse_args()

    # Getting file from internet
   
    # If the URL has no filename, default to 'downloaded_file.tmp'
    try:
        path = urlparse(args.url).path
        local_filename = os.path.basename(path) or "downloaded_file.tmp"
    except Exception as e:
        print(f"Error parsing URL: {e}")
        sys.exit(1)

    print(f"Attempting to download '{args.url}' as '{local_filename}'...")

    # Using requests to download the file
    try:
        r = requests.get(args.url, allow_redirects=True)
        r.raise_for_status()
        
        with open(local_filename, 'wb') as f:
            f.write(r.content)
            
        print(f"Successfully downloaded '{local_filename}'.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")


    # Upload file to S3
    
    s3 = boto3.client('s3', region_name='us-east-1')
    object_name = local_filename
    print(f"Uploading '{local_filename}' to S3 bucket '{args.bucket}' as '{object_name}'...")

    try:
        s3.upload_file(local_filename, args.bucket, object_name)
        print("Upload successful.")
    
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Local file '{local_filename}' not found for upload.")
        sys.exit(1)

    # Presign file & Output the URL
    
    print(f"Generating presigned URL. Expires in {args.expires_in} seconds.")

    try:
        response = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': args.bucket, 'Key': object_name},
            ExpiresIn=args.expires_in
        )
        
        print("\n--- Success! ---")
        print(f"File: {object_name} \n Bucket: {args.bucket} \n Presigned URL:\n{response}")

    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
