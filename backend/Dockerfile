# use an official lightweight python image
FROM python:3.11-slim 

# prevent from writing .pyc files and force stdout to log immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set working directory
WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# copy project files
COPY . .

# expose the port the app runs on
EXPOSE 8000

# command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]