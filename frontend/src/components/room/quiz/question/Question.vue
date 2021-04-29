<template>
  <div class="question">
    <span class="query">This is a question</span>
    <ol class="answers">
      <li v-for="a in answers" :key="a">
        <MultipleChoice />
      </li>
    </ol>
  </div>
</template>

<script>
import MultipleChoice from "@/components/room/quiz/question/answer/MultipleChoice";
import { Vue, Options } from "vue-class-component";

@Options({
  components: {
    MultipleChoice,
  },
})
export default class Question extends Vue {
  answers = 4;
}
</script>

<style scoped></style>
