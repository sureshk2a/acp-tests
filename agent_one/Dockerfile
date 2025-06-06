FROM python:slim

# Set the working directory
WORKDIR /app

# Copy all contents to /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir uv && \
    python -m venv .venv && \
    . .venv/bin/activate && \
    UV_LINK_MODE=copy uv sync

# Set environment variable
ENV PYTHONPATH=/app

# Expose port 8000
EXPOSE 8000

# Run the agent.py script with the virtual environment's Python
CMD [".venv/bin/python", "agent.py"]
