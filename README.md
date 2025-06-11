# Introduction

Documentation for the application that exposes an API for identifying the polarity of the sentiment of a comment.

# Set Up and Usage

The project provides the Sentiment Analysis API that depends on the Feddit API. Both are containerized using Docker.

## Build and Run Docker Container

In order to access the API, first make sure Docker is installed, and then, in the root folder of the project, run:


```
docker-compose -f docker-compose.yml  up --build
```
This will make the API available at http://0.0.0.0:8000/docs#/

In order to shut down the container, run:

```
docker-compose -f docker-compose.yml down
```

## Local Run of the Tests

This project includes unit tests. In order to run them locally, you can install the dependencies and execute the tests.

First, ensure you have Poetry installed, then run:

```
poetry install
```

Followed by:

```
poetry run pytest
```


# Project Overview

The repository provided creates an API that enables sentiment analysis on comments retrieved from the Feddit API. The core functionalities are as follows: the API allows fetching comments with a default limit of 25, which can be adjusted via query parameters. Each comment in the response includes its sentiment score and polarity. Additionally, the API supports sorting the comments by score and filtering them based on a start and end date. The GitHub repository also includes a workflow that runs linting using Ruff and executes the existing unit tests.

# Project Structure

The layout of this repository is intentionally simple and structured to stay aligned with the scope and requirements of the task. The goal was to keep everything logical and easy to navigate, without introducing unnecessary complexity.


├── Dockerfile                     # Docker setup for the sentiment analysis API
├── docker-compose.yml             # Compose setup integrating this API with the Feddit API
├── pyproject.toml                 # Project dependencies and Python tooling (Poetry)
├── config/
│   └── config.yaml                # Configuration file (e.g. API endpoints)
├── app/                           # Core application code
│   ├── main.py                    # FastAPI application entry point
│   ├── endpoints.py               # Functions for interacting with the Feddit API
│   ├── sentiment_analysis.py      # Comment sentiment analysis logic
│   └── core/
│       ├── config.py              # Loads and parses the config.yaml
│       └── constants.py           # Shared constants used across the app
├── tests/                         # Unit tests
│   ├── test_main.py               # API endpoint tests
│   ├── test_feddit_api.py         # Tests mocking Feddit API interactions
│   └── test_sent_analysis.py      # Tests for sentiment logic
└── README.md                      # Project documentation


# Choices Related to the Tech Stack

In this section, I discuss the tech decisions I made within this project.

### FastAPI

For exposing the API, I chose FastAPI. While there are other valid options, FastAPI is — to the best of my knowledge — one of the current industry standards for building modern, performant Python APIs. It's open source, widely adopted, and something I already use in my current work. Given the nature of the task, FastAPI provided a reliable, well-documented, and efficient framework to implement the required functionality without unnecessary overhead.

### Async Calls

One of the decisions in building this API was to access the Feddit API using asynchronous calls. The reason behind this is to avoid blocking operations during external API requests — especially important when response times may vary.

By using asynchronous functions (`async/await`), the system remains responsive even when waiting for data from the Feddit API. This approach is useful when multiple requests hit the sentiment API simultaneously, making sure that no request has to wait in a queue unnecessarily.

### Sentiment Analysis

For the sentiment analysis part, as the specifications encouraged not to train a model from scratch, I used an out-of-the-box solution from the NLTK package, as it is an open source and reliable solution for this purpose.


