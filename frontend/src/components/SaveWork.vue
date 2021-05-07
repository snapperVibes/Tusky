<template>
  <div class="save-work">
    <nav>
      <button @click.prevent="saveWork">Save work</button>
    </nav>
  </div>
</template>

<script>
export default {
  name: "SaveWork",
  emits: ["saveWork"],

  methods: {
    saveWork: function () {
      this.$emit("saveWork");
    },
  },
};
</script>

<style scoped></style>
