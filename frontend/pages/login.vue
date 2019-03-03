<template>
  <v-app id="login" class="primary">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4 lg4>
            <v-card class="elevation-1 pa-3">
              <v-card-text>
                <div class="layout column align-center">
                  <!-- <img src="../static/m.png" alt="Vue Material Admin" width="120" height="120"> -->
                  <h1 class="flex my-4 primary--text">Your Brand</h1>
                </div>
                <v-form>
                  <v-text-field
                    append-icon="person"
                    name="username"
                    label="Username"
                    type="text"
                    v-model="model.username"
                    v-validate="'required'"
                    :error-messages="errors.collect('username')"
                  ></v-text-field>
                  <v-text-field
                    append-icon="lock"
                    data-vv-name="password"
                    label="Password"
                    type="password"
                    v-model="model.password"
                    v-validate="'required'"
                    :error-messages="errors.collect('password')"
                    ref="password"
                  ></v-text-field>
                </v-form>
                <p v-if="error" style="color:red">{{error}}</p>
              </v-card-text>
              <v-card-actions>
                <v-btn block color="primary" @click="login" :loading="loading">Login</v-btn>
              </v-card-actions>
              <v-card-text>
                Don't have an account yet?
                <a href="/register">Register</a>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  layout: "default",
  middleware: "guest",
  data: () => ({
    loading: false,
    model: {
      username: "",
      password: ""
    },
    error: ""
  }),

  methods: {
    formIsNull() {
      let isnull = false;
      Object.keys(this.model).forEach(field => {
        if (this.model[field].length <= 0) {
          isnull = true;
        }
      });
      return isnull;
    },
    async login() {
      this.error = ""
      if (!this.formIsNull()) {
        try {
          this.loading = true;
          await this.$auth.loginWith("local", {
            data: {
              username: this.model.username,
              password: this.model.password
            }
          });

          this.$router.push("/");
        } catch (e) {
          this.error = "Unable to login with provided credentials.";
          this.loading = false;
        }
      } else {
        this.$validator.validateAll();
      }
    }
  }
};
</script>
<style scoped lang="css">
#login {
  height: 50%;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  content: "";
  z-index: 0;
}
</style>
