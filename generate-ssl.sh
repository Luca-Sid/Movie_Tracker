#!/bin/bash
mkdir -p nginx/ssl
openssl req -x509 -newkey rsa:4096 -nodes -keyout nginx/ssl/self-signed.key -out nginx/ssl/self-signed.crt -days 365 -subj "/CN=localhost"
