<!-- Good code shouldn't need comments. Unfortunately, the quality of this code is questionable -->
<template>
  <!--  TODO: Documentation
   For an element to be editable, the element must be wrapped in a div.
   The div's id must be the editable field's counterpart on `this.quiz`, and underscore, and the primary key.
   The div must contain 2 child elements; The second must be a label. -->
  <div class="quiz">
    <div
      class="quiz__div_quiz-name editable"
      v-bind:id="'name_' + quiz.id"
      v-on:dblclick="editElement"
    >
      <h1 class="quiz__div_quiz-name_h1" v-html="quiz.name"></h1>
      <label hidden>
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
          class="quiz__div_query editable"
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
              class="quiz__div_answer editable"
              v-bind:id="'text_' + a.id"
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
      <!--      &lt;!&ndash; Additional Question &ndash;&gt;-->
      <!--      <li class="quiz__li_question">-->
      <!--        <div-->
      <!--          class="quiz__div_query"-->
      <!--          id="query_additional"-->
      <!--          v-on:dblclick="editElement"-->
      <!--        >-->
      <!--          <span class="quiz__div_query_span additional editable">-->
      <!--            Double click to add an additional question.-->
      <!--          </span>-->
      <!--          <label hidden>-->
      <!--            <input-->
      <!--              type="text"-->
      <!--              class="quiz__div_query_input text-editor"-->
      <!--              v-on:keyup.enter="setText"-->
      <!--            />-->
      <!--          </label>-->
      <!--        </div>-->
      <!--      </li>-->
    </ol>
    <div>
      <button class="saveButton" v-on:click="saveAll">Save</button>
    </div>
  </div>
</template>

<script>
import { Vue } from "vue-class-component";
import { api, QuizzesApi, UsersApi } from "@/api";

let usersApi = new UsersApi();
let quizApi = new QuizzesApi();

async function getData() {
  let _admin = (
    await Promise.resolve(usersApi.getByNameApiV1UsersGetByNameGet("Admin", 0))
  ).data;
  console.log("Admin:", _admin);
  let _quiz = quizApi.getFullQuizApiV1QuizzesGetGet("Example Quiz", _admin.id);
  // let _admin = (await Promise.resolve(api.getUser("Admin", "0"))).data;
  // let _quiz = (await Promise.resolve(api.getQuiz("Example Quiz", _admin.id)))
  //   .data;
  return {
    admin: _admin,
    quiz: _quiz,
  };
}
let data = getData();

function splitIdParts(element) {
  let splitId = element.id.split("_");
  // Doing it this way makes it easier to extend the id in the future
  return {
    part: splitId[splitId.length - 2],
    pk: splitId[splitId.length - 1],
  };
}

function getAll(obj, pk) {
  for (const [_, value] of Object.entries(obj)) {
    if (pk === value) {
      return obj;
    }
    if (typeof value != "object" || value === null) {
      continue;
    }
    let r = getAll(value, pk);
    if (r) {
      return r;
    }
  }
}

export default class QuizEditor extends Vue {
  // Todo: Order answers: This should happen at the API level

  quiz = data.then((res) => (this.quiz = res.quiz));

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
    inputElement.setAttribute("placeholder", element.textContent);

    // Swap invisibility
    textElement.setAttribute("hidden", "true");
    labelElement.removeAttribute("hidden");
    inputElement.focus();
  }

  // This function is called when the user finishes (clicks enter) on a text-editor
  setText(keyupEvent) {
    // Allow multiple-lines if the user holds the control-key
    if (keyupEvent.ctrlKey) {
      return;
    }
    // The first parent is the label. The second parent is the div
    let labelElement = keyupEvent.target.parentElement;
    let parentElement = labelElement.parentElement;
    let textElement = parentElement.firstElementChild;
    let idParts = splitIdParts(parentElement);
    // Todo: Better naming; both the names quizAttr and getAll are weak
    let quizAttr = getAll(this.quiz, idParts.pk);

    let text = keyupEvent.target.value.trim();
    if (text === "") {
      // If the box is empty, return the original value
    } else {
      quizAttr[idParts.part] = text;
      // Todo: mark element as dirty (and only change dirty elements)
    }
    // Swap invisibility
    labelElement.setAttribute("hidden", "true");
    textElement.removeAttribute("hidden");
  }

  saveAll() {
    api.modifyQuiz(this.quiz.id, this.quiz.name, this.quiz.owner_id);
    console.log("Saved!");
    console.log(api);
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
.additional {
  font-style: italic;
}
</style>
