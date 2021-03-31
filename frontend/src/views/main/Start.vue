<template>
  <router-view></router-view>
</template>


<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
// import { store } from "@/store";
import { store } from "../../store";
import { readIsLoggedIn } from "../../store/main/getters";

export default {
  name: "Start",
};
</script>

<style scoped>

</style>
