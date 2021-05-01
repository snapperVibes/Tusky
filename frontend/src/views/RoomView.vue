<template>
  <Suspense>
    <template #default>
      <Room
        :roomCodeProp="roomCodeProp"
        :authTokenProp="authTokenProp"
        :roomInfoProp="roomInfoProp"
      />
    </template>
    <!--    Todo: Move the fallback into its own component-->
    <template #fallback>
      <div>
        <h1>Loading...</h1>
        <p>
          If you see this screen for more than a couple seconds, something went
          wrong. Try refreshing your page. If that doesn't work,
          <a href="mailto:bugs@tusky.org">report a bug </a>
        </p>
      </div>
    </template>
  </Suspense>
</template>
t
<script>
import { schema } from "@/api";
import Room from "@/components/room/Room";

export default {
  name: "RoomView",
  components: {
    Room,
  },
  props: {
    roomCodeProp: String,
    roomInfoProp: String,
    authTokenProp: String,
  },
};
</script>

<style scoped></style>
