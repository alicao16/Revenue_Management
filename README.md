# 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```bash
   $ streamlit run streamlit_app.py
   ```

> **Tip:** you don't need to keep this file open while the app is running. the command above starts a Python process that continues until you stop it (Ctrl‑C or kill the process). you can also run it in the background:
>
> ```bash
> nohup streamlit run streamlit_app.py &
> # or use the helper script included in the repo
> chmod +x run_streamlit.sh
> ./run_streamlit.sh &
> ```

### Docker container

You can build a container and serve the app anywhere Docker is supported:

```bash
# build the image (first time)
$ docker build -t revenue-game .

# run it locally, mapping port 8501
$ docker run --rm -p 8501:8501 revenue-game
```

Inside the container Streamlit listens on all interfaces so the site works without any code editor open.

### Deploying to a host or the cloud

- **Streamlit Community Cloud**: click the "Open in Streamlit" badge at the top of this README and follow the instructions; the service automatically deploys from the GitHub repository and keeps the app running 24/7.
- **Heroku / Railway / Render / etc.**: the included `Procfile` tells the platform how to start the app. ensure `requirements.txt` is installed and deploy the repo normally.
- **Self‑managed server**: create a systemd service or Docker container using the `Dockerfile` above.

After deployment, users can access the URL without the repository or editor being open — only the running Streamlit server is required.
