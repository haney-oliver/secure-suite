# Secure Suite
![frontend](https://github.com/haney-oliver/secure-suite/workflows/frontend/badge.svg)   ![flask backend](https://github.com/haney-oliver/secure-suite/workflows/flask%20backend/badge.svg)   ![full stack](https://github.com/haney-oliver/secure-suite/workflows/full%20stack/badge.svg)


Secure Suite. An open source software package that uses machine learning to increase the user's general internet security.

Secure Suite offers a secure password manager. It also processes browser traffic to mitigate the risk of navigating to a URL that hosts malicious web services.


## Run the full application
```
git clone https://github.com/haney-oliver/secure-suite.git
cd docker
docker-compose up
```
Navigate to `http://localhost:8080`.


### App services and port bindings
| service name | port bindings |
|---|---|
| app-db | 33060:3306 |
| audit-db | 33061:3306 |
| zookeeper | 2181:2181 |
| kafka | 9092:9092 |
| maxwell | N/A |
| frontend | 8080:8080 |
| backend | 5000:5000 |


### Other projects featured in Secure Suite
[Maxwell's Daemon](https://github.com/zendesk/maxwell)

[Kafka](https://github.com/wurstmeister/kafka-docker)

