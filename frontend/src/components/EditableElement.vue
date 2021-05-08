<template>
  <div class="editable-element">
    <div
      class="output"
      ref="outputElement"
      v-show="!editMode"
      @dblclick="enterEditMode"
    >
      {{ textOut }}
    </div>
    <div v-show="editMode">
      <label>
        <input
          ref="inputElement"
          type="text"
          :placeholder="textOut"
          @keyup.enter="editElement"
        />
      </label>
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
  // startEditMode is currently unused
  emits: ["update:text", "startEditMode", "edit", "endEditMode"],
  methods: {
    enterEditMode: function () {
      this.$emit("startEditMode");
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
      // Todo: You could change the value half way through this function
      let input_ = this.$refs.inputElement;
      if (!input_.value) {
        this.$emit("endEditMode");
        return;
      }
      if (input_.value !== this.textOut) {
        this.$emit("update:text", input_.value);
        this.$emit("edit");
      }
      this.textOut = input_.value;
      this.$refs.inputElement.value = null;
      this.$emit("endEditMode");
    },
    clearElement: function () {
      this.textOut = null;
      this.$refs.inputElement.value = null;
    },
  },
};
</script>

<style scoped>
.output:hover {
  background: aliceblue;
}
</style>
