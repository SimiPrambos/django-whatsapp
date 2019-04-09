<template>
  <div id="pageMessages">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex>
          <v-card>
            <v-toolbar card dense color="transparent">
              <v-btn v-if="selected.length > 0" flat outline color="red" @click="onDelete">
                <v-icon>delete</v-icon>
                delete ({{selected.length===(items.length)?"ALL":selected.length}})
              </v-btn>
              <v-toolbar-title v-else>
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
              <v-spacer></v-spacer>
              <v-btn flat large icon @click="refresh">
                <v-icon>refresh</v-icon>
              </v-btn>
            </v-toolbar>
            <v-card-text class="pa-0">
              <template>
                <v-data-table
                  v-model="selected"
                  :headers="headers"
                  :items="items"
                  :search="search"
                  item-key="id"
                  select-all
                  :pagination.sync="pagination"
                  hide-actions
                  class="elevation-1 table-striped"
                >
                  <template v-slot:items="props">
                    <tr>
                      <td>
                        <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
                      </td>
                      <!-- <td>{{ props.index+1 }}</td> -->
                      <td class="text-xs-left">{{ props.item.message_number }}</td>
                      <td
                        class="text-xs-left"
                        @click="detailMessage(props.item.number,props.item.message_number,props.item.message_content)"
                      >{{ props.item.message_content.substring(0,10) }}...</td>
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
                <div class="text-xs-center pt-2">
                  <v-pagination v-model="pagination.page" :length="pages"></v-pagination>
                </div>
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
            <v-layout row wrap>
              <v-flex lg12 sm12 xs12>
                <v-text-field
                  name="number"
                  :value="selectedMessage.message_number"
                  box
                  readonly
                  label="Number"
                ></v-text-field>
              </v-flex>
              <v-flex lg12 sm12 xs12>
                <v-textarea
                  name="message"
                  :value="selectedMessage.message_content"
                  box
                  readonly
                  label="Message"
                ></v-textarea>
              </v-flex>
              <v-flex lg10 sm10 xs10 v-if="messageType === 'IN'">
                <v-text-field name="replay" v-model="textreplay" label="Replay"></v-text-field>
              </v-flex>
              <v-flex lg2 sm2 xs2 v-if="messageType === 'IN'">
                <v-btn :disabled="!textreplay" flat fab color="teal" icon @click="replay">
                  <v-icon>send</v-icon>
                </v-btn>
              </v-flex>
            </v-layout>
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
      selectedMessage: {
        number: "",
        message_number: "",
        message_content: ""
      },
      pagination: {},
      textreplay: "",
      selected: []
    };
  },
  mounted() {
    if (!this.items) {
      this.$store.dispatch("messages/GET_MESSAGES");
    }
  },
  computed: {
    ...mapGetters({ messages: "messages/messagesByType" }),
    items() {
      return this.messages(this.messageType);
    },
    messageType() {
      let type = this.$route.params.messageType.toLowerCase();
      return type === "inbox" ? "IN" : type === "outbox" ? "OUT" : "ALL";
    },
    headers() {
      return [
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
    },
    pages() {
      if (
        this.pagination.rowsPerPage == null ||
        this.pagination.totalItems == null
      )
        return 0;

      return Math.ceil(
        this.pagination.totalItems / this.pagination.rowsPerPage
      );
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
      return string
        ? new Date(string).toLocaleTimeString(navigator.language, {
            hour12: false
          })
        : "";
    },
    detailMessage(number, message_number, message_content) {
      this.selectedMessage.number = number;
      this.selectedMessage.message_number = message_number;
      this.selectedMessage.message_content = message_content;
      this.dialog = true;
    },
    refresh() {
      this.$store.dispatch("messages/GET_MESSAGES");
    },
    replay() {
      let payload = {
        numberId: this.selectedMessage.number,
        messages: [
          {
            message_number: this.selectedMessage.message_number,
            message_content: this.textreplay
          }
        ]
      };
      this.$store.dispatch("messages/POST_TEXT_MESSAGE", payload);
      this.dialog = false;
    },
    onDelete() {
      this.selected.map(message => {
        this.$store.dispatch("messages/DELETE_MESSAGES", {
          id: message.id,
          number: message.number
        });
      });
    }
  }
};
</script>

<style scoped>
</style>