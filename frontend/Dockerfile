FROM node:12.19.0

WORKDIR /

ADD ./ ./

WORKDIR ./

RUN npm install -g npm@6.14.8
RUN npm install
RUN npm rebuild node-sass

CMD ["npm", "run", "serve"]

