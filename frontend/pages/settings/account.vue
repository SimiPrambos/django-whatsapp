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
                      <v-btn flat outline small>change password</v-btn>
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
export default {
  layout: "dashboard",
  middleware: "auth",
  data() {
    return {};
  },
  computed: {
    ...mapGetters({ user: "loggedInUser" }, { numbers: "numbers/numbers" })
  },
  methods: {
    formateDate(string) {
      return string ? new Date(string).toLocaleDateString() : "";
    }
  }
};
</script>

<style>
</style>
