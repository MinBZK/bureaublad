#!/usr/bin/env bash

USERNAME=""
PASSWORD=""
CLIENT_ID="files"
CLIENT_SECRET=""
KEYCLOAK_URL="https://id.la-suite.apps.digilab.network/realms/lasuite/protocol/openid-connect/token"

# Parse command-line options
while getopts u:p:c:s: flag
do
    case "${flag}" in
        u) USERNAME=${OPTARG};;
        p) PASSWORD=${OPTARG};;
        c) CLIENT_ID=${OPTARG};;
        s) CLIENT_SECRET=${OPTARG};;
        *) echo "Invalid option"; exit 1;;
    esac
done


if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ] || [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
    echo "Usage: $0 -u <username> -p <password> -c <client_id> -s <client_secret>"
    exit 1
fi

response=$(curl -s "$KEYCLOAK_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=${CLIENT_ID}" \
  --data-urlencode "client_secret=${CLIENT_SECRET}" \
  --data-urlencode "grant_type=password" \
  --data-urlencode "username=${USERNAME}" \
  --data-urlencode "password=${PASSWORD}" \
  --data-urlencode "scope=openid profile email")


access_token=$(echo $response | jq -r '.access_token')
id_token=$(echo $response | jq -r '.id_token')

echo "ACCESS TOKEN"
echo "-----------"
echo $access_token
echo ""
echo "ID TOKEN"
echo "--------"
echo $id_token