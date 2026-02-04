# Use Python 3.11
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install system dependencies (ffmpeg for audio)
RUN apt-get update && apt-get install -y ffmpeg

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your code files
COPY . .

# Create a cache folder for permission safety
RUN mkdir -p /app/cache

# Open the port for the web server
EXPOSE 7860

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]