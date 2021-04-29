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
import { roomsApi, authHeaders, usersApi } from "@/api";

export default {
  name: "CreateRoom",
  methods: {
    createRoom: async function (clickEvent) {
      const authHeader = authHeaders(this.authToken);
      const response = await roomsApi.createRoom(
        { owner_id: this.ownerId },
        authHeader
      );
      const room = response.data;
      window.location.href = `http://localhost:8080/room/${room.code}`;
    },
  },
  props: {
    ownerId: String,
    authToken: String,
  },
};
</script>

<style scoped></style>
