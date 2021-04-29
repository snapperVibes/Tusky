<template>
  <div class="home">
    <HomePage />
  </div>
</template>

<script lang="ts">
import HomePage from "../components/HomePage.vue"; // @ is an alias to /src

export default {
  name: "Home",
  components: {
    HomePage,
  },
};
</script>
