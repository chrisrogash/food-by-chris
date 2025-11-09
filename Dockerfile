FROM python:3.12-slim
RUN apt-get update && apt-get install -y git openssh-client && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
EXPOSE 5469
RUN pip install --no-cache-dir -r /app/admin/requirements.txt
EXPOSE 5469
CMD ["python", "/app/admin/app.py"]
