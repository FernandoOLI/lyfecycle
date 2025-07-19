#!/bin/bash
BUCKET="lyfecycle-management-bucket"
PREFIX="data/"

aws s3 ls s3://$BUCKET/$PREFIX --recursive | awk '{print $4}' | \
grep '/' | awk -F'/' '{
    path=""
    for(i=1;i<NF;i++) {
        path = path $i "/"
    }
    print "s3://'"$BUCKET"'/" path
}' | sort -u | grep -E '_delta_log/|year='
