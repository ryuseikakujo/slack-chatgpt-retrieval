#!/bin/bash

curl --request POST \
    --url https://controller.$PINECONE_ENVIRONMENT.pinecone.io/databases \
    --header "Api-Key: ${PINECONE_API_KEY}" \
    --header 'accept: text/plain' \
    --header 'content-type: application/json' \
    --data '
{
  "name": "'"${PINECONE_INDEX}"'",
  "dimension": 1536,
  "metric": "cosine",
  "pods": 1,
  "replicas": 1,
  "pod_type": "s1.x1"
}
'
