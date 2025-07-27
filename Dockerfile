# Stage 1: Build Vue.js client
FROM node:18 as client-builder
WORKDIR /app
COPY client/package*.json ./client/
RUN cd client && npm install
COPY client ./client
RUN cd client && npm run build

# Stage 2: Run Python server
FROM python:3.9-slim
WORKDIR /app

# Copy built client files
COPY --from=client-builder /app/client/dist ./server/static

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server ./server

# Expose port (adjust if needed)
EXPOSE 8000

# Run the application
CMD ["python3", "server/api/api.py"]