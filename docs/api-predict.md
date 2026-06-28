# API: /predict Endpoint

The `/predict` endpoint accepts penguin measurements and returns a predicted species.

The server must be running locally to use this endpoint.
See the project README for instructions on how to start the server.

## Endpoint

```shell
POST http://127.0.0.1:8000/predict
```

## Request

Content-Type: `application/json`

| Field              | Type  | Description                        |
| ------------------ | ----- | ---------------------------------- |
| bill_length_mm     | float | Bill length in millimeters         |
| bill_depth_mm      | float | Bill depth in millimeters          |
| flipper_length_mm  | float | Flipper length in millimeters      |
| body_mass_g        | float | Body mass in grams                 |

### Example Request

```json
{
  "bill_length_mm": 39.1,
  "bill_depth_mm": 18.7,
  "flipper_length_mm": 181,
  "body_mass_g": 3750
}
```

## Response

| Field      | Type   | Description               |
| ---------- | ------ | ------------------------- |
| prediction | string | Predicted species label   |

### Example Response

```json
{ "prediction": "Adelie" }
```

## Error Response

If a required field is missing or non-numeric, the server returns HTTP 400:

```json
{ "detail": "Missing required feature: 'bill_depth_mm'" }
```

## Interactive Docs

When the server is running, FastAPI provides interactive documentation at:

```shell
http://127.0.0.1:8000/docs
```

## Free Server Hosting Options

Many hosting options require a credit card to sign up,
even if you can host your function for free.

Possible options for hosting a free live endpoint:

- **Render** - simplest deploy, free tier, point at a GitHub repo and it builds automatically
- **Railway** - free tier, similar to Render, good developer experience
- **Fly.io** - free tier, more control, slightly more setup
- **Hugging Face Spaces** - free, no credit card, popular in ML circles, supports FastAPI

## Cloud Hosting Options

The major cloud providers all offer free tiers
that can host a FastAPI endpoint,
but all require a credit card to sign up (even for free usage).

- **AWS Lambda + API Gateway** - 1M requests/month free; FastAPI works via the Mangum adapter
- **Azure Functions** - 1M requests/month free; FastAPI works via a similar adapter
- **Google Cloud Run** - 2M requests/month free; easiest of the three for FastAPI;
  build a Docker container and deploy

For this, **Render** or **Hugging Face Spaces** are the easiest starting points.
For production experience closest to what industry uses,
**Google Cloud Run** may be a good option to explore.
