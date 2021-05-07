<template>
  <div class="teacher-room">
    <Suspense v-if="mode === 'selection'">
      <template #default>
        <TeacherSelectionMode
          :auth-token="authToken"
          :room-info="roomInfo"
          @createQuiz="onCreateQuiz"
          @seeQuiz="onSeeQuiz"
          @editQuiz="onEditQuiz"
        />
      </template>
      <template #fallback> Loading selection mode... </template>
    </Suspense>
    <Suspense v-if="mode === 'quiz-edit'">
      <template #default>
        <QuizEditor
          v-model:quizInfo="quizInfo"
          :auth-token="authToken"
          @toSelectionMode="onToSelectionMode"
        />
      </template>
      <template #fallback> Loading quiz editor... </template>
    </Suspense>
  </div>
</template>

<script>
import jwt_decode from "jwt-decode";
import { quizzesApi } from "@/api";
import TeacherSelectionMode from "@/components/TeacherSelectionMode";
import QuizEditor from "@/components/QuizEditor";

export default {
  name: "TeacherRoom",
  props: {
    authToken: String,
    roomInfo: Object,
  },
  components: {
    TeacherSelectionMode,
    QuizEditor,
  },
  async setup(props) {
    const owner_id = jwt_decode(props.authToken).sub;
    const quizzes = (await quizzesApi.getQuizPreviewByUser(owner_id)).data;
    return {
      quizzes: quizzes,
      quizInfo: null,
    };
  },
  data() {
    return {
      mode: "selection", // Modes include "selection", "quiz-edit", and more to follow
    };
  },
  methods: {
    onCreateQuiz: function (quizInfo) {
      this.mode = "quiz-edit";
      this.quizInfo = quizInfo;
    },
    onSeeQuiz: function (quizId) {
      alert("Not implamented yet.");
    },
    onEditQuiz: async function (quizInfo) {
      this.mode = "quiz-edit";
      this.quizInfo = quizInfo;
    },
    onToSelectionMode: function () {
      this.mode = "selection";
    },
  },
};
</script>

<style scoped></style>
