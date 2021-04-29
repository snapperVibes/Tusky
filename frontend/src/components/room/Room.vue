<template>
  <div class="room">
    <h1>Room {{ roomcode }}</h1>
    <!--    <Quiz />-->
  </div>
</template>

<script>
// import Quiz from "@/components/room/quiz/Quiz";

export default {
  props: {
    roomcode: String,
  },
  //   components: {
  //     Quiz,
  //   },
};
</script>

<style scoped></style>
