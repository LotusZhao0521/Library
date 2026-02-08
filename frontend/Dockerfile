# -- Build stage --
FROM node:22-alpine AS build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# -- Serve stage --
FROM nginx:alpine

# nginx:alpine 会自动处理 /etc/nginx/templates/*.template 文件
# 在容器启动时使用环境变量替换（FRONTEND_PORT, FRONTEND_DOMAIN）
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/templates/default.conf.template

# EXPOSE 只是文档性的，实际端口由环境变量 FRONTEND_PORT 控制（默认 80）
EXPOSE 80
