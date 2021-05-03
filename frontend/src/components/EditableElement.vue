<template>
  <div class="editable-element">
    <div ref="outputElement" v-show="!editMode" @dblclick="enterEditMode">
      {{ textOut }}
    </div>
    <div v-show="editMode">
      <label />
      <input
        ref="inputElement"
        type="text"
        :placeholder="textOut"
        @keyup.enter="editElement"
      />
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "EditableElement",
  setup() {
    const inputElement = ref(null);
    const outputElement = ref(null);
    return {
      inputElement,
      outputElement,
    };
  },
  props: ["text"],
  data() {
    return {
      editMode: false,
      textIn: "",
      textOut: this.text,
    };
  },
  emits: ["elementUpdate"],

  methods: {
    enterEditMode: function () {
      this.editMode = true;
      // An explanation for why we need this.$nextTick to focus:
      // https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks/Vue_refs_focus_management
      this.$nextTick(() => {
        this.$refs.inputElement.focus();
      });
    },
    editElement: function (keyupEvent) {
      if (keyupEvent.ctrlKey) {
        return;
      }
      this.editMode = false;
      let input_ = this.$refs.inputElement;
      if (input_.value !== this.textOut) {
        console.log("Emitting an element updated event");
        this.$emit("elementUpdate");
      }
      this.textOut = input_.value;
      this.$refs.inputElement.value = null;
    },
  },
};
</script>

<style scoped></style>
