<template>
  <h1>Editor2</h1>
  <Room />
</template>

<script>
import Room from "@/components/Room";
import { Options, Vue } from "vue-class-component";

@Options({
  components: {
    Room,
  },
})
export default class Editor2 extends Vue {}
</script>

<style scoped></style>
