<template>
  <div class="quiz-preview">
    <h4>{{ name }}</h4>
    <span class="quiz-preview--options">
      <span class="edit-quiz">See Results</span> |
      <span class="see-results">Edit</span> |
      <span class="delete-quiz">Delete</span>
    </span>
  </div>
</template>

<script>
export default {
  name: "QuizPreview",
  props: {
    name: String,
    id: String,
  },
};
</script>

<style scoped></style>
