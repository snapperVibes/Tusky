<template>
  <div class="quiz-editor">
    <h2>Quiz Editor</h2>
    <ToSelectionMode @toSelectionMode="onToSelectionMode" />
    <h2><EditableElement class="quiz-title" :text="quizInfo.name" /></h2>
    <EditableQuestion
      v-for="question in quizInfo.questions"
      :key="question.id"
      :questionInfo="question"
      @elementUpdate="onElementUpdate"
    />
    {{ quizInfo }}
  </div>
</template>

<script>
import EditableElement from "@/components/EditableElement";
import ToSelectionMode from "@/components/ToSelectionMode";
import EditableQuestion from "@/components/EditableQuestion";

export default {
  name: "QuizEditor",
  components: {
    EditableQuestion,
    ToSelectionMode,
    EditableElement,
  },
  props: {
    quizInfo: Object,
  },
  methods: {
    onToSelectionMode: function () {
      this.$emit("toSelectionMode");
    },
  },
  emits: ["toSelectionMode"],
};
</script>

<style scoped></style>
