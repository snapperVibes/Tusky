<template>
    <h1>{{ quiz.name }}</h1>
    <ol>
        <li v-for="q in questions" :key="q">
            {{ q.query }}
        </li>
    </ol>
</template>

<script>
import { Vue } from "vue-class-component";
import { api } from "@/api";

let _quiz = api.getQuiz("Admin#0000", "Example Quiz");

export default class QuizEditor extends Vue {
    quiz = _quiz.then((res) => (this.quiz = res.data));
    questions = _quiz.then(
        (res) =>
            (this.questions = api
                .getQuestions(res.data.id)
                .then((res) => (this.questions = res.data)))
    );
}
</script>
