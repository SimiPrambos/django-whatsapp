<template>
  <div id="pageNumbers">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg12 sm12 xs12>
          <v-card>
            <v-toolbar card dense color="transparent">
              <v-dialog v-model="dialog" max-width="500px">
                <template v-slot:activator="{ on }">
                  <v-btn flat small outline color="primary" v-on="on">add new</v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="headline">New Number</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container grid-list-md>
                      <v-layout wrap>
                        <v-flex xs12 sm12 md12>
                          <v-text-field v-model="newnumber.name" label="Name"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm12 md12>
                          <v-text-field v-model="newnumber.number" label="Number"></v-text-field>
                        </v-flex>
                      </v-layout>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
                    <v-btn color="blue darken-1" flat @click="save">Save</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                append-icon="search"
                label="Search"
                single-line
                hide-details
              ></v-text-field>
            </v-toolbar>
            <v-card-text class="pa-0">
              <template>
                <v-data-table
                  :headers="headers"
                  :items="items"
                  :search="search"
                  hide-actions
                  class="elevation-0 table-striped"
                >
                  <template slot="items" slot-scope="props">
                    <td>{{ props.index+1 }}</td>
                    <td class="text-xs-left">{{ props.item.lable }}</td>
                    <td class="text-xs-left">{{ props.item.number }}</td>
                    <td class="text-xs-left">
                      <v-chip
                        label
                        small
                        :color="getColorByStatus(getLabelIsRunning(props.item.is_running))"
                        text-color="white"
                      >{{ getLabelIsRunning(props.item.is_running) }}</v-chip>
                    </td>
                    <td class="text-xs-left">
                      <v-chip
                        label
                        small
                        :color="getColorByStatus(getLabelStatus(props.item.is_logged_in))"
                        text-color="white"
                      >{{ getLabelStatus(props.item.is_logged_in) }}</v-chip>
                    </td>
                    <td class="text-xs-left">{{ props.item.created_at }}</td>
                    <td>
                      <v-btn-toggle>
                        <v-btn small outline fab color="black" @click="toSetting(props.item.id)">
                          <v-icon>settings</v-icon>
                        </v-btn>
                        <v-btn
                          small
                          outline
                          fab
                          color="black"
                          @click="deleteNumber(props.item.id)"
                          :disabled="props.item.is_running"
                        >
                          <v-icon>delete</v-icon>
                        </v-btn>
                      </v-btn-toggle>
                    </td>
                  </template>
                  <v-alert
                    slot="no-results"
                    :value="true"
                    color="error"
                    icon="warning"
                  >No results for "{{ search }}".</v-alert>
                </v-data-table>
              </template>
              <v-divider></v-divider>
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
  data() {
    return {
      headers: [
        { text: "ID", align: "left", sortable: true, value: "id" },
        { text: "Name", align: "left", value: "lable", sortable: true },
        { text: "Number", align: "left", value: "number", sortable: true },
        {
          text: "Instance",
          align: "left",
          value: "is_running",
          sortable: true
        },
        {
          text: "Status",
          align: "left",
          value: "is_logged_in",
          sortable: true
        },
        {
          text: "Created",
          align: "left",
          value: "created_at",
          sortable: true
        },
        { text: "Action", align: "center", value: "action" }
      ],
      newnumber: {
        name: "",
        number: ""
      },
      search: "",
      colors: {
        Running: "green",
        NotRunning: "red",
        LoggedIn: "green",
        NotLoggedIn: "red",
        WaitForLogin: "blue"
      },
      disable: false,
      dialog: false
    };
  },
  mounted() {
    this.$store.dispatch("numbers/GET_NUMBERS");
  },
  computed: {
    ...mapGetters({ items: "numbers/numbers", user: "loggedInUser" })
  },
  methods: {
    getColorByStatus(status) {
      return this.colors[status];
    },
    getLabelIsRunning(status) {
      return status === true ? "Running" : "NotRunning";
    },
    getLabelStatus(status) {
      return status ? "LoggedIn" : status ? "WaitForLogin" : "NotLoggedIn";
    },
    toSetting(id) {
      this.$router.push(`numbers/${id}`);
    },
    close() {
      this.dialog = false;
    },
    save() {
      let payload = {
        lable: this.newnumber.name,
        number: this.newnumber.number
      };
      this.$store.dispatch("numbers/POST_NUMBERS", payload);
      this.close();
    },
    deleteNumber(id) {
      this.$store.dispatch("numbers/DELETE_NUMBERS", id);
    }
  }
};
</script>
