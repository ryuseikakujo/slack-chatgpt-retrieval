# ChatGPT Retrieval Plugin

## Introduction

The ChatGPT Retrieval Plugin repository provides a flexible solution for semantic search and retrieval of personal or organizational documents using natural language queries. The repository is organized into several directories:

| Directory                     | Description                                                                                                      |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [`datastore`](/datastore)     | Contains the core logic for storing and querying document embeddings using various vector database providers.    |
| [`models`](/models)           | Contains the data models used by the plugin, such as document and metadata models.                               |
| [`server`](/server)           | Houses the main FastAPI server implementation.                                                                   |
| [`services`](/services)       | Contains utility services for tasks like chunking, metadata extraction, and PII detection.                       |
| [`.well-known`](/.well-known) | Stores the plugin manifest file and OpenAPI schema, which define the plugin configuration and API specification. |

This README provides detailed information on how to set up, develop, and deploy the ChatGPT Retrieval Plugin.

## About

### Plugins

Plugins are chat extensions designed specifically for language models like ChatGPT, enabling them to access up-to-date information, run computations, or interact with third-party services in response to a user's request. They unlock a wide range of potential use cases and enhance the capabilities of language models.

Developers can create a plugin by exposing an API through their website and providing a standardized manifest file that describes the API. ChatGPT consumes these files and allows the AI models to make calls to the API defined by the developer.

A plugin consists of:

- An API
- An API schema (OpenAPI JSON or YAML format)
- A manifest (JSON file) that defines relevant metadata for the plugin

