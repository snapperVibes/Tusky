<template>
  <Suspense>
    <template #default>
      <Room :roomcode="roomcode" />
    </template>
    <!--    Todo: Move the fallback into its own component-->
    <template #fallback>
      <div>
        <h1>Loading...</h1>
        <p>
          If you see this screen for more than a couple seconds, something went
          wrong
        </p>
      </div>
    </template>
  </Suspense>
  <!--  <Room :roomcode="roomcode" />-->
</template>

<script>
import Room from "@/components/room/Room";

export default {
  name: "RoomView",
  components: {
    Room,
  },
  props: {
    roomcode: String,
  },
};
</script>

<style scoped></style>
