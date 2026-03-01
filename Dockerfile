FROM python:3.11-slim

# create working directory
WORKDIR /app

# install python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the repository
COPY . ./

# default streamlit port
EXPOSE 8501

# run the streamlit app on all interfaces so it can be accessed from outside the container
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
