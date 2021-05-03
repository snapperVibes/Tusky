<template>
  <form dis>
    <fieldset :disabled="loggedIn">
      <legend>Login / Register</legend>
      <label for="username-input"></label>
      <input
        type="text"
        placeholder="Username"
        id="username-input"
        v-model="usernameInput"
        required
      />
      <br />
      <label for="password-input"></label>
      <input
        type="password"
        placeholder="Password"
        id="password-input"
        v-model="passwordInput"
        required
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
      <span class="tusky__disabled-explanation" v-show="loggedIn">
        Log out to log-back-in / register as a different user.
      </span>
    </fieldset>
  </form>
</template>

<script>
// https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/#persistance
import { displayError, loginApi, usersApi } from "@/api";
import { concatUsername } from "@/userUtils";

export default {
  setup() {
    return {
      usernameInput: null,
      passwordInput: null,
      loggedIn: false,
    };
  },
  emits: {
    authTokenUpdate: String,
  },
  methods: {
    async loginEvent(clickEvent) {
      // On success emits a 'authTokenUpdate'
      const [frozenUsername, frozenPassword] = [
        this.usernameInput,
        this.passwordInput,
      ];
      const err = this._validate_input(frozenUsername, frozenPassword);
      if (err) {
        // Todo: Handle error should get its own function (once it's more complicated)
        alert(err);
        return;
      }
      await this._login(frozenUsername, frozenPassword);
    },

    async _login(username, password) {
      // Note: _login expects non-empty username and password.
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
      [this.usernameInput, this.passwordInput] = [null, null];
      this.$forceUpdate();
      // const authToken = await response.data.authToken;
      // // Todo: the username SHOULD be fetched on the same call as the token
      // console.log(response);
      // this.$emit("authTokenUpdate", authToken);
    },

    async registerEvent(clickEvent) {
      // On success, modifies this.authToken and emits a 'authTokenUpdate'
      const [frozenUsername, frozenPassword] = [
        this.usernameInput,
        this.passwordInput,
      ];

      const err = this._validate_input(frozenUsername, frozenPassword);
      if (err) {
        // Todo: Handle error should get its own function (once it's more complicated)
        // Note: Handle error != api.handleError
        alert(err);
        return;
      }

      let response = await usersApi
        .createUser({
          display_name: frozenUsername,
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
    _validate_input(username, password) {
      if (!username || !password) {
        return `Username and password fields must be filled out to log in to login / register.`;
      }
    },
  },
  computed: {},
};
</script>

<style scoped></style>
