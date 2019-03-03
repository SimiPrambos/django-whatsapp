<template>
  <v-toolbar color="primary" fixed dark app>
    <v-toolbar-title class="ml-0 pl-3">
      <v-toolbar-side-icon @click.stop="toggleDrawer()"></v-toolbar-side-icon>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon @click="handleFullScreen()">
      <v-icon>fullscreen</v-icon>
    </v-btn>
    <v-menu
      offset-y
      origin="center center"
      class="elelvation-1"
      :nudge-width="140"
      :nudge-bottom="14"
      transition="scale-transition"
      v-if="isAuthenticated"
    >
      <v-toolbar-title slot="activator">
        <span>{{loggedInUser.username}}</span>
        <v-icon dark>arrow_drop_down</v-icon>
      </v-toolbar-title>

      <v-list class="pa-0">
        <v-list-tile href="#" @click="logout" rel="noopener">
          <v-list-tile-action>
            <v-icon>fullscreen_exit</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Logout</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-menu>
    <v-menu
      offset-y
      origin="center center"
      :nudge-right="140"
      :nudge-bottom="10"
      transition="scale-transition"
      v-else
    >
      <v-btn @click="login" icon large flat slot="activator">LOGIN</v-btn>
    </v-menu>
  </v-toolbar>
</template>
<script>
import Util from "@/util";
import { mapGetters } from "vuex";

export default {
  name: "app-toolbar",
  data: () => ({}),
  computed: {
    toolbarColor() {
      return this.$vuetify.options.extra.mainNav;
    },
    ...mapGetters(["loggedInUser", "isAuthenticated"])
  },
  methods: {
    toggleDrawer() {
      this.$store.commit("toggleDrawer");
    },
    handleFullScreen() {
      Util.toggleFullScreen();
    },
    async login() {
      await this.$router.push("/login");
    },
    async logout() {
      await this.$auth.logout().then(() => {
        this.$store.dispatch("messages/RESET_STATE");
        this.$store.dispatch("numbers/RESET_STATE");
      });
    }
  }
};
</script>
