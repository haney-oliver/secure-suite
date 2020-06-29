# secure-suite
![frontend](https://github.com/haney-oliver/secure-suite/workflows/frontend/badge.svg) ![flask backend](https://github.com/haney-oliver/secure-suite/workflows/flask%20backend/badge.svg)

Secure Suite. An open source software package that uses machine learning to increase the user's general internet security.

Secure Suite offers a secure password manager. It also processes browser traffic to mitigate the risk of navigating to a URL that hosts malicious web services.

# Backend
The Secure Suite Backend is composed of `mal_url_net`, the machine learning model that processes browser traffic, and a flask server to serve the model and endpoints for app interaction.

## Project Setup
```
git clone https://github.com/haney-oliver/secure-suite.git
cd secure-suite/backend/app/
source development.env
```

Now, in the flask app route directory, you can simply run
```
flask run
```

# Frontend

## Project Setup
```
npm install
```

Compile and hot-reload for development
```
npm run serve
```

Compile and minify for production
```
npm run build
```

Lint and fix files
```
npm run lint
```
