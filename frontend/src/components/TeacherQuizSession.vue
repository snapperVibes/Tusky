<template>
  <button @click.prevent="endQuiz">END QUIZ</button>
  <p>This is the teacher quiz session view</p>
  {{ quizId }}
</template>

<script>
import { authHeaders, displayError, sessionsApi } from "@/api";

export default {
  name: "TeacherQuizSession",
  props: ["roomInfo", "quizId", "authToken"],
  emits: ["toSelectionMode"],
  async setup(props) {
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
  },
};
</script>

<style scoped></style>
