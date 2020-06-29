# secure-suite
![frontend](https://github.com/haney-oliver/secure-suite/workflows/frontend/badge.svg) ![flask backend](https://github.com/haney-oliver/secure-suite/workflows/flask%20backend/badge.svg)

Secure Suite. An open source software package that uses machine learning to increase the user's general internet security.

Secure Suite offers a password manager that allows people on the same network to share secrets with each other via role/permission authorization. It also processes browser traffic to mitigate the risk of navigating to a malicious URL that could steal sensitive user data or scrape cookies/credentials.

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

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```
