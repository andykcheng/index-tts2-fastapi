# Use NVIDIA CUDA base image with Ubuntu 24.04 (which defaults to Python 3.12)
# We use the 'devel' tag because DeepSpeed often requires nvcc for compilation
FROM nvidia/cuda:12.6.0-devel-ubuntu24.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
# Ubuntu 24.04 comes with Python 3.12
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    ffmpeg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Copy the rest of the application code
COPY . .

# Ensure outputs directory exists
RUN mkdir -p outputs

# Expose the default FastAPI port
EXPOSE 8000

# Run the application
CMD ["/bin/bash"]
