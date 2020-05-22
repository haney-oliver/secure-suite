<template>
  <div id="dashboard">
    <div class="navbar" id="navbar">
      <ul class="option">
        <li>
          <router-link
            :to="{name: 'Vault', params: { userId: this.$route.params.userId}}"
          >Vault</router-link>
        </li>
        <li>
          <router-link to="/preferences">Preferences</router-link>
        </li>
        <li>
          <a v-on:click="logout">Logout</a>
        </li>
      </ul>
    </div>
    <div class="container">
      <div class="grid">
        <div class="chart">
          <h1>Url Live Classification</h1>
          <canvas id="url-live-chart"></canvas>
        </div>
        <div class="chart">
          <h1>Accuracy over Epochs</h1>
          <canvas id="nidl1_ne3_lr0_001_bs_16_acc_data"></canvas>
        </div>
        <div class="chart">
          <h1>Loss over Epochs</h1>
          <canvas id="nidl1_ne3_lr0_001_bs_16_loss_data"></canvas>
        </div>
        <div class="chart">
          <h1>Accuracy over Epochs</h1>
          <canvas id="nidl1_ne6_lr0_005_bs_32_acc_data"></canvas>
        </div>
        <div class="chart">
          <h1>Loss over Epochs</h1>
          <canvas id="nidl1_ne6_lr0_005_bs_32_loss_data"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js";
import nidl1_ne3_lr0_001_bs_16_acc_data from "../nidl1_ne3_lr0_001_bs_16_acc_data.js";
import nidl1_ne3_lr0_001_bs_16_loss_data from "../nidl1_ne3_lr0_001_bs_16_loss_data.js";
import nidl1_ne6_lr0_005_bs_32_acc_data from "../nidl1_ne6_lr0_005_bs_32_acc_data.js";
import nidl1_ne6_lr0_005_bs_32_loss_data from "../nidl1_ne6_lr0_005_bs_32_loss_data.js";
import urlLiveChartData from "../url-live-chart-data.js";
import axios from "axios";

export default {
  name: "dashboard",
  data() {
    return {
      nidl1_ne3_lr0_001_bs_16_acc_data: nidl1_ne3_lr0_001_bs_16_acc_data,
      nidl1_ne3_lr0_001_bs_16_loss_data: nidl1_ne3_lr0_001_bs_16_loss_data,
      nidl1_ne6_lr0_005_bs_32_acc_data: nidl1_ne6_lr0_005_bs_32_acc_data,
      nidl1_ne6_lr0_005_bs_32_loss_data: nidl1_ne6_lr0_005_bs_32_loss_data,
      urlLiveChartData: urlLiveChartData
    };
  },
  methods: {
    getCookie(cname) {
      var name = cname + "=";
      var decodedCookie = decodeURIComponent(document.cookie);
      var ca = decodedCookie.split(";");
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    },
    logout() {
      var ssid = this.getCookie("ssid");
      axios
        .post("http://localhost:8080/api/LogoutUser", {
          userId: this.$route.params.userId
        })
        .then(response => {
          var code = response.data.status;
          if (code == 200) {
            axios
              .post("http://localhost:8080/api/DeleteSession", {
                sessionId: ssid
              })
              .then(function(response) {
                var code = response.data.status;
                if (code == 200) {
                  document.cookie = "ssid=";
                  document.location.href = "/";
                } else {
                  console.log(
                    "Status: " +
                      code +
                      " ErrorMessage: " +
                      response.data.errorMessage
                  );
                }
              })
              .catch(function(error) {
                console.log(error);
              });
          } else {
            console.log(
              "Status: " + code + " ErrorMessage: " + response.data.errorMessage
            );
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    createChart(chartId, chartData) {
      const ctx = document.getElementById(chartId);
      const myChart = new Chart(ctx, {
        type: chartData.type,
        data: chartData.data,
        options: chartData.options
      });
      return myChart;
    },
    async getUrlList() {
      const response = await fetch("http://localhost:8080/api/ListUrl", {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json"
        }
      });
      return response.json();
    },
    addData(data, chart) {
      if (data) {
        console.log("Data: ");
        console.log(data);
        chart.data.datasets.forEach(dataset => {
          console.log("Dataset data: ");
          console.log(dataset.data);
          dataset.data = data;
          console.log(dataset.data);
        });
      }
    },
    updateData(chart) {
      console.log("Update Data");
      var mal_urls = [];
      var good_urls = [];
      this.getUrlList().then(response => {
        console.log("List URL Response: ");
        console.log(response);
        response.urls.forEach(url => {
          if (url.urlMalicious == true) {
            mal_urls.push(url);
          } else {
            good_urls.push(url);
          }
        });
        console.log(good_urls.length, mal_urls.length);
        this.addData([good_urls.length, mal_urls.length], chart);
        chart.update();
      });
    }
  },
  mounted() {
    this.createChart(
      "nidl1_ne3_lr0_001_bs_16_acc_data",
      this.nidl1_ne3_lr0_001_bs_16_acc_data
    );

    this.createChart(
      "nidl1_ne3_lr0_001_bs_16_loss_data",
      this.nidl1_ne3_lr0_001_bs_16_loss_data
    );

    this.createChart(
      "nidl1_ne6_lr0_005_bs_32_acc_data",
      this.nidl1_ne6_lr0_005_bs_32_acc_data
    );

    this.createChart(
      "nidl1_ne6_lr0_005_bs_32_loss_data",
      nidl1_ne6_lr0_005_bs_32_loss_data
    );

    var urlChart = this.createChart("url-live-chart", this.urlLiveChartData);
    this.updateData(urlChart);
  }
};
</script>

<style scoped>
.navbar {
  background-color: #2985ff;
}

.navbar a {
  color: white;
}

.navbar a:hover,
.navbar a:active,
.navbar a:focus {
  color: rgb(255, 238, 0);
  cursor: pointer;
}

.chart {
  flex-basis: 45%;
  padding: 1.5rem;
}

.container {
  text-align: center;
}
</style>
