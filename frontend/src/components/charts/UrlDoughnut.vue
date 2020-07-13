<script>
import { Doughnut } from "vue-chartjs";

export default {
  extends: Doughnut,
  props: {
    chartdata: Object
  },
  data() {
    return {
      options: {
        cutoutPercentage: 90
      }
    };
  },
  watch: {
    chartdata: {
      immediate: true,
      deep: true,
      handler() {
        this.renderChart(this.chartdata, this.options);
      }
    }
  }
};
</script>

<style>
@import "../../assets/scss/doughnut-chart.scss";
</style>
