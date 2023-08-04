#!/bin/bash

docker build --platform linux/amd64 -t $GCP_REGISTRY_HOSTNAME/$GCP_PROJECT_ID/$APP_NAME:latest .
docker push $GCP_REGISTRY_HOSTNAME/$GCP_PROJECT_ID/$APP_NAME:latest

gcloud beta run deploy $APP_NAME \
  --memory 1Gi \
  --platform managed \
  --region asia-northeast1 \
  --port=8080 \
  --image $GCP_REGISTRY_HOSTNAME/$GCP_PROJECT_ID/$APP_NAME:latest \
  --ingress all \
  --timeout 10m \
  --allow-unauthenticated \
  --set-env-vars "DATASTORE=pinecone" \
  --set-env-vars "BEARER_TOKEN=secret" \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY \
  --set-env-vars OPENAI_ORGANIZATION=$OPENAI_ORGANIZATION \
  --set-env-vars PINECONE_API_KEY=$PINECONE_API_KEY \
  --set-env-vars PINECONE_ENVIRONMENT=$PINECONE_ENVIRONMENT \
  --set-env-vars PINECONE_INDEX=$PINECONE_INDEX \
  --service-account $SERVICE_ACCOUNT \
  --execution-environment gen2
