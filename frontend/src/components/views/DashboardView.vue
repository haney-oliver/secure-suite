<template>
  <div class="dashboard-view">
    <navbar />
    <div class="doughnut container">
      <h2>URLs Visited</h2>
      <doughnut :chartdata="this.chartData" />
      <div class="stats">
        <h1 id="good">Good: {{ this.number_good_urls }}</h1>
        <h1 id="mal">Mal: {{ this.number_mal_urls }}</h1>
        <p class="small-stat">Total # URLs visited: {{ this.total_number_urls }}</p>
      </div>
    </div>
    <div class="form container" id="expand-url-form">
      <h3>Expand and Analyze Shortened URL</h3>
      <input
        transition="slidein"
        type="text"
        class="input-field"
        id="shortenedUrlField"
        placeholder="Enter shortened URL"
        v-model="shortenedUrl"
      />
      <input
        transition="slidein"
        type="text"
        class="input-field"
        id="expandedUrlField"
        placeholder="Expanded URL will appear here"
        v-model="expandedUrl"
        disabled
      />
      <span class="buttons">
        <button class="main-button" v-on:click="expandShortenedUrl">
          <span class="button-content">Expand</span>
        </button>
      </span>
    </div>
    <div class="form container" id="analyze-url-form">
      <h3>Analyze URL</h3>
      <input
        transition="slidein"
        type="text"
        class="input-field"
        id="urlField"
        placeholder="Enter URL"
        v-model="urlToAnalyze"
      />
      <input
        transition="slidein"
        type="text"
        class="input-field"
        id="expandedUrlField"
        v-model="urlClassificationString"
        disabled
        v-bind:class="[urlBad ? urlBadClass : urlGoodClass]"
      />
      <span class="buttons">
        <button class="main-button" v-on:click="analyzeUrl">
          <span class="button-content">Analyze</span>
        </button>
      </span>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import UrlDoughnut from "@/components/charts/UrlDoughnut.vue";
import axios from "axios";
import { BACKEND_URI } from "../../main";

export default {
  components: {
    navbar: Navbar,
    doughnut: UrlDoughnut,
  },
  data() {
    return {
      urlClassificationString: "",
      urlGoodClass: "url-good",
      urlBadClass: "url-bad",
      urlToAnalyze: "",
      shortenedUrl: "",
      expandedUrl: "",
      urlBad: null,
      urls: [],
      good_urls: [],
      mal_urls: [],
      number_good_urls: [],
      number_mal_urls: [],
      total_number_urls: null,
      data: {
        labels: ["Good", "Mal"],
        datasets: [
          {
            data: [],
            backgroundColor: ["#6480ff", "#ff6384"],
          },
        ],
      },
    };
  },
  methods: {
    fetchUrls() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/ListUrls", {
          session_key: session.session_key,
          user_key: session.user.user_key,
        })
        .then((response) => {
          var analytics = response.data.analytics;
          this.urls = response.data.urls;
          this.good_urls = analytics.good_urls;
          this.mal_urls = analytics.mal_urls;
          this.number_good_urls = analytics.number_good_urls;
          this.number_mal_urls = analytics.number_mal_urls;
          this.total_number_urls = analytics.total_urls_visited;
          if (this.data.datasets[0].data.length == 0) {
            this.data.datasets[0].data.push(analytics.number_good_urls);
            this.data.datasets[0].data.push(analytics.number_mal_urls);
          } else {
            this.data.datasets[0].data[0] = (analytics.number_good_urls);
            this.data.datasets[0].data[1] = (analytics.number_mal_urls);
          }
          this.$forceUpdate();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    expandShortenedUrl() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/ExpandShortenedUrl", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          shortened_url: this.shortenedUrl,
        })
        .then((response) => {
          this.expandedUrl = response.data.expanded_url;
          this.fetchUrls();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    analyzeUrl() {
      var session = JSON.parse(window.sessionStorage.vuex);
      axios
        .post(BACKEND_URI + "/api/CreateOrAnalyzeUrl", {
          session_key: session.session_key,
          user_key: session.user.user_key,
          url: this.urlToAnalyze,
        })
        .then((response) => {
          this.urlBad = !response.data.url_good;
          if (this.urlBad == true) {
            this.urlClassificationString = "Malicious"
          } else {
            this.urlClassificationString = "Benign"
          }
          this.fetchUrls();
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.fetchUrls();
  },
  computed: {
    chartData: function () {
      return this.data;
    },
  },
  watch: {
    data: function () {
      this.fetchUrls();
      this.$forceUpdate();
    }
  }
};
</script>

<style scoped>
@import "../../assets/scss/dashboard-view.scss";
</style>