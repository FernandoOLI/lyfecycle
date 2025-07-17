#!/bin/bash


echo Applying lifecycle to bucket: lyfecycle-management-bucket 

aws s3api put-bucket-lifecycle-configuration \
--bucket lyfecycle-management-bucket \
--lifecycle-configuration file://../rules/raw_lifecycle.json
