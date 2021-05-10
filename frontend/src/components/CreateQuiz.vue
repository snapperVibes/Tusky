<template>
  <form autocomplete="off">
    <fieldset :disabled="!authToken">
      <legend>Create Quiz</legend>
      <label for="create-quiz-input"></label>
      <input
        type="text"
        placeholder="Quiz name"
        id="create-quiz-input"
        v-model="quizNameInput"
        required
      />
      <br />
      <input
        @click.prevent="createQuiz"
        class="button"
        type="submit"
        value="Create Quiz"
      />
      <span class="tusky__disabled-explanation" v-show="!authToken">
        Log in to create a quiz.
      </span>
    </fieldset>
  </form>
</template>

<script>
import { authHeaders, displayError, quizzesApi } from "@/api";
import jwt_decode from "jwt-decode";

export default {
  name: "CreateQuiz",
  props: {
    authToken: String,
  },
  data: function () {
    return {
      owner_id: jwt_decode(this.authToken).sub,
      quizNameInput: null,
    };
  },
  emits: ["createQuiz"],

  methods: {
    createQuiz: async function (clickEvent) {
      const frozenQuizName = this.quizNameInput;
      const err = this._validate_input(frozenQuizName);
      if (err) {
        alert(err);
        return;
      }
      const authHeader = authHeaders(this.authToken);
      const response = await quizzesApi
        .createQuiz(
          {
            title: frozenQuizName,
            owner_id: this.owner_id,
          },
          authHeader
        )
        .catch((err) => {
          displayError(err);
          return false;
        });
      if (!response) {
        return;
      }
      const response2 = await quizzesApi
        .createQuestion(
          {
            query: "Example question",
            quiz_id: response.data.id,
            previous_question: null,
          },
          authHeader
        )
        .catch((err) => {
          displayError(err);
          return false;
        });
      if (!response2) {
        return;
      }
      const response3 = await quizzesApi
        .createAnswer(
          {
            text: "Example answer",
            question_id: response2.data.id,
            previous_answer: null,
          },
          authHeader
        )
        .catch((err) => {
          displayError(err);
          return false;
        });
      if (!response2) {
        return;
      }
      const quiz = response.data;
      quiz.questions.push(response2.data);
      quiz.questions[0].answers.push(response3.data);
      this.$emit("createQuiz", quiz);
    },
    _validate_input(quizName) {
      if (!quizName) {
        return `Quiz name field must be filled out to log in to create a quiz.`;
      }
    },
  },
};
</script>

<style scoped></style>
