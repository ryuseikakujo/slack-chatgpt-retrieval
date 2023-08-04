import json
import logging
import os
import re

import functions_framework
import google.cloud.logging
import openai
from box import Box
from flask import Request
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.retrievers import ChatGPTPluginRetriever
from slack_bolt import App, context
from slack_bolt.adapter.google_cloud_functions import SlackRequestHandler

logging_client = google.cloud.logging.Client()
logging_client.setup_logging(log_level=logging.DEBUG)

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.organization = os.environ.get("OPENAI_ORGANIZATION")

# When running on FaaS, process_before_response must be True due to slow response time
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ["SLACK_BOT_SIGNING_SECRET"],
    process_before_response=True,
)
handler = SlackRequestHandler(app)


# Response to an event mentions to the Bot app
@app.event("app_mention")
def handle_app_mention_events(body: dict, say: context.say.say.Say):
    """Function to generate a response to a mentions to the app

    Args:
        body: HTTP request body
        say: Send contents to Slack
    """
    logging.debug(type(body))
    logging.debug(body)
    box = Box(body)
    user = box.event.user
    text = box.event.text
    only_text = re.sub("<@[a-zA-Z0-9]{11}>", "", text).strip()
    logging.debug("text:", only_text)

    if only_text:
        # ChatGPTPluginRetriever
        retriever = ChatGPTPluginRetriever(
            url=os.environ["CHATGPT_RETRIEVER_URL"], bearer_token="secret"
        )

        # RetrievalQA chain
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(), chain_type="stuff", retriever=retriever
        )

        ans = qa.run(only_text)
        logging.info("***** answer:", ans)

        url = ""
        if ans not in [" I don't know."]:
            documents = retriever.get_relevant_documents(text)
            if len(documents):
                url = f"\nRef: {documents[0].metadata['metadata']['url']}"

        say(f"<@{user}> {ans} {url}")
    else:
        say(f"<@{user}> What?")


def create_chat_completion(messages: list) -> tuple[str, int]:
    """Function that calls the OpenAI API to generate answers to questions

    Args:
        messages: List of chat contents

    Returns:
        GPT-3.5 generated response content
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        # max_tokens=4096,
        stop=None,
    )
    openai_response = response["choices"][0]["message"]["content"]
    total_tokens = response["usage"]["total_tokens"]
    return (openai_response, total_tokens)


# Entry points called by Cloud Functions
@functions_framework.http
def slack_bot(request: Request):
    """Functions that receive slack event requests and execute each process

    Args:
        request: Event request of Slack

    Returns:
        Connection to SlackRequestHandler
    """
    header = request.headers
    body = request.get_json()

    if body.get("type") == "url_verification":
        logging.info("url verification started")
        headers = {"Content-Type": "application/json"}
        res = json.dumps({"challenge": body["challenge"]})
        logging.debug(f"res: {res}")
        return (res, 200, headers)
    elif header.get("x-slack-retry-num"):
        logging.info("slack retry received")
        return {"statusCode": 200, "body": json.dumps({"message": "No need to resend"})}

    return handler.handle(request)
