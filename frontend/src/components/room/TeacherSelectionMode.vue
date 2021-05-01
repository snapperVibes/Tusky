<template>
  <div class="selection-mode">
    <CreateQuiz :auth-token="authToken"></CreateQuiz>
    <div class="my-own-quizzes-menu">
      <h2>My Quizzes</h2>
      <ul class="my-quizzes" v-if="quizzes">
        <li v-for="quiz in quizzes" :key="quiz.id">
          <QuizPreview :name="quiz.name" :id="quiz.id" />
        </li>
      </ul>
      <!--Todo: Add quiz creation button-->
      <h3 v-else>You haven't made any quizzes yet. Create one now?</h3>
    </div>
  </div>
</template>

<script>
import QuizPreview from "@/components/room/quiz/QuizPreview";
import CreateQuiz from "@/components/forms/CreateQuiz";
import jwt_decode from "jwt-decode";
import { quizzesApi } from "@/api";

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
};
</script>

<style scoped></style>
