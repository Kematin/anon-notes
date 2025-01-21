#!/bin/bash

SECRET_KEY=$(dd if=/dev/urandom bs=32 count=1 2>/dev/null | openssl base64)

echo "$SECRET_KEY" > secret.key

echo "Secret key generated and saved to 'secret.key'."
echo "Generated Key: $SECRET_KEY"
