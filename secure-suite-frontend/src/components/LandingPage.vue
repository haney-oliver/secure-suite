<template>
  <div class="index">
    <div class="banner"></div>
    <div class="navbar" id="navbar">
      <ul class="option">
        <li>
          <a href="#top">Home</a>
        </li>
        <li>
          <a href="#docs">Docs</a>
        </li>
        <li>
          <a href="#security">Security</a>
        </li>
        <li>
          <a href="#enterprise">Enterprise</a>
        </li>
        <li>
          <router-link to="/login">Login</router-link>
        </li>
        <li>
          <router-link to="/register">Register</router-link>
        </li>
      </ul>
    </div>
    <div class="container">
      <div class="grid">
        <article>
          <img src="../assets/images/vault.svg" />
          <h3>Store secure passwords</h3>
          <p>Generate and store categorized passwords in an encrypted database.</p>
        </article>
        <article>
          <img src="../assets/images/dropwizard.svg" />
          <h3>Dropwizard Backend</h3>
          <p>Modern Java Dropwizard server with intuitive gRPC interface.</p>
        </article>
        <article>
          <img src="../assets/images/encryption.svg" />
          <h3>End to end encryption</h3>
          <p>Encrypted data transfer.</p>
        </article>
        <article>
          <img src="../assets/images/open-source.svg" />
          <h3>Open source</h3>
          <p>Own your data.</p>
        </article>
        <article>
          <img src="../assets/images/report.svg" />
          <h3>Real time analytics</h3>
          <p>Understand your data.</p>
        </article>
        <article>
          <img src="../assets/images/vpn.svg" />
          <h3>Easy VPN setup</h3>
          <p>Connect to your internal network in one click.</p>
        </article>
      </div>
      <h2 id="security">Mitigating security vunlerabilities enabled by cloud computing.</h2>
      <div class="grid">
        <img class="articlePicture" src="../assets/images/cloud-security.svg" />
        <p class="articleParagraph">
          Large companies and governments both domestic (U.S.) and abroad,
          driven by necessities of cloud computing and policy, have collected exponentially increasing quantities
          of data. As data driven practices and data markets became mainstream, so too did exploitative corporate
          and government policies that decrease user control and increase provider control of user data; often
          achieving such goals by means of misdirection and deceit.
        </p>
      </div>
      <h2>Other security considerations.</h2>
      <div class="grid">
        <p class="articleParagraph">
          It may seem counter intuitive, but by making source code public, one can utilize work from passionate
          contributors over time to meet security threats with new and tested solutions iteratively and dynamically.
          Also, open source projects converge to their most robust state in general due simply to the enhancement of
          the strengths of iterative collaborative development driven by user and professional feedback. The enhancement
          of this process is because open source increases the pool of people willing and eligible to help.
        </p>
        <img class="articlePicture" src="../assets/images/local-network.svg" />
      </div>
      <h2>Innovative machine learning techniques.</h2>
      <div class="grid">
        <img class="articlePicture" src="../assets/images/ai.svg" />
        <p class="articleParagraph">
          Using the Secure Suite browser extension, MalURLNet receives URL traffic before user navigation, and predicts
          whether or not that URL is malicious. MalURLNet uses the latest in URL classification and machine learning to
          discourage traffic to fishy links that may try to steal user secrets. MalURLNet is a hybrid CNN-LSTM base network
          with traditional dense components, and makes sense of the relationships in unstructured and structured URL data.
        </p>
      </div>
      <h2>Enterprise cloud secrets management solutions.</h2>
      <div class="grid">
        <p class="articleParagraph">
          Everything in the open source project is obviously free to use but is meant for personal and amatuer use.
          For enterprises robust authorization based secrets management and sharing solutions from Secure Suite are available,
          but these are paid services. Enterprise machine learning data and network security applications are in development to
          bolster existing security measures with increased observational capacity using network traffic analysis techniques.
        </p>
        <img class="articlePicture" src="../assets/images/enterprise.svg" />
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
export default {
  name: "Index",
  data() {
    return {};
  },
  mounted() {
    window.onscroll = function() {
      myFunction();
    };

    var navbar = document.getElementById("navbar");

    var sticky = navbar.offsetTop;

    function myFunction() {
      if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky");
      } else {
        navbar.classList.remove("sticky");
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
