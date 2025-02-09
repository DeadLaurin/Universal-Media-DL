# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables
ENV GALLERYDL_VERSION=1.28.5
ENV YTDLP_VERSION=2025.01.26

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Download and install gallery-dl binary
RUN wget https://github.com/mikf/gallery-dl/releases/download/v${GALLERYDL_VERSION}/gallery-dl.bin \
    && chmod +x gallery-dl.bin \
    && mv gallery-dl.bin /usr/local/bin/gallery-dl

# Install yt-dlp
RUN wget https://github.com/yt-dlp/yt-dlp/releases/download/${YTDLP_VERSION}/yt-dlp -O /usr/local/bin/yt-dlp \
    && chmod +x /usr/local/bin/yt-dlp

# Install Flask for the web GUI
RUN pip3 install flask

# Create a directory for the app
WORKDIR /app

# Copy the Flask app and GUI files
COPY . /app

# Expose the web server port
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]