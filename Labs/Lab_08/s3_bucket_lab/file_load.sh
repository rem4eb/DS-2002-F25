#!/bin/bash

# Checking for correct # of arguments
if [ "$#" -ne 3 ]; then
    echo "Error: Incorrect number of arguments."
    echo "Usage: $0 <local-file> <bucket-name> <expiration-seconds>"
    exit 1
fi

LOCAL_FILE="$1"
BUCKET_NAME="$2"
EXPIRATION_SEC="$3"

# Defining S3 path
S3_PATH="s3://${BUCKET_NAME}/${LOCAL_FILE}"

echo "Uploading ${LOCAL_FILE} to ${S3_PATH}"
aws s3 cp "${LOCAL_FILE}" "${S3_PATH}"

# Check if upload was successful before proceeding
if [ $? -ne 0 ]; then
    echo "Error: Upload failed."
    exit 1
fi
echo "Upload successful."

echo "Generating presigned URL (expires in ${EXPIRATION_SEC} seconds):"
aws s3 presign --expires-in "${EXPIRATION_SEC}" "${S3_PATH}"
