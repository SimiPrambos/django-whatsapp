<template>
  <v-app id="register" class="primary">
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
                    append-icon="person"
                    data-vv-name="email"
                    label="Email"
                    type="text"
                    v-model="model.email"
                    v-validate="'required|email'"
                    :error-messages="errors.collect('email')"
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
                  <v-text-field
                    append-icon="lock"
                    data-vv-name="confirm-password"
                    data-vv-as="password"
                    label="Confirm Password"
                    type="password"
                    v-model="model.confirmpassword"
                    v-validate="'required|confirmed:password'"
                    :error-messages="errors.collect('confirm-password')"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  block
                  color="primary"
                  @click="register"
                  :disabled="!formValid"
                  :loading="loading"
                >Register</v-btn>
              </v-card-actions>
              <v-card-text>
                Already have account?
                <a href="/login">Login</a>
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
  data() {
    return {
      model: {
        username: "",
        email: "",
        password: "",
        confirmpassword: ""
      },
      loading: false
    };
  },
  computed: {
    formValid() {
      return !this.errors.any();
    }
  },
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
    async register() {
      if (!this.formIsNull() && this.formValid) {
        try {
          await this.$axios.post("auth/users/create/", {
            username: this.model.username,
            email: this.model.email,
            password: this.model.password
          });

          await this.$auth.loginWith("local", {
            data: {
              username: this.model.username,
              password: this.model.password
            }
          });

          this.$router.push("/");
        } catch (e) {
          this.clear();
        }
      }else{
        this.$validator.validateAll()
      }
    },
    clear() {
      this.model.username = "";
      this.model.email = "";
      this.model.password = "";
      this.model.confirmpassword = "";
      this.$validator.reset();
    }
  }
};
</script>