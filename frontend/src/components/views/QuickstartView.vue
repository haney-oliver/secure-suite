<template>
  <div class="quickstart-view">
    <navbar />
    <div class="quickstart-container">
      <h1 id="securesuite">Quickstart</h1>
        <p>
          <img
            src="https://github.com/haney-oliver/secure-suite/workflows/frontend/badge.svg"
            alt="frontend"
            class="badge"
          />
          <img
            src="https://github.com/haney-oliver/secure-suite/workflows/flask%20backend/badge.svg"
            alt="flask backend"
            class="badge"
          />
          <img
            src="https://github.com/haney-oliver/secure-suite/workflows/full%20stack/badge.svg"
            alt="full stack"
            class="badge"
          />
        </p>  
      <p>
        Secure Suite. An open source software package that uses machine learning
        to increase the user's general internet security.
      </p>
      <p>
        Secure Suite offers a secure password manager. It also processes browser
        traffic to mitigate the risk of navigating to a URL that hosts malicious
        web services.
      </p>
      <h2 id="runthefullapplication">Run the full application</h2>
      <pre><code>git clone https://github.com/haney-oliver/secure-suite.git
  cd docker
  docker-compose up</code></pre><p>Navigate to <code>http://localhost:8080</code>.</p>
      <h3 id="appservicesandportbindings">App services and port bindings</h3>
      <table class="port-mappings">
        <tr>
          <th>service name</th>
          <th>port bindings</th>
        </tr>
        <tr>
          <th>app-db</th>
          <th>33060:3306</th>
        </tr>
        <tr>
          <th>audit-db</th>
          <th>33061:3306</th>
        </tr>
        <tr>
          <th>zookeeper</th>
          <th>2181:2181</th>
        </tr>
        <tr>
          <th>kafka</th>
          <th>9092:9092</th>
        </tr>
        <tr>
          <th>maxwell</th>
          <th>N/A</th>
        </tr>
        <tr>
          <th>backend</th>
          <th>5000:5000</th>
        </tr>
        <tr>
          <th>app-db</th>
          <th>8080:8080</th>
        </tr>
      </table>
      <h3 id="otherprojectsfeaturedinsecuresuite">
        Other projects featured in Secure Suite
      </h3>
      <p><a href="https://github.com/zendesk/maxwell">Maxwell's Daemon</a></p>
      <p><a href="https://github.com/wurstmeister/kafka-docker">Kafka</a></p>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";

export default {
  name: "QuickstartView",
  components: {
    navbar: Navbar,
  },
};
</script>


<style scoped lang="scss">
@import "@/assets/scss/quickstart-view.scss";
</style>