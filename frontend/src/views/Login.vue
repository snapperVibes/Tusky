<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>{{appName}}</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form @keyup.enter="submit">
                <v-text-field @keyup.enter="submit" v-model="username" prepend-icon="person" name="login" label="Login" type="text"></v-text-field>
                <v-text-field @keyup.enter="submit" v-model="password" prepend-icon="lock" name="password" label="Password" id="password" type="password"></v-text-field>
              </v-form>
              <div v-if="loginError">
                <v-alert :value="loginError" transition="fade-transition" type="error">
                  Incorrect email or password
                </v-alert>
              </div>
              <v-flex class="caption text-xs-right"><router-link to="/recover-password">Forgot your password?</router-link></v-flex>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click.prevent="submit">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content></template>

<script>
import { Component, Vue } from 'vue-property-decorator'
import { appName } from '@/env'
import { readLoginError } from '@/store/main/getters'
import { dispatchLogIn } from '@/store/main/actions'

@Component
export default class Login extends Vue {
  username = ''
  password = ''
  appName = appName

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  get loginError () {
    return readLoginError(this.$store)
  }

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  get submit () {
    dispatchLogIn(this.$store, { username: this.username, password: this.password })
  }
}

</script>

<!--<style scoped>-->

<!--</style>-->
