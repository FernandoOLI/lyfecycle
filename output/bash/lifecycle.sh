#!/bin/bash


echo Applying lifecycle to bucket: lyfecycle-management-bucket
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON_FILE="$SCRIPT_DIR/../rules/lyfecycle-management-bucket.json"
aws s3api put-bucket-lifecycle-configuration \
  --bucket lyfecycle-management-bucket \
  --lifecycle-configuration file://$JSON_FILE

echo Applying lifecycle to bucket: lyfecycle-management-bucket-test
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON_FILE="$SCRIPT_DIR/../rules/lyfecycle-management-bucket-test.json"
aws s3api put-bucket-lifecycle-configuration \
  --bucket lyfecycle-management-bucket-test \
  --lifecycle-configuration file://$JSON_FILE
