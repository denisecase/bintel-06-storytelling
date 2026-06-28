# Glossary

Use this page to record terms and ideas that help you understand
professional analytics projects.

This project covers model serving: saving a trained model,
wrapping it in an API, and deploying it so others can send requests
and receive predictions.

Pro-tip: Expand the VS Code **Outline** view (below the navigator on the right)
to see this file organization at-a-glance.

## Model Artifacts

### model serialization

Model serialization is the process of converting a trained in-memory model
into bytes and writing them to a file.
This allows the model to be saved once and reloaded later without retraining.

### joblib

joblib is a Python library for efficiently serializing Python objects,
including large numpy arrays and scikit-learn models.
`joblib.dump()` saves a model to disk; `joblib.load()` restores it.

## Serving

### serving core

The serving core is a small, pure function that takes inputs,
validates them, calls the model, and returns a result.
Keeping this logic separate from the web framework makes it
easier to test and reuse.

### API (Application Programming Interface)

An API is a defined way for one program to send requests to another.
A prediction API accepts input data and returns a model's prediction.

### FastAPI

FastAPI is a Python web framework for building APIs.
It handles routing, input validation, and response formatting.
The serving core is called by FastAPI when a request arrives.

### endpoint

An endpoint is a specific URL that an API exposes for a particular action.
The `/predict` endpoint in this project receives feature values
and returns a predicted species.

### payload

A payload is the data sent in a request to an API.
In this project, the payload is a JSON object containing
the four penguin measurement features.

### JSON

JSON (JavaScript Object Notation) is a lightweight text format
for sending structured data between programs.
API requests and responses in this project use JSON.

### input validation

Input validation checks that incoming data is complete, correctly typed,
and within expected ranges before passing it to the model.
A server that crashes on bad input is fragile;
one that returns a helpful error message is robust.

### HTTP status code

An HTTP status code is a number returned by a server to indicate
the outcome of a request.
200 means success; 422 means the input failed validation;
500 means the server encountered an error.

## Deployment

### deployment

Deployment is the process of making a trained model available
to others over the internet.
In this project, deployment means running the FastAPI server
on a hosting platform such as Render or Hugging Face Spaces.

### cold start

A cold start happens when a server that has been sleeping wakes up
to handle a request.
Free hosting tiers often sleep after inactivity,
causing the first request to be slow.

### Render

Render is a cloud hosting platform that can run Python web services.
The free tier requires a credit card but hosts small projects at no cost.
Services on the free tier sleep after inactivity.

### Hugging Face Spaces

Hugging Face Spaces is a free hosting platform for ML demos and APIs.
It requires no credit card and supports Docker-based deployments.
The space has its own git repository separate from GitHub.
