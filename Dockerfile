FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone SadTalker
ARG SADTALKER_ROOT=/workspace/SadTalker
ENV SADTALKER_ROOT=${SADTALKER_ROOT}
RUN mkdir -p /workspace && \
    cd /workspace && \
    git clone https://github.com/OpenTalker/SadTalker.git && \
    cd SadTalker && \
    pip install -r requirements.txt

# Download SadTalker models (this may take a while)
RUN cd ${SADTALKER_ROOT} && \
    bash scripts/download_models.sh || echo "Model download script may need manual execution"

# Copy Django project
COPY . .

# Create media directories
RUN mkdir -p media/reels

# Expose port
EXPOSE 8000

# Create run script
RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python manage.py collectstatic --noinput || true\n\
python manage.py runserver 0.0.0.0:8000' > /app/run.sh && \
    chmod +x /app/run.sh

# Run the application
CMD ["/app/run.sh"]

