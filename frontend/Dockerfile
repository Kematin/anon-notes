FROM node:22-alpine AS builder

WORKDIR /frontend/app

COPY app/package*.json ./

RUN npm ci

COPY app/ ./

COPY .env.prod /frontend/.env.production

RUN npm run build

FROM alpine:3.19

COPY --from=builder /frontend/app/dist /app/dist
