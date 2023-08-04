# ChatGPT Slackbot

This repo creates a ChatGPT Slack bot that retrieves your original information. The architecture is as shown below:

![Architecture](/docs/architecture.png)

The tech stack is as follows:

- Cloud Functions
  - This is a bridge between Slack and ChatGPT Retrieval Plugin.
- Cloud Run
  - The Cloud Run hosts [ChatGPT Retrieval Plugin](https://github.com/openai/chatgpt-retrieval-plugin) developed by FastAPI. This app retrieves the related information using OpenAI API and Pinecone.
- OpenAI API
  This generates vector embeddings for text input.
- Pinecone
  This is a vector database that stores your information embedded with Open AI API.

## Environment Variables

You need to set up the following environment variables.

```bash
$ export DATASTORE=pinecone
$ export BEARER_TOKEN=secret
$ export OPENAI_API_KEY=aaa
$ export OPENAI_ORGANIZATION=aaa
$ export PINECONE_API_KEY=aaa
$ export PINECONE_ENVIRONMENT=aaa
$ export PINECONE_INDEX=chatbot
$ export GCP_PROJECT_ID=aaa
$ export GCP_REGISTRY_HOSTNAME=asia.gcr.io
$ export APP_NAME=chatgpt-retrieval-plugin
$ export SERVICE_ACCOUNT=aaa # Service account for Cloud Run
```

This source is for ChatGPT Slackbot. There are three components:

- `retrieval`
  - ChatGPT retrieval plugin deployed on Google Cloud Run. [Here](https://github.com/openai/chatgpt-retrieval-plugin) is the original source.
- `slackbot`
  - Slack bot for responding when you mention `@ChatGPT hogehoge` in your slack. The source code is deployed on Google Cloud Functions.
- `pinecone`
  - Shell script for creating Pinecone index.

## Deployment step

You should deploy three components as the following steps.

1. Create Pinecone index by running `sh pinecone/create-index.sh`
2. Go to `retrieval` directory and deploy Cloud Run
3. Go to `slackbot` directory and deploy Cloud Function (Note that you need to deploy manually via console. This repo just offers the source code.)

Deployment instructions are written in the respective README.md.
