#base image with python, node.js, playwright preinstalled
FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

#set working directory
WORKDIR /app

#copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy the rest of the code
COPY . .

#run script with fast flag
CMD ["python", "main.py", "--fast"]
