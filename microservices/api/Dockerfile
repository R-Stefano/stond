FROM node:12-slim

WORKDIR /usr/src/app

ENV DB_HOST=35.189.95.166
ENV DB_NAME=stond
ENV DB_USERNAME=root
ENV DB_PSW=root
ENV DB_PORT=3306
ENV DB_CONN_NAME=/cloudsql/beyondborders:europe-west2:beyondborders
#ENV BUCKET_NAME=staging-wiredhub

COPY . .
RUN npm install

CMD [ "npm", "run", "start"]
