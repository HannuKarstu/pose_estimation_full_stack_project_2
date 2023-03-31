
FROM node:16-alpine

WORKDIR /app
COPY frontend .

RUN npm ci
RUN npm run build

RUN apk --no-cache add curl

CMD [ "npx", "serve", "build" ]