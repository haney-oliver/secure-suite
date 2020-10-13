FROM node:latest

WORKDIR /

ADD ./ ./

WORKDIR ./

RUN npm install -g npm
RUN npm install
RUN npm rebuild node-sass

CMD ["npm", "run", "serve"]

