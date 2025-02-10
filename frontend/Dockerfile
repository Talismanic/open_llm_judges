# Use node image to build frontend
FROM node:16

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

# Serve frontend using a simple static file server
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
