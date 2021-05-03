<template>
  <form>
    <fieldset :disabled="!authToken">
      <legend>Enter Room</legend>
      <label for="room-code"></label>
      <input
        type="text"
        placeholder="Room code"
        id="room-code"
        v-model="roomCodeInput"
      />
      <br />
      <input
        @click.prevent="enterRoom"
        class="button"
        type="submit"
        value="Enter Room"
      />
      <span class="tusky__disabled-explanation" v-show="!authToken">
        Log in to enter a room.
      </span>
    </fieldset>
  </form>
</template>

<script>
import { Vue } from "vue-class-component";
import { roomsApi, authHeaders, displayError } from "@/api";
import jwt_decode from "jwt-decode";

export default {
  name: "EnterRoom",
  data() {
    return {
      roomCodeInput: null,
    };
  },
  methods: {
    enterRoom: async function (clickEvent) {
      const frozenRoomCode = this.roomCodeInput;
      const err = this._validate_input(frozenRoomCode);
      if (err) {
        alert(err);
        return;
      }
      await this._enterRoom(frozenRoomCode);
    },
    _enterRoom: async function (roomcode) {
      const authHeader = authHeaders(this.authToken);
      const response = await roomsApi
        .getRoomByCode(this.roomCodeInput, authHeader)
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
    _validate_input(roomcode) {
      if (!roomcode) {
        return `The roomcode field must be filled out to log in to enter a room.`;
      }
    },
  },
  props: {
    authToken: String,
  },
};
</script>

<style scoped></style>
