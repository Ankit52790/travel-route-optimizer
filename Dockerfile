FROM python:3.9

WORKDIR /app

# Copy backend code
COPY backend/ .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port for FastAPI
EXPOSE 8080

# Command to run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
