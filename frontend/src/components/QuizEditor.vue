<template>
  <div class="quiz-editor">
    <h2>Quiz Editor</h2>
    <div class="action-buttons">
      <ToSelectionMode @toSelectionMode="onToSelectionMode" />
    </div>
    <div class="editable-quiz">
      <!--QUIZ TITLE-->
      <div class="title">
        <h2>
          <EditableElement
            class="editable-title"
            v-model:text="editableInfo.title"
            @edited="onEditedTitle(this.editableInfo)"
          />
        </h2>
      </div>
    </div>
    <!--QUIZ QUESTIONS-->
    <div class="questions">
      <ol class="ol__questions">
        <li v-for="question in editableInfo.questions" :key="question.id">
          <EditableElement
            class="editable-question"
            v-model:text="question.query"
            @edited="onEditedQuestion(question)"
          />
          <!--QUESTION ANSWERS-->
          <ol class="ol__answers">
            <li v-for="answer in question.answers" :key="answer.id">
              <EditableElement
                class="editable-answer"
                v-model:text="answer.text"
                @edited="onEditedAnswer(answer)"
              />
            </li>
          </ol>
        </li>
      </ol>
    </div>
  </div>
  {{ editableInfo }}
</template>

<script>
import ToSelectionMode from "@/components/ToSelectionMode";
import EditableElement from "@/components/EditableElement";
import { authHeaders, quizzesApi } from "@/api";

export default {
  name: "QuizEditor",
  components: {
    ToSelectionMode,
    EditableElement,
  },
  props: {
    quizInfo: Object,
    authToken: String,
  },
  data() {
    let editableInfo = Object.assign({}, this.quizInfo);
    return {
      editableInfo,
      exitWithoutSaving: false,
    };
  },
  // Todo: The methods could save a lot of repeated code if they were written in a functional manner
  methods: {
    onToSelectionMode: function () {
      this.$emit("toSelectionMode");
    },
    onEditedTitle: async function (quiz) {
      const authHeader = authHeaders(this.authToken);
      this.editableInfo = (
        await quizzesApi.updateQuiz(
          { id: quiz.id, title: quiz.title },
          authHeader
        )
      ).data;
      console.log("Title updated!");
    },
    onEditedQuestion: async function (question) {
      const authHeader = authHeaders(this.authToken);
      question = (
        await quizzesApi.updateQuestion(
          { id: question.id, query: question.query },
          authHeader
        )
      ).data;
      console.log("Question updated");
    },
    onEditedAnswer: async function (answer) {
      const authHeader = authHeaders(this.authToken);
      answer = (
        await quizzesApi.updateAnswer(
          { id: answer.id, text: answer.text },
          authHeader
        )
      ).data;
      console.log("Answer updated");
    },
  },
  emits: ["toSelectionMode"],
};
</script>

<style scoped>
ol.ol__answers {
  list-style-type: lower-alpha;
}
</style>
