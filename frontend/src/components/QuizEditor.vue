<template>
  <div class="quiz-editor">
    <h2>Quiz Editor</h2>
    <div class="action-buttons">
      <ToSelectionMode @toSelectionMode="onToSelectionMode" />
      <SaveWork @saveWork="onSaveWork" />
    </div>
    <div class="editable-quiz">
      <!--QUIZ TITLE-->
      <div class="title">
        <h2>
          <EditableElement
            class="editable-title"
            v-model:text="editableInfo.name"
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
          />
          <!--QUESTION ANSWERS-->
          <ol class="ol__answers">
            <li v-for="answer in question.answers" :key="answer.id">
              <EditableElement
                class="editable-answer"
                v-model:text="answer.text"
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
import SaveWork from "@/components/SaveWork";
import { authHeaders, quizzesApi } from "@/api";

export default {
  name: "QuizEditor",
  components: {
    SaveWork,
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
  methods: {
    onToSelectionMode: function () {
      this.$emit("toSelectionMode");
    },
    onSaveWork: async function () {
      const authHeader = authHeaders(this.authToken);
      this.editableInfo = (
        await quizzesApi.updateQuiz(this.editableInfo, authHeader)
      ).data;
      console.log("After save", this.editableInfo);
      alert("Quiz saved");
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
