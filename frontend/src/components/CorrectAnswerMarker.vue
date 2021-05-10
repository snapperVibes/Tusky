<template>
  <label>
    <input
      title="Check box if the answer is correct"
      type="checkbox"
      :checked="is_correct"
    />
  </label>
</template>

<script>
export default {
  name: "CorrectAnswerMarker",
  props: ["is_correct"],
};
</script>

<style scoped></style>
