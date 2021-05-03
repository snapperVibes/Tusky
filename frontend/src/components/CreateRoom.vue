<template>
  <form>
    <fieldset :disabled="!authToken">
      <legend>Create Room</legend>
      <input
        @click.prevent="createRoom"
        class="button"
        type="submit"
        value="Create Room"
      />
      <span class="tusky__disabled-explanation" v-show="!authToken">
        Log in to create a room.
      </span>
    </fieldset>
  </form>
</template>

<script>
import { roomsApi, authHeaders, usersApi, displayError } from "@/api";

export default {
  name: "CreateRoom",

  methods: {
    createRoom: async function (clickEvent) {
      const authHeader = authHeaders(this.authToken);
      const response = await roomsApi
        .createRoom({ owner_id: this.ownerId }, authHeader)
        .catch((err) => {
          displayError(err);
          return false;
        });
      if (!response) {
        return;
      }
      const roomInfo = response.data;
      await this.$router.push({
        name: "Room",
        params: {
          roomCodeProp: roomInfo.code,
          roomInfoProp: JSON.stringify(roomInfo),
          authTokenProp: this.authToken,
        },
      });
    },
  },
  props: {
    ownerId: String,
    authToken: String,
  },
};
</script>

<style scoped></style>
