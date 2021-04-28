<template>
  <div class="home">
    <HomePage />
  </div>
</template>

<script lang="ts">
import HomePage from "../components/HomePage.vue"; // @ is an alias to /src
import { Options, Vue } from "vue-class-component";

@Options({
  components: {
    HomePage,
  },
})
export default class Home extends Vue {}
</script>
