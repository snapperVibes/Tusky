# Stage 0, "build-stage", builds and compiles the front end
FROM node:15 as build-stage

WORKDIR /src

COPY package*.json /src/

RUN npm install

COPY ./ /src/

ARG FRONTEND_ENV=development

ENV VUE_APP_ENV=%(FRONTEND_ENV)

# Comment out next line to disable tests
#RUN npm run test:unit

RUN npm run build

# Stage 1
FROM nginx:1.15

COPY --from=build-stage /src/dist /usr/share/nginx/html

COPY --from=build-stage /src/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
