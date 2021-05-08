<template>
  <div class="quiz-editor">
    <h2>Quiz Editor</h2>
    <div class="action-buttons">
      <ToSelectionMode @toSelectionMode="onToSelectionMode" />
    </div>
    <div class="editable-quiz">
      <!--QUIZ TITLE-->
      <div class="title edit-box">
        <h2>
          <EditableElement
            class="editable-title"
            v-model:text="editableInfo.title"
            @edit="onEditTitle(editableInfo)"
          />
        </h2>
      </div>
    </div>
    <!--QUIZ QUESTIONS-->
    <div class="questions">
      <ol class="ol__questions">
        <li v-for="question in editableInfo.questions" :key="question.id">
          <div class="edit-box">
            <EditableElement
              class="editable-question"
              v-model:text="question.query"
              @edit="onEditQuestion(question)"
            >
            </EditableElement>
            <EditableElementToolbar
              class="question-toolbar"
              placeholder="Example question"
              @delete="onDeleteQuestion(question.id)"
              @add="onAddQuestion"
            />
          </div>
          <!--QUESTION ANSWERS-->
          <ol class="ol__answers">
            <li v-for="answer in question.answers" :key="answer.id">
              <div class="edit-box">
                <EditableElement
                  class="editable-answer"
                  v-model:text="answer.text"
                  @edit="onEditAnswer(answer)"
                >
                </EditableElement>
                <EditableElementToolbar
                  class="answer-toolbar"
                  placeholder="Example answer"
                  @delete="onDeleteAnswer(answer.id)"
                  @add="onAddAnswer"
                />
              </div>
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
import EditableElementToolbar from "@/components/EditableElementToolbar";
import { authHeaders, displayError, quizzesApi } from "@/api";

export default {
  name: "QuizEditor",
  components: {
    ToSelectionMode,
    EditableElement,
    EditableElementToolbar,
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
    onEditTitle: async function (quiz) {
      const authHeader = authHeaders(this.authToken);
      const response = await quizzesApi
        .updateQuiz({ id: quiz.id, title: quiz.title }, authHeader)
        .catch((err) => {
          displayError(err);
          return false;
        });
      if (!response) {
        return;
      }
      this.editableInfo = response.data;
      console.log("Title updated!");
    },
    onAddQuestion: async function (value) {
      console.log(value);
    },
    onAddAnswer: async function (value) {
      console.log(value);
    },
    onDeleteAnswer: async function (answerId) {
      const authHeader = authHeaders(this.authToken);
      const response = await quizzesApi
        .deleteAnswer(answerId, authHeader)
        .catch((err) => {
          displayError(err);
          return false;
        });
      if (!response) {
        return;
      }
      let questionIndex;
      let answerIndex;
      this.editableInfo.questions.some((q, _questionIndex) => {
        this.editableInfo.questions[_questionIndex].answers.some(
          (a, _answerIndex) => {
            if (a.id !== answerId) {
              return false;
            }
            questionIndex = _questionIndex;
            answerIndex = _answerIndex;
            return true;
          }
        );
        return !(!answerIndex || answerIndex === 0);
      });
      this.editableInfo.questions[questionIndex].answers.splice(answerIndex, 1);
      this.$forceUpdate();
      console.log("Deleted answer!");
      // Change the next answer's previous answer

      if (
        typeof this.editableInfo.questions[questionIndex].answers[
          answerIndex
        ] === "undefined"
      ) {
        return;
      }
      let nextAnswer = this.editableInfo.questions[questionIndex].answers[
        answerIndex
      ];
      if (answerIndex === 0) {
        nextAnswer.previous_answer = null;
        return;
      }
      nextAnswer.previous_answer = this.editableInfo.questions[
        questionIndex
      ].answers[answerIndex - 1].id;
    },
    onEditQuestion: async function (question) {
      const authHeader = authHeaders(this.authToken);
      question = (
        await quizzesApi.updateQuestion(
          { id: question.id, query: question.query },
          authHeader
        )
      ).data;
      console.log("Question updated");
    },
    onEditAnswer: async function (answer) {
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
.edit-box {
  display: flex;
  flex: 1;
  flex-direction: row;
}
</style>
