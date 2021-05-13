<template>
  <div class="student-room">
    <div class="quiz-for-student">
      <h2>{{ quizInfo.title }}</h2>
      <ol>
        <li v-for="question in quizInfo.questions" :key="question.id">
          {{ question.query }}
          <ol class="tusky__answers">
            <li v-for="answer in question.answers" :key="answer.id">
              <div class="tusky__edit-box">
                <CorrectAnswerMarker
                  v-model:is_correct="answer.is_correct"
                  @change="submitAnswer(answer)"
                />
                <span class="answer"> {{ answer.text }} </span>
              </div>
            </li>
          </ol>
        </li>
      </ol>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { authHeaders, quizzesApi, sessionsApi, displayError } from "@/api";
import CorrectAnswerMarker from "@/components/CorrectAnswerMarker";
import jwt_decode from "jwt-decode";

export default {
  name: "StudentRoom",
  components: { CorrectAnswerMarker },
  props: ["authToken", "roomInfo"],
  async setup(props) {
    // Get the quiz for the room's session
    // Let's make it in 1 get request later... and a layer up
    const authHeader = authHeaders(props.authToken);
    console.log(props);
    const session = ref(props.roomInfo.session[0]);
    const myId = jwt_decode(props.authToken).sub;

    const response = await quizzesApi
      .getQuizForStudent(session.value.quiz_id)
      .catch((err) => {
        return displayError(err);
      });
    if (!response) {
      return;
    }
    const quiz = response.data;
    // Last minute hack
    quiz.questions.forEach((q) => {
      q.answers.forEach((a) => {
        a.is_correct = false;
      });
    });
    return {
      session: session,
      quizInfo: response.data,
      myId: myId,
    };
  },
  methods: {
    submitAnswer: async function (answer) {
      const authHeader = authHeaders(this.authToken);
      const response = await sessionsApi
        .createStudentResponse(
          {
            quiz_session_id: this.session.id,
            student_id: this.myId,
            question_id: answer.question_id,
            is_correct: answer.is_correct,
          },
          authHeader
        )
        .catch((err) => {
          return displayError(err);
        });
    },
  },
};
</script>

<style scoped></style>
