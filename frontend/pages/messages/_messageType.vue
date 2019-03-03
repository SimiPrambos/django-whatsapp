<template>
  <div id="pageMessages">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg10 sm10 xs10>
          <v-card>
            <v-progress-linear :height="loading" :indeterminate="true"></v-progress-linear>
            <v-toolbar card dense color="transparent">
              <v-toolbar-title>
                <h4>Message List</h4>
              </v-toolbar-title>
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
                  :items="items(messageType)"
                  :search="search"
                  hide-actions
                  class="elevation-0 table-striped"
                >
                  <template slot="items" slot-scope="props">
                    <tr
                      @click="detailMessage(props.item.message_number,props.item.message_content)"
                    >
                      <td>{{ props.index+1 }}</td>
                      <td class="text-xs-left">{{ props.item.message_number }}</td>
                      <td class="text-xs-left">{{ props.item.message_content.substring(0,10) }}...</td>
                      <td class="text-xs-left">
                        <v-chip
                          label
                          small
                          :color="getColorByStatus(getLabelByStatus(props.item.message_status))"
                          text-color="white"
                        >{{ getLabelByStatus(props.item.message_status) }}</v-chip>
                      </td>
                      <td class="text-xs-left">{{ formateDate(props.item.message_timestamp) }}</td>
                      <td class="text-xs-left">{{ formateTime(props.item.message_timestamp) }}</td>
                    </tr>
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
    <template>
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span class="headline">Message Detail</span>
          </v-card-title>
          <v-card-text>
            <h5>Number  : {{selected.number}}</h5>
            <h5>Message : {{selected.message}}</h5>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click="dialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  layout: "dashboard",
  middleware: "auth",
  data() {
    return {
      loading: 0,
      search: "",
      colors: {
        Pending: "blue",
        Delivered: "green",
        Failed: "red"
      },
      dialog: false,
      selected: {
        message: "",
        number: ""
      }
    };
  },
  mounted() {
    this.$store.dispatch("messages/GET_MESSAGES");
  },
  computed: {
    ...mapGetters({ items: "messages/messagesByType" }),
    messageType() {
      let type = this.$route.params.messageType.toLowerCase();
      return type === "inbox" ? "IN" : type === "outbox" ? "OUT" : "ALL";
    },
    headers() {
      return [
        { text: "ID", align: "left", sortable: true, value: "id" },
        {
          text: this.messageType === "IN" ? "FROM" : "TO",
          align: "left",
          value: "message_number",
          sortable: true
        },
        {
          text: "MESSAGE",
          align: "left",
          value: "message_content",
          sortable: true
        },
        {
          text: "STATUS",
          align: "left",
          value: "message_status",
          sortable: true
        },
        {
          text: "DATE",
          align: "left",
          value: "message_timestamp",
          sortable: true
        },
        {
          text: "TIME",
          align: "left",
          value: "message_timestamp",
          sortable: true
        }
      ];
    }
  },
  methods: {
    getColorByStatus(status) {
      return this.colors[status];
    },
    getLabelByStatus(status) {
      return status === "P"
        ? "Pending"
        : status === "D"
        ? "Delivered"
        : status === "F"
        ? "Failed"
        : "Unknown";
    },
    formateDate(string) {
      return string ? new Date(string).toLocaleDateString() : "";
    },
    formateTime(string) {
      return string ? new Date(string).toLocaleTimeString() : "";
    },
    detailMessage(number, message) {
      this.selected.number = number;
      this.selected.message = message;
      this.dialog = true;
    }
  }
};
</script>

<style scoped>
</style>