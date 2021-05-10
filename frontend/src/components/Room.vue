<template>
  <div class="room">
    <h1>Room {{ roomcode }}</h1>
    <div class="before-login">
      <RegistrationAndLogin
        v-show="!authToken"
        @authTokenUpdate="onAuthTokenUpdate"
      />
    </div>
    <div class="after-login" v-if="authToken">
      <Suspense>
        <template #default>
          <TeacherRoom
            v-if="userId === roomInfo.owner_id"
            :authToken="authToken"
            :roomInfo="roomInfo"
          />
          <StudentRoom v-else :authToken="authToken" :room-info="roomInfo" />
        </template>
        <template #fallback> Loading </template>
      </Suspense>
    </div>

    <!--    <Quiz />-->
  </div>
</template>

<script>
import { ref } from "vue";
import TeacherRoom from "@/components/TeacherRoom";
import StudentRoom from "@/components/StudentRoom";
import RegistrationAndLogin from "@/components/RegistrationAndLogin";
import { roomsApi, displayError, authHeaders, usersApi } from "@/api";
import jwt_decode from "jwt-decode";
// import Quiz from "@/components/room/quiz/Quiz";

function atLeastOneOf(...values) {
  // Takes a number of attributes that may be undefined.
  // Tests that the ones that aren't undefined share the same value.
  // Returns the value
  let masterValue;
  values.forEach((v) => {
    if (v !== undefined) {
      if (masterValue === undefined) {
        masterValue = v;
      }
      if (masterValue != v) {
        alert("Tusky failed a santiy check.");
        console.log("Failed sanity check values:", values);
      }
    }
  });
}

export default {
  props: {
    roomCodeProp: String,
    authTokenProp: String,
    roomInfoProp: String,
  },
  async setup(props) {
    let activeRoom = true;
    let roomInfo;
    if (props.roomInfoProp) {
      roomInfo = ref(JSON.parse(props.roomInfoProp));
    } else {
      const response = await roomsApi
        .getRoomByCode(props.roomCodeProp.toUpperCase())
        .catch(function (err) {
          displayError(err);
          // Todo: it would be nice if the error was "not authenticated" it would allow
          // you to authenticate in place instead of kicking you back to the home screen
          window.location.href = "http://localhost:8080/";
        });
      roomInfo = response.data;
    }
    if (roomInfo === undefined) {
      activeRoom = false;
      alert("The room could not be found");
      window.location.href = "http://localhost:8080/";
    }

    // Get the room code, however it may be given
    const propsToTry = [];
    if (props.roomInfoProp) {
      propsToTry.push(props.roomInfoProp.code);
    }
    if (props.roomCodeProp) {
      propsToTry.push(props.roomCodeProp);
    }
    const authToken = ref(props.authTokenProp);
    const roomCodeProp = atLeastOneOf.apply(this, propsToTry);
    return {
      activeRoom: activeRoom,
      // roomInfo: roomInfo.data,
      // eslint-disable-next-line vue/no-dupe-keys
      roomcode: ref(props.roomCodeProp),
      roomInfo: roomInfo,
      authToken: authToken,
    };
  },
  components: { TeacherRoom, StudentRoom, RegistrationAndLogin },
  methods: {
    onAuthTokenUpdate: async function (authToken) {
      this.authToken = authToken;
      const authHeader = authHeaders(this.authToken);
      const response = await usersApi.readCurrentUser(authHeader);
      const data = response.data;
      this.userId = data.id;
      this.username = data.display_name;
      this.number = data.number;
    },
  },
  computed: {
    userId() {
      return jwt_decode(this.authToken).sub;
    },
  },
};
</script>

<style scoped></style>
