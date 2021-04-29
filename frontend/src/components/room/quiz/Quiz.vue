<template>
  <div class="quiz">
    <h1>This is a quiz</h1>
    <h1>{{ title }}</h1>
    <ol class="questions">
      <li v-for="q in questions" :key="q" class="question__li">
        <Question />
      </li>
    </ol>
  </div>
</template>

<script>
import { Vue, Options } from "vue-class-component";
import Question from "@/components/room/quiz/question/Question";

@Options({
  components: {
    Question,
  },
})
export default class Quiz extends Vue {
  questions = 5;
  computed = mapState({});
}
</script>

<style scoped></style>
