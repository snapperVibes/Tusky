<template>
  <form>
    <fieldset>
      <legend>Create Room</legend>
      <input
        @click.prevent="createRoom"
        class="button"
        type="submit"
        value="Create Room"
      />
    </fieldset>
  </form>
</template>

<script>
import { roomsApi } from "@/api";

export default {
  name: "CreateRoom",
  methods: {
    createRoom: function (clickEvent) {
      roomsApi.createRoom({}).then(function (res) {
        const room = res.data;
        window.location.href = `http://localhost:8080/room/${room.code}`;
      });
    },
  },
};
</script>

<style scoped></style>
