<template>
  <div class="quiz-preview">
    <h4>{{ title }}</h4>
    <span class="quiz-preview--options">
      <button
        class="quiz-preview__button start-quiz"
        @click.prevent="startQuiz"
      >
        Start Quiz Session
      </button>

      |
      <button class="quiz-preview__button edit-quiz" @click.prevent="editQuiz">
        Edit
      </button>
      |
      <button
        class="quiz-preview__button delete-quiz"
        @click.prevent="deleteQuiz"
      >
        Delete
      </button>
      |
      <button class="quiz-preview__button see-results" @click.prevent="seeQuiz">
        See Results
      </button>
    </span>
  </div>
</template>

<script>
import { authHeaders, displayError, quizzesApi } from "@/api";

export default {
  name: "QuizPreview",
  props: ["title", "quizId", "authToken"],
  emits: ["seeQuiz", "editQuiz", "deleteQuiz", "startQuiz"],

  methods: {
    seeQuiz: function () {
      this.$emit("seeQuiz", this.quizId);
    },
    editQuiz: async function () {
      const authHeader = authHeaders(this.authToken);
      const response = await quizzesApi
        .getQuiz(this.quizId, authHeader)
        .catch((err) => {
          displayError(err);
          return false;
        });
      if (!response) {
        return;
      }
      this.$emit("editQuiz", response.data);
    },
    deleteQuiz: function () {
      this.$emit("deleteQuiz", this.quizId);
      // Todo: this view breaks if it's the last quiz
    },
    startQuiz: function () {
      this.$emit("startQuiz", this.quizId);
    },
  },
};
</script>

<style scoped>
.quiz-preview__button {
  border: none;
  background: none;
}
.quiz-preview__button:hover {
  background: wheat;
}
</style>
