# Use the official Node.js image.
FROM node:18

# Create and change to the app directory.
ENV NODE_ENV=production
ENV PORT=8080
ENV MODEL_URL='https://storage.googleapis.com/ml-models-buckets-nic/model-in-prod/model.json'

# Copy local code to the container image.
COPY . .

RUN apt-get update && \
    apt-get install -y build-essential \
    wget \
    python3 \
    make \
    gcc \
    libc6-dev


RUN npm install

EXPOSE 8080

CMD [ "npm", "run", "prod" ]