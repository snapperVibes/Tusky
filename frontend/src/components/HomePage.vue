<!--TODO: Refactor forms into components-->
<template>
  <NavBar :username="username" :number="number" />
  <RegistrationAndLogin @authTokenUpdate="onAuthTokenUpdate" />
  <EnterRoom :auth-token="authToken" />
  <CreateRoom :owner-id="userId" :auth-token="authToken" />
</template>

<script>
import { ref } from "vue";
import NavBar from "@/components/NavBar";
import RegistrationAndLogin from "@/components/RegistrationAndLogin";
import EnterRoom from "@/components/EnterRoom";
import CreateRoom from "@/components/CreateRoom";
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
      userId: null,
      username: null,
      number: null,
    };
  },
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
};
</script>

<style scoped></style>
