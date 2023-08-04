# ChatGPT Slack Bot

## Google Cloud Functions

Deploy Cloud Functions manually.

### Spec

- 1st gen
- Python 3.10
- asia-northeast1
- Allow unauthenticated invocations

### Environment variables

- `OPENAI_API_KEY`
- `OPENAI_ORGANIZATION`
- `SLACK_BOT_TOKEN`
- `SLACK_BOT_SIGNING_SECRET`
- `CHATGPT_RETRIEVER_URL`: Cloud Run Endpoint that you deploy

### Deploy

Deploy the following scripts to Google Cloud Functions from the console.

- `main.py`
- `requirements.txt`

Entry point is `slack_bot`
