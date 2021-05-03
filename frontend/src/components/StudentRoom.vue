<template>
  <div class="student-room">Student View {{ authToken }}</div>
</template>

<script>
export default {
  name: "StudentRoom",
  props: {
    authTokenProp: String,
  },
  data() {
    return {
      authToken: this.authTokenProp,
    };
  },
};
</script>

<style scoped></style>
