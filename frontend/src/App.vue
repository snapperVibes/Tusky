<template>
  <div id="app">
    <v-app>
      <v-content>
      </v-content>

    </v-app>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

// import { readIsLoggedIn } from "@store/main/getters"
import { readIsLoggedIn } from "./store/main/getters";

export default class App extends Vue {
  get loggedIn() {
    return readIsLoggedIn(this.$store);
  }
}
</script>

<style scoped>

</style>
