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
          @startQuiz="onStartQuiz"
        />
      </template>
      <template #fallback> {{ loadingMsg("selection mode") }}</template>
    </Suspense>
    <Suspense v-if="mode === 'quiz-edit'">
      <template #default>
        <QuizEditor
          v-model:quizInfo="quizInfo"
          :auth-token="authToken"
          @toSelectionMode="onToSelectionMode"
        />
      </template>
      <template #fallback> {{ loadingMsg("quiz editor") }} </template>
    </Suspense>
    <Suspense v-if="mode === 'quiz-session'">
      <template #default>
        <div>
          <h2>The room is now open for students!</h2>
          <p>http://localhost:8000/{{ roomInfo.code }}</p>
          <TeacherQuizSession
            @toSelectionMode="onToSelectionMode"
            :room-info="roomInfo"
            :quiz-id="quizId"
            :auth-token="authToken"
          />
        </div>
      </template>
      <template #fallback>
        {{ loadingMsg("quiz session") }}
      </template>
    </Suspense>
  </div>
</template>

<script>
import jwt_decode from "jwt-decode";
import { quizzesApi } from "@/api";
import TeacherSelectionMode from "@/components/TeacherSelectionMode";
import QuizEditor from "@/components/QuizEditor";
import TeacherQuizSession from "@/components/TeacherQuizSession";

export default {
  name: "TeacherRoom",
  props: {
    authToken: String,
    roomInfo: Object,
  },
  components: {
    TeacherSelectionMode,
    QuizEditor,
    TeacherQuizSession,
  },
  async setup(props) {
    const owner_id = jwt_decode(props.authToken).sub;
    const quizzes = (await quizzesApi.getQuizPreviewByUser(owner_id)).data;
    return {
      quizzes: quizzes,
      quizInfo: null,
      quizId: null, // Todo: QuizId should definitely just be quizInfo
    };
  },
  data() {
    return {
      mode: "selection", // Modes include "selection", "quiz-edit", and more to follow
    };
  },
  methods: {
    loadingMsg: function (msg) {
      return `Loading ${msg}... if this takes more than a couple seconds, something went wrong.`;
    },
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
    onStartQuiz: async function (quizId) {
      this.mode = "quiz-session";
      this.quizId = quizId;
    },
    onToSelectionMode: function () {
      this.mode = "selection";
    },
  },
};
</script>

<style scoped></style>
