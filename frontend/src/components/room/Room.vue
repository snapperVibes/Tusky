<template>
  <div class="room">
    <!--  Todo: There's definitely a better place to ensure uppercase. Put uppercase logic somewhere else-->
    <h1>Room {{ roomcode.toUpperCase() }}</h1>
    <!--    <Quiz />-->
  </div>
</template>

<script>
import { toRef, toRefs } from "vue";
import { roomsApi, authHeaders } from "@/api";
// import Quiz from "@/components/room/quiz/Quiz";

export default {
  props: {
    roomcode: String,
    x: String,
  },
  async setup(props) {
    const roomInfo = await roomsApi.getRoomByCode(props.roomcode);
    console.log(roomInfo);
  },
  //   components: {
  //     Quiz,
  //   },
};
</script>

<style scoped></style>
