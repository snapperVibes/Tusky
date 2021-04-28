<template>
  <nav>
    <div id="nav-wrapper">
      This is the navbar
      <input type="button" @click="whoAmI" :value="username" />
    </div>
  </nav>
</template>

<script>
export default {
  props: {
    username: String,
  },
};
</script>

<style scoped></style>
