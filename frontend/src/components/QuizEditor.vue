<template>
  <!--  TODO: Documentation: For an element to be editable, the element must be wrapped in a div. The div must contain 2 child elements; The second must be an label-->
  <div class="quiz">
    <div
      class="quiz__div_quiz-name"
      v-bind:id="'quiz_' + quiz.id"
      v-on:dblclick="editElement"
    >
      <h1 class="quiz__div_quiz-name_h1" v-html="quiz.name"></h1>
      <label hidden>
        ok
        <input
          class="quiz__div_quiz-name_input text-editor"
          type="text"
          v-on:keyup.enter="setText"
        />
      </label>
    </div>
    <!-- Question List -->
    <ol class="quiz__ol_question-list">
      <li v-for="q in quiz.questions" :key="q" class="quiz__li_question">
        <div
          class="quiz__div_query"
          v-bind:id="'query_' + q.id"
          v-on:dblclick="editElement"
        >
          <span class="quiz__div_query_span">
            {{ q.query }}
          </span>
          <label hidden>
            <input
              type="text"
              class="quiz__div_query_input text-editor"
              v-on:keyup.enter="setText"
            />
          </label>
        </div>
        <!-- Answer List (per question) -->
        <ol class="quiz__ol_answer-list">
          <li v-for="a in q.answers" :key="a" class="quiz__li_answer">
            <div
              class="quiz__div_answer"
              v-bind:id="'answer_' + a.id"
              v-on:dblclick="editElement"
            >
              <span class="quiz__div_answer_text">
                {{ a.text }}
              </span>
              <label hidden>
                <input
                  type="text"
                  class="quiz__div_answer_input text-editor"
                  v-on:keyup.enter="setText"
                />
              </label>
            </div>
          </li>
        </ol>
      </li>
    </ol>
  </div>
</template>

<script>
import { Vue } from "vue-class-component";
import { api } from "@/api";

let _quiz = api.getQuiz("Admin#0000", "Example Quiz");

function getElementPK(element) {
  let splitId = element.id.split("_");
  return splitId[splitId.length - 1];
}

export default class QuizEditor extends Vue {
  // Todo: Order answers: This should happen at the API level
  quiz = _quiz.then((res) => (this.quiz = res.data));
  editElement(dblclickEvent) {
    // Todo: This selector feels un-idiomatic. What's the Vue way to do this?
    let element = dblclickEvent.target;
    let parent = element.parentElement;
    let textElement = parent.firstElementChild;
    if (element !== textElement) {
      alert("Something went wrong");
    }
    let labelElement = parent.lastElementChild;
    let inputElement = labelElement.firstElementChild;

    textElement.setAttribute("hidden", "true");
    labelElement.removeAttribute("hidden");
    inputElement.focus();
  }
  setText(keyupEvent) {
    // Allow multiple-lines if the user holds the control-key
    if (keyupEvent.ctrlKey) {
      return;
    }
    // The first parent is the label. The second parent is the div
    let parentElement = keyupEvent.target.parentElement.parentElement;
    let textElement = parentElement.firstElementChild;
    textElement.textContent = keyupEvent.target.value;
    let pk = getElementPK(parentElement);
    // let idAttribute = searchForPK(this.quiz);
  }
}
</script>
<style scoped>
.quiz {
}
.quiz__ol_question-list {
  list-style: decimal;
}
.quiz__ol_answer-list {
  list-style: lower-alpha;
}
</style>
