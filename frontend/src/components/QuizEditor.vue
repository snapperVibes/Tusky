<template>
  <div class="quiz-editor">
    <h2>Quiz Editor</h2>
    <div class="🙁">
      <h3>Bug alert 🐛!</h3>
      Only the last plus button and first-and-last trash button of each answer
      group works (with similar logic on Question actions). The reason for this
      is known and will be fixed before it is deployed publicly. Polishing bugs
      out is not crucial to having a working demo.
    </div>
    <div class="action-buttons">
      <ToSelectionMode @toSelectionMode="onToSelectionMode" />
    </div>
    <div class="editable-quiz">
      <!--QUIZ TITLE-->
      <div class="title tusky__edit-box">
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
        <li
          v-for="(question, questionIndex) in editableInfo.questions"
          :key="question.id"
        >
          <div class="tusky__edit-box">
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
              @add="onAddQuestion($event, questionIndex)"
            />
          </div>
          <!--QUESTION ANSWERS-->
          <ol class="tusky__answers">
            <li
              v-for="(answer, answerIndex) in question.answers"
              :key="answer.id"
            >
              <div class="tusky__edit-box">
                <CorrectAnswerMarker
                  v-model:is_correct="answer.is_correct"
                  @change="onEditAnswer(answer)"
                />

                <EditableElement
                  class="editable-answer"
                  v-model:text="answer.text"
                  @edit="onEditAnswer(answer)"
                />
                <EditableElementToolbar
                  class="answer-toolbar"
                  placeholder="Example answer"
                  @delete="onDeleteAnswer(answer.id)"
                  @add="onAddAnswer($event, questionIndex, answerIndex)"
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
import CorrectAnswerMarker from "@/components/CorrectAnswerMarker";
import { authHeaders, displayError, quizzesApi } from "@/api";

export default {
  name: "QuizEditor",
  components: {
    ToSelectionMode,
    EditableElement,
    EditableElementToolbar,
    CorrectAnswerMarker,
  },
  props: {
    quizInfo: Object,
    authToken: String,
  },
  data() {
    let editableInfo = Object.assign({}, this.quizInfo);
    return {
      editableInfo,
    };
  },
  // Todo: The methods could save a lot of repeated code if they were written in a functional manner
  // Todo: I found out about passing $event after writing a lot of now useless code; Replace lumpy code with $event
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
    onAddQuestion: async function (query, questionIndex) {
      let previous_question_id;
      const authHeader = authHeaders(this.authToken);

      previous_question_id = this.editableInfo.questions[questionIndex].id;

      const response = await quizzesApi
        .createQuestion(
          {
            previous_question: previous_question_id,
            query: query,
            quiz_id: this.editableInfo.id,
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
      this.editableInfo.questions.splice(questionIndex + 1, 0, response.data);
      try {
        this.editableInfo.questions[questionIndex + 2].previous_question =
          response.data.id;
      } catch (e) {
        if (e instanceof TypeError) {
          // pass
          // This is expected behavior: The question was added as the last element
        }
      }
      this.$forceUpdate();
      console.log("Created question!");

      // Add default answer
      const response2 = await quizzesApi.createAnswer(
        {
          text: "Example answer",
          question_id: response.data.id,
          previous_answer: null,
          is_correct: false,
        },
        authHeader
      );
      this.editableInfo.questions[questionIndex + 1].answers.push(
        response2.data
      );
    },
    onDeleteQuestion: async function (questionId) {
      const authHeader = authHeaders(this.authToken);
      const response = await quizzesApi
        .deleteQuestion(questionId, authHeader)
        .catch((err) => {
          displayError(err);
          return false;
        });
      if (!response) {
        return;
      }
      let questionIndex;
      this.editableInfo.questions.some((q, _questionIndex) => {
        if (q.id !== questionId) {
          return false;
        }
        questionIndex = _questionIndex;
        return true;
      });
      this.editableInfo.questions.splice(questionIndex, 1);
      this.$forceUpdate();
      console.log("Deleted question!");
      // Change the next answer's previous answer
      if (typeof this.editableInfo.questions[questionIndex] === "undefined") {
        return;
      }
      let nextQuestion = this.editableInfo.questions[questionIndex];
      if (questionIndex === 0) {
        nextQuestion.previous_question = null;
        return;
      }
      nextQuestion.previous_question = this.editableInfo.questions[
        questionIndex
      ].id;
    },
    onAddAnswer: async function (eventText, questionIndex, answerIndex) {
      const authHeader = authHeaders(this.authToken);
      const q = this.editableInfo.questions[questionIndex];
      const previousAnswer = q.answers[answerIndex];
      const response = await quizzesApi
        .createAnswer(
          {
            text: eventText,
            question_id: q.id,
            previous_answer: previousAnswer.id,
            is_correct: false,
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
      q.answers.splice(answerIndex + 1, 0, response.data);
      try {
        q.answers[answerIndex + 2].previous_answer = response.data.id;
      } catch (err) {
        if (!(err instanceof TypeError)) {
          throw err;
        }
      }
      this.$forceUpdate();
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
        q.answers.some((a, _answerIndex) => {
          if (a.id !== answerId) {
            return false;
          }
          questionIndex = _questionIndex;
          answerIndex = _answerIndex;
          return true;
        });
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
          { id: answer.id, text: answer.text, is_correct: answer.is_correct },
          authHeader
        )
      ).data;
      console.log("Answer updated");
    },
  },
  emits: ["toSelectionMode"],
};
</script>

<style scoped></style>
