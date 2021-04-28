<template>
  <form v-show="!loggedIn">
    <fieldset>
      <legend>Login / Register</legend>
      <label for="username-input"></label>
      <input
        type="text"
        placeholder="Username"
        id="username-input"
        v-model="usernameInput"
      />
      <br />
      <label for="password-input"></label>
      <input
        type="password"
        placeholder="Password"
        id="password-input"
        v-model="passwordInput"
      />
      <br />
      <input
        @click.prevent="loginEvent"
        class="button"
        type="submit"
        value="Login"
      />
      <input
        @click.prevent="registerEvent"
        class="button"
        type="submit"
        value="Register"
      />
    </fieldset>
  </form>
</template>

<script>
// https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/#persistance
import { Vue } from "vue-class-component";
import { displayError, loginApi, usersApi } from "@/api";
import { concatUsername } from "@/userUtils";

// Modes

export default {
  setup() {
    return {
      usernameInput: null,
      passwordInput: null,
      loggedIn: false,
    };
  },

  methods: {
    async loginEvent(clickEvent) {
      // On success emits a 'authTokenUpdate'
      await this._login(this.usernameInput, this.passwordInput);
    },
    async _login(username, password) {
      const response = await loginApi
        .loginAccessToken("", username, password, "", "", "")
        .catch((error) => {
          displayError(error);
        });
      if (response === undefined) {
        return;
      }
      const authToken = response.data.access_token;
      this.$emit("authTokenUpdate", authToken);
      this.loggedIn = true;
      this.$forceUpdate();
      // const authToken = await response.data.authToken;
      // // Todo: Obviously, the username SHOULD be fetched on the same call as the token
      // console.log(response);
      // this.$emit("authTokenUpdate", authToken);
    },
    async registerEvent(clickEvent) {
      // On success, modifies this.authToken and emits a 'authTokenUpdate'
      const frozenPassword = this.passwordInput;
      let response = await usersApi
        .createUser({
          display_name: this.usernameInput,
          password: frozenPassword,
        })
        .catch((error) => displayError(error));
      if (response === undefined) {
        return;
      }
      const user = response.data;
      console.log(user);
      const fullUsername = concatUsername(user.identifier_name, user.number);
      await this._login(fullUsername, frozenPassword);
    },
  },
  emits: {
    authTokenUpdate: String,
  },
};
</script>

<style scoped></style>
