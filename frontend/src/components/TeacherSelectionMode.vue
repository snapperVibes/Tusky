<template>
  <div class="selection-mode">
    <CreateQuiz :auth-token="authToken" @createQuiz="onCreateQuiz" />
    <div class="my-own-quizzes-menu">
      <h2>My Quizzes</h2>
      <ul class="my-quizzes" v-if="quizzes.length !== 0">
        <li v-for="quiz in quizzes" :key="quiz.id">
          <QuizPreview
            :title="quiz.title"
            :quiz-id="quiz.id"
            :auth-token="authToken"
            @seeQuiz="onSeeQuiz"
            @editQuiz="onEditQuiz"
            @deleteQuiz="onDeleteQuiz"
            @startQuiz="onStartQuiz"
          />
        </li>
      </ul>
      <!--Todo: Add quiz creation button-->
      <h3 v-else>You haven't made any quizzes yet. Create one now?</h3>
    </div>
  </div>
</template>

<script>
import QuizPreview from "@/components/QuizPreview";
import CreateQuiz from "@/components/CreateQuiz";
import jwt_decode from "jwt-decode";
import { authHeaders, displayError, quizzesApi } from "@/api";

export default {
  name: "TeacherSelectionMode",
  components: { QuizPreview, CreateQuiz },
  props: {
    authToken: String,
    roomInfo: Object,
  },
  async setup(props) {
    const owner_id = jwt_decode(props.authToken).sub;
    const quizzes = (await quizzesApi.getQuizPreviewByUser(owner_id)).data;
    return {
      quizzes: quizzes,
    };
  },
  emits: ["createQuiz", "seeQuiz", "editQuiz", "startQuiz"],

  methods: {
    onCreateQuiz: function (quizInfo) {
      this.$emit("createQuiz", quizInfo);
    },
    onSeeQuiz: function (quizId) {
      this.$emit("seeQuiz", quizId);
    },
    onEditQuiz: function (quizInfo) {
      this.$emit("editQuiz", quizInfo);
    },
    onDeleteQuiz: async function (quizId) {
      const authHeader = authHeaders(this.authToken);
      const response = await quizzesApi
        .deleteQuiz(quizId, authHeader)
        .catch((err) => {
          displayError(err);
          return false;
        });
      if (!response) {
        return;
      }
      const indexToDelete = this.quizzes.some((q, index) => {
        if (q.id !== quizId) {
          return false;
        }
        return index;
      });
      this.quizzes.splice(indexToDelete, 1);
      this.$forceUpdate();
      alert("Deleted");
      return true;
    },
    onStartQuiz: function (quizId) {
      this.$emit("startQuiz", quizId);
    },
  },
};
</script>

<style scoped></style>