The Retrieval Plugin already contains all of these components. Read the Chat Plugins blogpost [here](https://openai.com/blog/chatgpt-plugins), and find the docs [here](https://platform.openai.com/docs/plugins/introduction).

### Retrieval Plugin

This is a plugin for ChatGPT that enables semantic search and retrieval of personal or organizational documents. It allows users to obtain the most relevant document snippets from their data sources, such as files, notes, or emails, by asking questions or expressing needs in natural language. Enterprises can make their internal documents available to their employees through ChatGPT using this plugin.

The plugin uses OpenAI's `text-embedding-ada-002` embeddings model to generate embeddings of document chunks, and then stores and queries them using a vector database on the backend. As an open-source and self-hosted solution, developers can deploy their own Retrieval Plugin and register it with ChatGPT. The Retrieval Plugin supports several vector database providers, allowing developers to choose their preferred one from a list.

A FastAPI server exposes the plugin's endpoints for upserting, querying, and deleting documents. Users can refine their search results by using metadata filters by source, date, author, or other criteria. The plugin can be hosted on any cloud platform that supports Docker containers, such as Fly.io, Heroku or Azure Container Apps. To keep the vector database updated with the latest documents, the plugin can process and store documents from various data sources continuously, using incoming webhooks to the upsert and delete endpoints. Tools like [Zapier](https://zapier.com) or [Make](https://www.make.com) can help configure the webhooks based on events or schedules.

### API Endpoints

The Retrieval Plugin is built using FastAPI, a web framework for building APIs with Python. FastAPI allows for easy development, validation, and documentation of API endpoints. Find the FastAPI documentation [here](https://fastapi.tiangolo.com/).

One of the benefits of using FastAPI is the automatic generation of interactive API documentation with Swagger UI. When the API is running locally, Swagger UI at `<local_host_url i.e. http://0.0.0.0:8000>/docs` can be used to interact with the API endpoints, test their functionality, and view the expected request and response models.

The plugin exposes the following endpoints for upserting, querying, and deleting documents from the vector database. All requests and responses are in JSON format, and require a valid bearer token as an authorization header.

- `/upsert`: This endpoint allows uploading one or more documents and storing their text and metadata in the vector database. The documents are split into chunks of around 200 tokens, each with a unique ID. The endpoint expects a list of documents in the request body, each with a `text` field, and optional `id` and `metadata` fields. The `metadata` field can contain the following optional subfields: `source`, `source_id`, `url`, `created_at`, and `author`. The endpoint returns a list of the IDs of the inserted documents (an ID is generated if not initially provided).

- `/upsert-file`: This endpoint allows uploading a single file (PDF, TXT, DOCX, PPTX, or MD) and storing its text and metadata in the vector database. The file is converted to plain text and split into chunks of around 200 tokens, each with a unique ID. The endpoint returns a list containing the generated id of the inserted file.

- `/query`: This endpoint allows querying the vector database using one or more natural language queries and optional metadata filters. The endpoint expects a list of queries in the request body, each with a `query` and optional `filter` and `top_k` fields. The `filter` field should contain a subset of the following subfields: `source`, `source_id`, `document_id`, `url`, `created_at`, and `author`. The `top_k` field specifies how many results to return for a given query, and the default value is 3. The endpoint returns a list of objects that each contain a list of the most relevant document chunks for the given query, along with their text, metadata and similarity scores.

- `/delete`: This endpoint allows deleting one or more documents from the vector database using their IDs, a metadata filter, or a delete_all flag. The endpoint expects at least one of the following parameters in the request body: `ids`, `filter`, or `delete_all`. The `ids` parameter should be a list of document IDs to delete; all document chunks for the document with these IDS will be deleted. The `filter` parameter should contain a subset of the following subfields: `source`, `source_id`, `document_id`, `url`, `created_at`, and `author`. The `delete_all` parameter should be a boolean indicating whether to delete all documents from the vector database. The endpoint returns a boolean indicating whether the deletion was successful.

The detailed specifications and examples of the request and response models can be found by running the app locally and navigating to http://0.0.0.0:8000/openapi.json, or in the OpenAPI schema [here](/.well-known/openapi.yaml). Note that the OpenAPI schema only contains the `/query` endpoint, because that is the only function that ChatGPT needs to access. This way, ChatGPT can use the plugin only to retrieve relevant documents based on natural language queries or needs. However, if developers want to also give ChatGPT the ability to remember things for later, they can use the `/upsert` endpoint to save snippets from the conversation to the vector database. An example of a manifest and OpenAPI schema that gives ChatGPT access to the `/upsert` endpoint can be found [here](/examples/memory).

To include custom metadata fields, edit the `DocumentMetadata` and `DocumentMetadataFilter` data models [here](/models/models.py), and update the OpenAPI schema [here](/.well-known/openapi.yaml). You can update this easily by running the app locally, copying the JSON found at http://0.0.0.0:8000/sub/openapi.json, and converting it to YAML format with [Swagger Editor](https://editor.swagger.io/). Alternatively, you can replace the `openapi.yaml` file with an `openapi.json` file.

## Deployment

You can deploy your app to different cloud providers, depending on your preferences and requirements. However, regardless of the provider you choose, you will need to update two files in your app: [openapi.yaml](/.well-known/openapi.yaml) and [ai-plugin.json](/.well-known/ai-plugin.json). As outlined above, these files define the API specification and the AI plugin configuration for your app, respectively. You need to change the url field in both files to match the address of your deployed app.

Before deploying your app, you might want to remove unused dependencies from your [pyproject.toml](/pyproject.toml) file to reduce the size of your app and improve its performance. Depending on the vector database provider you choose, you can remove the packages that are not needed for your specific provider. Refer to the respective documentation in the [`/docs/deployment/removing-unused-dependencies.md`](/docs/deployment/removing-unused-dependencies.md) file for information on removing unused dependencies for each provider.

Once you have deployed your app, consider uploading an initial batch of documents using one of [these scripts](/scripts) or by calling the `/upsert` endpoint.

Here are detailed deployment instructions for various platforms:

- [Deploying to Fly.io](/docs/deployment/flyio.md)
- [Deploying to Heroku](/docs/deployment/heroku.md)
- [Other Deployment Options](/docs/deployment/other-options.md) (Azure Container Apps, Google Cloud Run, AWS Elastic Container Service, etc.)

After you create your app, make sure to change the plugin url in your plugin manifest file [here](/.well-known/ai-plugin.json), and in your OpenAPI schema [here](/.well-known/openapi.yaml), and redeploy.

### Deploy to Google Cloud Run

Run the following commands.

```bash
$ sh deploy.sh
```
