# Deploying to Render (Free)

Render hosts a FastAPI service for free,
but now **requires a credit card** even for the free option.

The service will sleep after inactivity and
wake on the next request (cold start ~50s or more).

## Free Option

Free instances spin down after periods of inactivity.
They do not support SSH access, scaling, one-off jobs, or persistent disks.
Select any paid instance type (starting at $7/month in June 2026)
to enable these features.

## Requirements

- An appropriate, working repository pushed to GitHub
- A free account at [render.com](https://render.com)
- `artifacts/model.joblib` committed to your repo
  - run `model_builder_case.py` locally first if missing.
  - For a custom model output your model_yourname.joblib.

## Update Configuration File

Update the `render.yaml` file in the root project folder.

- update repo `name` to your repo name
- update `startCommand` to use your custom app name

## Steps

1. Go to [render.com](https://render.com) and sign up with your GitHub account.
2. Click **New / Web Service**.
3. Connect your GitHub account if prompted, then select your repo.
4. Render will detect `render.yaml` automatically and pre-fill the settings.
5. Confirm the settings look correct and click **Deploy**.
6. Wait for the build to complete (2–4 minutes first time).
7. Render gives you a public URL like `https://ml-penguin-predictor-xxxx.onrender.com`.

Build Command:

```shell
pip install uv && uv sync --no-dev
```

Start Command (use your module name):

```shell
uv run uvicorn bizintel.serve_case:app --host 0.0.0.0 --port $PORT
```

## Testing Your Deployment

Replace `YOUR-URL` with your Render URL:

```shell
# PowerShell
curl -X POST https://YOUR-URL/predict `
     -H "Content-Type: application/json" `
     -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181, "body_mass_g": 3750}'

# macOS / Linux
curl -X POST https://YOUR-URL/predict \
     -H "Content-Type: application/json" \
     -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181, "body_mass_g": 3750}'
```

For example:

```shell
# PowerShell
curl -X POST https://ml-penguin-predictor.onrender.com/predict `
     -H "Content-Type: application/json" `
     -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181, "body_mass_g": 3750}'

# macOS / Linux
curl -X POST https://ml-penguin-predictor.onrender.com/predict \
     -H "Content-Type: application/json" \
     -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181, "body_mass_g": 3750}'
```

Should return:

```json
{ "prediction": "Adelie" }
```

The interactive API docs are also available at `https://YOUR-URL/docs`.

## Notes

- **Cold starts**: The free tier sleeps after ~15 minutes of inactivity. The first request after sleeping takes ~30 seconds.
- **Redeployment**: Render redeploys automatically on every push to `main`.
- **Logs**: View live logs in the Render dashboard under your service → Logs.
