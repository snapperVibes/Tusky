<template>
  <button @click.prevent="endQuiz">END QUIZ</button>
  <form @submit.prevent="dummyResponse">
    <label for="helloThere">
      <input ref="hello" id="helloThere" type="text" autocomplete="off" />
    </label>
    <button>Send</button>
    <ul v-for="response in responses" :key="response.id">
      <li>{{ response }}</li>
    </ul>
  </form>
</template>

<script>
import { authHeaders, displayError, sessionsApi } from "@/api";

export default {
  name: "TeacherQuizSession",
  props: ["roomInfo", "quizId", "authToken"],
  emits: ["toSelectionMode"],
  async setup(props, context) {
    const authHeader = authHeaders(props.authToken);
    const response = await sessionsApi
      .createSession(
        {
          room_id: props.roomInfo.id,
          quiz_id: props.quizId,
          is_active: true,
        },
        authHeader
      )
      .catch((err) => {
        return displayError(err);
      });
    if (!response) {
      return;
    }
    const session = response.data;
    return {
      session: session,
      authHeader: authHeader,
    };
  },
  data() {
    const ws = new WebSocket("ws://localhost:8000/session/get_responses");
    ws.onmessage = (event) => {
      this.responses.push(event.data);
    };
    return {
      ws: ws,
      responses: [],
    };
  },
  methods: {
    endQuiz: async function () {
      const confirmation = confirm("Are you sure you want to end the quiz?");
      if (!confirmation) {
        return;
      }
      const response = await sessionsApi
        .updateSession(
          {
            id: this.session.id,
            is_active: false,
          },
          this.authHeader
        )
        .catch((err) => {
          return displayError(err);
        });
      if (!response) {
        return;
      }
      this.$emit("toSelectionMode");
    },
    dummyResponse: async function (event) {
      var input = this.$refs.hello;
      this.ws.send(input.value);
      input.value = "";
    },
  },
};
</script>

<style scoped></style>
