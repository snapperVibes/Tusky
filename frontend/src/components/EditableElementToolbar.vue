<!--Todo: Proper SVGs 😛-->
<template>
  <div class="toolbar">
    <div class="toolbox">
      <span class="action material-add" @click="addElement">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 0 24 24"
          width="24px"
          fill="green"
        >
          <path d="M0 0h24v24H0V0z" fill="none" />
          <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
        </svg>
      </span>
      <span class="action delete" @click="deleteElement"
        ><svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 0 24 24"
          width="24px"
          fill="red"
        >
          <path d="M0 0h24v24H0V0z" fill="none" />
          <path
            d="M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-3.5l-1-1zM18 7H6v12c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7z"
          /></svg
      ></span>
      <!--    This is the icon for the Edit button, if we want it -->
      <!--    <span class="action edit" @click="$emit('edit')"-->
      <!--      ><svg-->
      <!--        xmlns="http://www.w3.org/2000/svg"-->
      <!--        height="24px"-->
      <!--        viewBox="0 0 24 24"-->
      <!--        width="24px"-->
      <!--        fill="#F88917"-->
      <!--      >-->
      <!--        <path d="M0 0h24v24H0V0z" fill="none" />-->
      <!--        <path-->
      <!--          d="M14.06 9.02l.92.92L5.92 19H5v-.92l9.06-9.06M17.66 3c-.25 0-.51.1-.7.29l-1.83 1.83 3.75 3.75 1.83-1.83c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.2-.2-.45-.29-.71-.29zm-3.6 3.19L3 17.25V21h3.75L17.81 9.94l-3.75-3.75z"-->
      <!--        /></svg-->
      <!--    ></span>-->
    </div>
    <li v-if="editMode">
      <EditableElement
        ref="editMe"
        :text="placeholder"
        @edit="onEdit"
        @endEditMode="onEndEditMode"
      />
    </li>
  </div>
</template>

<script>
import EditableElement from "@/components/EditableElement";
export default {
  name: "EditableElementToolbar",
  components: { EditableElement },
  emits: ["add", "edit", "delete"],
  data() {
    return {
      editMode: false,
    };
  },
  props: ["placeholder"],
  methods: {
    addElement: function () {
      console.log("Hit add!");
      this.editMode = true;
      this.$nextTick(() => {
        this.$refs.editMe.enterEditMode();
      });
    },
    deleteElement: function () {
      this.$emit("delete");
    },
    onEdit: function () {
      // Writing bad code pains me.
      // Tusky's inner $emit API is an uncohesive mess
      this.$emit("add", this.$refs.editMe.inputElement.value);
    },
    onEndEditMode: function () {
      this.$refs.editMe.clearElement();
      this.editMode = false;
    },
  },
};
</script>

<style scoped>
.toolbox {
  display: flex;
  flex: 1;

  flex-direction: row;
}
span.action {
  padding: 3px;
  margin: 1px;
}
span.action:hover {
  background: wheat;
}
</style>
