FROM python:slim

# Set the working directory
WORKDIR /app

# Copy all contents to /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable
ENV PYTHONPATH=/app

# Expose port 8000
EXPOSE 8000

# Run the agent.py script
CMD ["python", "agent.py"]
