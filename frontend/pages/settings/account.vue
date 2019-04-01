<template>
  <div id="pageAccount">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex>
          <v-card>
            <v-card-title>
              <v-icon left>details</v-icon>
              <span class="title font-weight-light">Account Details</span>
            </v-card-title>
            <v-card-text>
              <v-data-table :items="[1]" hide-headers hide-actions>
                <template v-slot:items="props">
                  <tr>
                    <td class="text-xs-left subheading">Username</td>
                    <td class="text-xs-left subheading">{{user.username}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Email</td>
                    <td class="text-xs-left subheading">{{user.email}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Password</td>
                    <td class="text-xs-left subheading">
                      <form-dialog
                        title="Change password"
                        label="change password"
                        color="black"
                        icon="mdi-lock-open-outline"
                        :onSave="onSave"
                        ref="changepassword"
                      >
                        <template v-slot:form>
                          <v-flex>
                            <v-text-field
                              append-icon="lock"
                              data-vv-name="currentpassword"
                              label="Current Password"
                              type="password"
                              v-model="changePassword.current_password"
                              v-validate="'required|min:8'"
                              :error-messages="errors.collect('currentpassword')"
                              ref="currentpassword"
                            ></v-text-field>
                          </v-flex>
                          <v-flex>
                            <v-text-field
                              append-icon="lock"
                              data-vv-name="newpassword"
                              label="New Password"
                              type="password"
                              v-model="changePassword.new_password"
                              v-validate="'required|min:8'"
                              :error-messages="errors.collect('newpassword')"
                              ref="newpassword"
                            ></v-text-field>
                          </v-flex>
                        </template>
                      </form-dialog>
                    </td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Joined at</td>
                    <td class="text-xs-left subheading">{{formateDate(user.date_joined)}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Status</td>
                    <td class="text-xs-left subheading">{{user.is_active?'Activated':'Deactivated'}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Api Key</td>
                    <td class="text-xs-left subheading">{{user.api_key}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Key Expired</td>
                    <td class="text-xs-left subheading">{{formateDate(user.expired)}}</td>
                  </tr>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import FormDialog from "@/components/contacts/FormDialog";
export default {
  layout: "dashboard",
  middleware: "auth",
  components: {
    FormDialog
  },
  data() {
    return {
      changePassword: {
        current_password: "",
        new_password: ""
      }
    };
  },
  computed: {
    ...mapGetters({ user: "loggedInUser" }, { numbers: "numbers/numbers" })
  },
  methods: {
    formateDate(string) {
      return string ? new Date(string).toLocaleDateString() : "";
    },
    onSave() {
      console.log(this.changePassword);
      this.$axios
        .post("auth/password/", this.changePassword)
        .then(response => {
          if (response.status === 204) {
            this.$auth.logout();
          }
        })
        .catch(error => {
          if (error.response.status === 400) {
            if (error.response.data.current_password) {
              this.errors.add({
                field: "currentpassword",
                msg: error.response.data.current_password
              });
            }
            if (error.response.data.new_password) {
              this.errors.add({
                field: "newpassword",
                msg: error.response.data.new_password
              });
            }
          }
        });
    }
  }
};
</script>

<style>
</style>
