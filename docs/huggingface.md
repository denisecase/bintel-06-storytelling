# Deploying to Hugging Face Spaces (Free)

Hugging Face Spaces hosts your FastAPI service for free with no credit card required.

## Free Option

Services stay live and do not require a card to deploy.

## HF Spaces is Its Own Git Repo

HF Spaces does **not** sync from your GitHub repo automatically.
It creates its own git repo at `huggingface.co/spaces/YOUR-USERNAME/YOUR-SPACE-NAME`.
We upload files to that HF repo via the browser.

## Requirements

- A free account at [huggingface.co](https://huggingface.co)
- `artifacts/model.joblib` committed to your repo
  - run `model_builder_case.py` locally first if missing.
  - For a custom model output your model_yourname.joblib.

## Update Configuration Files

Update the `app.py` file in the root project folder.
It may need changes if your folders or file names have been changed.

Update the `Dockerfile` file in the root project folder.

Update the `requirements.txt` file in the root project folder.
It may not need any changes.

## Steps

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. Give your Space a name (e.g. `ml-penguin-predictor`).
3. Select **Docker** as the SDK, no template needed.
4. Set visibility to **Public**.
5. Click **Create Space**.

## Editing Files

Files live in the HF repo.
Go to (customize for your HF space):

<https://huggingface.co/spaces/YOUR-USERNAME/YOUR-SPACE-NAME/tree/main>

For example:

<https://huggingface.co/spaces/denisecase/ml-penguin-predictor/tree/main>

Click **Contribute" / Upload Files**.
Then drag & drop from your repo (drag the whole folder from root):

- artifacts/ - must have `model.joblib` or similar
- src/ - includes `bizintel` and all the files
- Dockerfile
- README.md
- app.py
- pyproject.toml
- requirements.txt

## Public URLs

- <https://YOUR-USERNAME-YOUR-SPACE-NAME.hf.space/predict>
- <https://YOUR-USERNAME-YOUR-SPACE-NAME.hf.space/docs>

For example:

- <https://denisecase-ml-penguin-predictor.hf.space/predict>
- <https://denisecase-ml-penguin-predictor.hf.space/docs>

## Testing Your Deployment

Replace `YOUR-URL` with your Hugging Face Space URL:

```shell
# PowerShell
curl -X POST https://YOUR-USERNAME-YOUR-SPACE-NAME.hf.space/predict `
     -H "Content-Type: application/json" `
     -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181, "body_mass_g": 3750}'

# macOS / Linux
curl -X POST https://YOUR-USERNAME-YOUR-SPACE-NAME.hf.space/predict \
     -H "Content-Type: application/json" \
     -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181, "body_mass_g": 3750}'
```

Should return:

```json
{ "prediction": "Adelie" }
```

Interactive API docs are available at `https://YOUR-URL/docs`.

## Notes

- **Updates**: To update your Space, re-upload changed files via the browser.
- **Logs**: View build and runtime logs in the Space's **Logs** tab.
- **model.joblib**: Must be uploaded. HF builds from its own repo, not your GitHub repo.
- **Custom model**: If you trained a custom model, upload `artifacts/model_yourname.joblib` and update `app.py` to point to it.
