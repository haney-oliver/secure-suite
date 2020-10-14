<template>
  <span class="category-mini" @click="emitCategory()">
    <h3>{{ category.category_name }}</h3>
  </span>
</template>

<script>
import { EventBus } from "@/event-bus";
export default {
  props: {
    category: Object
  },
  methods: {
    emitCategory() {
      EventBus.$emit("category-clicked", this.category);
    },
  },
};
</script>

<style scoped>
@import "../../assets/scss/category-mini.scss";
</style>