<!--TODO: Refactor forms into components-->
<template>
  <NavBar :username="username" />
  <h1>Tusky</h1>
  <RegistrationAndLogin @authTokenUpdate="onAuthTokenUpdate" />
  <EnterRoom />
  <CreateRoom />
</template>

<script>
import { ref } from "vue";
import NavBar from "@/components/NavBar";
import RegistrationAndLogin from "@/components/forms/RegistrationAndLogin";
import EnterRoom from "@/components/forms/EnterRoom";
import CreateRoom from "@/components/forms/CreateRoom";
import { roomsApi, usersApi, authHeaders } from "@/api";

export default {
  components: {
    RegistrationAndLogin,
    NavBar,
    EnterRoom,
    CreateRoom,
  },
  data: function () {
    return {
      authToken: null,
      username: null,
    };
  },
  methods: {
    onAuthTokenUpdate: async function (authToken) {
      this.authToken = authToken;
      const authHeader = authHeaders(authToken);
      const response = await usersApi.readCurrentUser(authHeader);
      this.username = response.data.display_name;
    },
  },
};
</script>

<style scoped></style>
