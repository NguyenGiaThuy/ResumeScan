#!/bin/bash
#
# Use this script to get the username, password and connection string

username=$(kubectl -n ai-elevate-dev get secret postgres-app -o jsonpath='{.data.username}' | base64 --decode)
password=$(kubectl -n ai-elevate-dev get secret postgres-app -o jsonpath='{.data.password}' | base64 --decode)
host=$(kubectl -n ai-elevate-dev get secret postgres-app -o jsonpath='{.data.host}' | base64 --decode)
port=$(kubectl -n ai-elevate-dev get secret postgres-app -o jsonpath='{.data.port}' | base64 --decode)
dbname=$(kubectl -n ai-elevate-dev get secret postgres-app -o jsonpath='{.data.dbname}' | base64 --decode)
connection_string="postgresql://${username}:${password}@${host}:${port}/${dbname}"

echo "Username: ${username}"
echo "Password: ${password}"
echo "Database name: ${dbname}"
echo "Connection String: ${connection_string}"
