#!/bin/sh

aws configure set aws_access_key_id "$Access_id" && aws configure set aws_secret_access_key "$Access_secret" && aws configure set region "$Region" && aws configure set output "none"

exec python boto_api.py