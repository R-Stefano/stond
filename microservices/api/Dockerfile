FROM node:12-slim

WORKDIR /usr/src/app

ENV DB_HOST=34.89.32.113
ENV DB_NAME=stond
ENV DB_USERNAME=root
ENV DB_PSW=root
ENV DB_PORT=3306
ENV DB_CONN_NAME=/cloudsql/stefano-lab:europe-west2:production
#ENV BUCKET_NAME=staging-wiredhub

COPY . .
RUN npm install

CMD [ "npm", "run", "start"]
