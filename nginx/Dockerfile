FROM node:latest AS frontend-builder

WORKDIR /frontend

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ ./

ARG VITE_API_BASE_URL=/api

ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build


FROM nginx:alpine

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend-builder \
    /frontend/dist \
    /usr/share/nginx/html

EXPOSE 80

CMD [
    "nginx",
    "-g",
    "daemon off;"
]