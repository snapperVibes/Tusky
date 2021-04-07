<template>
    <div class="editor">
        <QuizEditor/>
    </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import QuizEditor from "@/components/QuizEditor.vue";

@Options({
    components: {
        QuizEditor,
    },
})
export default class Editor extends Vue {}
</script>

<style scoped></style>
