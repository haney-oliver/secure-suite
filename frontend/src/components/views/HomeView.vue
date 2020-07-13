<template>
  <div class="home-view">
    <navbar />
    <div class="continer banner hidden">
      <img src="@/assets/images/secure-suite-logo.svg" />
    </div>
    <div class="container">
      <div class="grid">
        <article class="hidden">
          <img src="@/assets/images/vault.svg" />
          <h3>Store secure passwords</h3>
          <p>Generate and securely store passwords.</p>
        </article>
        <article class="hidden">
          <img src="@/assets/images/flask.svg" />
          <h3>Flask backend</h3>
          <p>Intuitive RPC-like API.</p>
        </article>
        <article class="hidden">
          <img src="@/assets/images/encryption.svg" />
          <h3>End to end encryption</h3>
          <p>Encrypted data transfer.</p>
        </article>
        <article class="hidden">
          <img src="@/assets/images/open-source.svg" />
          <h3>Open source</h3>
          <p>Own your data.</p>
        </article>
        <article class="hidden">
          <img src="@/assets/images/report.svg" />
          <h3>Real time analytics</h3>
          <p>Understand your data.</p>
        </article>
        <article class="hidden">
          <img src="@/assets/images/vpn.svg" />
          <h3>Easy VPN setup</h3>
          <p>Connect to your internal network in one click.</p>
        </article>
      </div>
      <div class="card hidden">
        <h2 class="card-title">Mitigating security vunlerabilities enabled by cloud computing.</h2>
        <img class="card-picture" src="@/assets/images/cloud-security.svg" />
        <p class="card-paragraph">
          Large companies and governments both domestic (U.S.) and abroad,
          driven by necessities of cloud computing and policy, have collected exponentially increasing quantities
          of data. As data driven practices and data markets became mainstream, so too did exploitative corporate
          and government policies that decrease user control and increase provider control of user data; often
          achieving such goals by means of misdirection and deceit.
        </p>
      </div>
      <div class="card hidden">
        <h2 class="card-title">Other security considerations.</h2>
        <img class="card-picture" src="@/assets/images/local-network.svg" />
        <p class="card-paragraph">
          It may seem counter intuitive, but by making source code public, one can utilize work from passionate
          contributors over time to meet security threats with new and tested solutions iteratively and dynamically.
          Also, open source projects converge to their most robust state in general due simply to the enhancement of
          the strengths of iterative collaborative development driven by user and professional feedback. The enhancement
          of this process is because open source increases the pool of people willing and eligible to help.
        </p>
      </div>
      <div class="card hidden">
        <h2 class="card-title">Innovative machine learning techniques.</h2>
        <img class="card-picture" src="@/assets/images/ai.svg" />
        <p class="card-paragraph">
          Using the Secure Suite browser extension, MalURLNet receives URL traffic before user navigation, and predicts
          whether or not that URL is malicious. MalURLNet uses the latest in URL classification and machine learning to
          discourage traffic to fishy links that may try to steal user secrets. MalURLNet is a hybrid CNN-LSTM base network
          with traditional dense components, and makes sense of the relationships in unstructured and structured URL data.
        </p>
      </div>
      <div class="card hidden">
        <h2 class="card-title">Enterprise cloud secrets management solutions.</h2>
        <img class="card-picture" src="@/assets/images/enterprise.svg" />
        <p class="card-paragraph">
          Everything in the open source project is obviously free to use but is meant for personal and amatuer use.
          For enterprises robust authorization based secrets management and sharing solutions from Secure Suite are available,
          but these are paid services. Enterprise machine learning data and network security applications are in development to
          bolster existing security measures with increased observational capacity using network traffic analysis techniques.
        </p>
      </div>
    </div>
    <footer>
      <div>
        Website by
        <a href="https://haney-oliver.github.io">Oliver Haney</a>
      </div>
    </footer>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";

export default {
  components: {
    navbar: Navbar
  },
  data() {
    return {};
  },
  methods: {
    listenForScroll() {
      var elements;
      var windowHeight;
      function init() {
        elements = document.querySelectorAll(".hidden");
        windowHeight = window.innerHeight;
      }
      function checkPosition() {
        elements.forEach(element => {
          if (element.getBoundingClientRect().top - windowHeight < 0) {
            element.classList.add("fade-in-element");
            element.classList.remove("hidden");
          }
        });
      }
      window.addEventListener("scroll", checkPosition);
      window.addEventListener("resize", init);

      init();
      checkPosition();
    }
  },
  mounted() {
    this.listenForScroll();
  }
};
</script>

<style scoped lang="scss">
@import "@/assets/scss/home-view.scss";
@import "@/assets/scss/_animations.scss";
</style>