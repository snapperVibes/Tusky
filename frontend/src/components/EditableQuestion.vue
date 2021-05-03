<template>
  <div class="editable-question">
    <EditableElement
      :text="questionInfo.query"
      @elementUpdate="onElementUpdate"
    />
  </div>
</template>

<script>
import EditableElement from "@/components/EditableElement";
export default {
  name: "EditableQuestion",
  components: { EditableElement },
  methods: {
    onElementUpdate: function () {
      alert("Updating elements in not support yet.");
    },
  },
  props: ["questionInfo"],
};
</script>

<style scoped></style>
