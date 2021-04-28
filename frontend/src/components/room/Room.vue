<template>
  <h1>Room</h1>
  <Quiz />
</template>

<script>
import { Options, Vue } from "vue-class-component";
import Quiz from "@/components/room/quiz/Quiz";

@Options({
  components: {
    Quiz,
  },
})
export default class Room extends Vue {}
</script>

<style scoped></style>
