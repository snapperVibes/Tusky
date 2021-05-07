<template>
  <div class="return-to-room">
    <nav>
      <button @click.prevent="toSelectionMode">To selection mode</button>
      (Unsaved data will be discarded)
    </nav>
  </div>
</template>

<script>
export default {
  name: "ToSelectionMode",
  emits: ["toSelectionMode"],

  methods: {
    toSelectionMode: function () {
      this.$emit("toSelectionMode");
    },
  },
};
</script>

<style scoped></style>
