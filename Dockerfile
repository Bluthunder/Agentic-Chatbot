FROM python:3.11-slim

# System dependencies for llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential cmake git \
    && apt-get clean

# Avoid CPU-specific optimizations for cross-platform compatibility (e.g. Mac M4 → EC2)
ENV CMAKE_ARGS="-DLLAMA_CUBLAS=off -DLLAMA_METAL=off -DLLAMA_AVX2=on -DLLAMA_FMA=on -DLLAMA_AVX512=off -DCMAKE_CXX_FLAGS='-march=x86-64-v3'"

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and model files
COPY ./src ./src
COPY ./api ./api
COPY ./src/ai_agent/models ./models

# Set environment variable for model path
ENV MISTRAL_MODEL_PATH=/app/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "api.chat:app", "--host", "0.0.0.0", "--port", "8000"]
