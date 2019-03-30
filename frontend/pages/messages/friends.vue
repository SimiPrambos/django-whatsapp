<template>
  <div id="pageFriends">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg5 sm5 xs12>
          <v-card>
            <v-toolbar card dense color="transparent">
              <v-btn v-if="cSelected.length > 0" flat outline color="red" @click="onDeleteContact">
                <v-icon left>delete</v-icon>
                delete ({{cSelected.length===(friendContacts.length)?"ALL":cSelected.length}})
              </v-btn>
              <v-card-title v-else>
                <v-icon left>mdi-contacts</v-icon>
                <span class="title font-weight-light">Friend Contacts</span>
              </v-card-title>
              <v-spacer></v-spacer>
              <!-- new contact -->
              <new-contact></new-contact>
            </v-toolbar>
            <v-card-text class="pa-0">
              <div>
                <v-data-table
                  v-model="cSelected"
                  :headers="hContacts"
                  :items="friendContacts"
                  :search="search"
                  hide-actions
                  item-key="id"
                  select-all
                  :pagination.sync="cPagination"
                  class="elevation-1"
                >
                  <template v-slot:items="props">
                    <td class="text-xs-left">
                      <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
                    </td>
                    <td class="text-xs-left">{{ props.item.name }}</td>
                    <td class="text-xs-left">{{ props.item.number }}</td>
                  </template>
                </v-data-table>
                <div class="text-xs-center pt-2">
                  <v-pagination v-model="cPagination.page" :length="pages('c')"></v-pagination>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex lg7 sm7 xs12>
          <v-card>
            <v-toolbar card dense color="transparent">
              <v-btn v-if="mSelected.length > 0" flat outline color="red" @click="onDeleteMessage">
                <v-icon left>delete</v-icon>
                delete ({{mSelected.length===(friendMessages.length)?"ALL":mSelected.length}})
              </v-btn>
              <v-card-title v-else>
                <v-icon left>mdi-message-text-outline</v-icon>
                <span class="title font-weight-light">Friend Messages</span>
              </v-card-title>
              <v-spacer></v-spacer>
              <form-dialog
                title="Add new message"
                label="add"
                color="blue"
                icon="add"
                :onSave="onSaveMessage"
                ref="addmessage"
              >
                <template v-slot:form>
                  <v-flex>
                    <v-textarea v-model="newMessage.message" label="text message"></v-textarea>
                  </v-flex>
                </template>
              </form-dialog>
            </v-toolbar>
            <v-card-text class="pa-0">
              <div>
                <v-data-table
                  v-model="mSelected"
                  :headers="hMessages"
                  :items="friendMessages"
                  :search="search"
                  hide-actions
                  item-key="id"
                  select-all
                  :pagination.sync="mPagination"
                  class="elevation-1"
                >
                  <template v-slot:items="props">
                    <td class="text-xs-left">
                      <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
                    </td>
                    <td class="text-xs-left">{{ props.item.message }}</td>
                  </template>
                </v-data-table>
                <div class="text-xs-center pt-2">
                  <v-pagination v-model="mPagination.page" :length="pages('m')"></v-pagination>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import NewContact from "@/components/contacts/NewContact";
import FormDialog from "@/components/contacts/FormDialog";
export default {
  layout: "dashboard",
  middleware: "auth",
  components: {
    NewContact,
    FormDialog
  },
  data() {
    return {
      hMessages: [
        { text: "message", align: "left", sortable: true, value: "message" }
      ],
      hContacts: [
        { text: "name", align: "left", sortable: true, value: "name" },
        { text: "number", align: "left", sortable: true, value: "number" }
      ],
      search: "",
      cPagination: {},
      mPagination: {},
      cSelected: [],
      mSelected: [],
      newMessage: {
        message: ""
      }
    };
  },
  mounted() {
    if (!this.friendMessages) {
      this.$store.dispatch("messages/GET_FRIEND_MESSAGES");
    }
    if (!this.contacts) {
      this.$store.dispatch("contacts/GET_CONTACTS");
    }
  },
  computed: {
    ...mapGetters({
      friendMessages: "messages/friendMessages",
      friendContacts: "contacts/friends",
      contacts: "contacts/contacts"
    })
  },
  methods: {
    pages(type) {
      let pagination = type === "c" ? this.cPagination : this.mPagination;
      if (pagination.rowsPerPage == null || pagination.totalItems == null)
        return 0;

      return Math.ceil(pagination.totalItems / pagination.rowsPerPage);
    },
    onDeleteContact() {
      this.$store.dispatch("contacts/DELETE_CONTACTS", this.cSelected);
    },
    onSaveMessage() {
      this.$store.dispatch("messages/POST_FRIEND_MESSAGE", this.newMessage);
      this.$refs.addmessage.close();
    },
    onDeleteMessage() {
      this.mSelected.map(message => {
        this.$store.dispatch("messages/DELETE_FRIEND_MESSAGE", message.id);
      });
    }
  }
};
</script>

<style>
</style>
