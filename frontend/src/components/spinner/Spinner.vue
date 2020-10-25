<template>
  <div class="spinner">
    <fulfilling-square-spinner
      :animation-duration="4000"
      :size="50"
      :color="'#5381ff'"
    />
  </div>
</template>

<script>
import {FulfillingSquareSpinner} from 'epic-spinners'

export default {
  components: {
    FulfillingSquareSpinner
  },
}

</script>

<style scoped>
@import "../../assets/scss/spinner.scss";
</style>