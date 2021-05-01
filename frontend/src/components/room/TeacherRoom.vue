<template>
  <div class="teacher-room">
    <Suspense v-show="mode === 'selection'">
      <template #default>
        <TeacherSelectionMode
          :auth-token="authToken"
          :room-info="roomInfo"
          @quizCreated="onQuizCreated"
        />
      </template>
      <template #fallback> Loading selection mode </template>
    </Suspense>
  </div>
</template>

<script>
import jwt_decode from "jwt-decode";
import { quizzesApi } from "@/api";
import TeacherSelectionMode from "@/components/room/TeacherSelectionMode";

export default {
  name: "TeacherRoom",
  props: {
    authToken: String,
    roomInfo: Object,
  },
  components: {
    TeacherSelectionMode,
  },
  async setup(props) {
    const owner_id = jwt_decode(props.authToken).sub;
    const quizzes = (await quizzesApi.getQuizPreviewByUser(owner_id)).data;
    return {
      quizzes: quizzes,
      mode: "selection", // Modes include "selection", "quiz-edit", and more to follow
      quizInfo: null,
    };
  },
  methods: {
    onQuizCreated: function (quizInfo) {
      this.mode = "quiz-edit";
      this.quizInfo = quizInfo;
    },
  },
};
</script>

<style scoped></style>
