<template>
  <form>
    <fieldset>
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
    </fieldset>
  </form>
</template>

<script>
import { Vue } from "vue-class-component";

export default class EnterRoom extends Vue {
  roomCodeInput = null;

  enterRoom(clickEvent) {
    console.log("Enter Room", this.roomCodeInput);
  }
}
</script>

<style scoped></style>
