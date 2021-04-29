<template>
  <Room :roomcode="roomcode" />
  <!--  <Room :roomcode="roomcode" />-->
</template>

<script>
import Room from "@/components/room/Room";

export default {
  name: "RoomView",
  components: {
    Room,
  },
  props: {
    roomcode: String,
  },
};
</script>

<style scoped></style>
