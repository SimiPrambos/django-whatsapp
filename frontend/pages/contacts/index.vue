<template>
  <div id="newContact">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg10 sm10 xs12>
          <v-card flat>
            <!-- header -->
            <v-toolbar card dense color="transparent">
              <!-- delete button -->
              <v-btn v-if="selected.length > 0" flat outline color="red" @click="onDelete">
                <v-icon>delete</v-icon>
                delete ({{selected.length===(contacts.length)?"ALL":selected.length}})
              </v-btn>
              <!-- add button -->
              <new-contact></new-contact>
              <!-- import button -->
              <form-dialog
                title="Import Contact"
                label="import"
                color="blue"
                icon="mdi-import"
                maxWidth="700px"
                :onSave="onSave"
                ref="importcontact"
              >
                <template v-slot:form>
                  <v-flex xs3 sm3 md3 align-self-start color="red">
                    <upload-button
                      accept=".csv, text/csv"
                      large
                      title
                      icon
                      color="transparent"
                      :ripple="false"
                      :fileChangedCallback="fileChanged"
                    >
                      <template slot="icon-left">
                        <v-icon>attach_file</v-icon>
                      </template>
                    </upload-button>
                  </v-flex>
                  <v-flex xs8 sm8 md8>
                    <v-text-field readonly :label="filename?filename:'select csv file'"></v-text-field>
                  </v-flex>
                  <v-dialog v-model="loadfile" hide-overlay persistent width="300">
                    <v-card color="primary" dark>
                      <v-card-text>
                        Validating File
                        <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
                      </v-card-text>
                    </v-card>
                  </v-dialog>
                  <!-- info -->
                  <v-flex>
                    <v-data-table disable-initial-sort :headers="helpImport.headers" :items="helpImport.items" hide-actions dark>
                      <template v-slot:items="props">
                        <tr>
                          <td class="text-xs-left caption">{{props.item.field}}</td>
                          <td class="text-xs-left caption">{{props.item.type}}</td>
                          <td class="text-xs-left caption">{{props.item.example}}</td>
                          <td class="text-xs-left caption">{{props.item.detail}}</td>
                        </tr>
                      </template>
                    </v-data-table>
                  </v-flex>
                </template>
              </form-dialog>
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
            <!-- body -->
            <v-card-text class="pa-0">
              <v-data-table
                v-model="selected"
                :headers="headers"
                :items="contacts"
                :search="search"
                item-key="id"
                select-all
                :pagination.sync="pagination"
                hide-actions
                class="elevation-1"
              >
                <template v-slot:items="props">
                  <tr>
                    <td>
                      <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
                    </td>
                    <td class="text-xs-left">{{ props.item.name }}</td>
                    <td class="text-xs-left">{{ props.item.number }}</td>
                    <td class="text-xs-left">{{ props.item.country.toUpperCase() }}</td>
                    <td class="text-xs-left">{{ props.item.is_phone_number?'Valid':'Invalid' }}</td>
                    <!-- <td>
                      <v-btn-toggle>
                        <v-btn
                          small
                          outline
                          fab
                          color="black"
                          @click="props.expanded = !props.expanded"
                        >
                          <v-icon>mdi-information-outline</v-icon>
                        </v-btn>
                      </v-btn-toggle>
                    </td>-->
                  </tr>
                </template>

                <!-- <template v-slot:expand="props">
                  <v-card flat>
                    <v-card-text class="text-xs-center">
                      <v-data-table :items="[1]" hide-headers hide-actions>
                        <template v-slot:items="props">
                          <tr>
                            <td class="text-xs-left subheading">Name</td>
                            <td class="text-xs-left subheading">{{props.item.name}}</td>
                          </tr>
                        </template>
                      </v-data-table>
                    </v-card-text>
                  </v-card>
                </template>-->
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
import UploadButton from "vuetify-upload-button";
import NewContact from "@/components/contacts/NewContact";
export default {
  layout: "dashboard",
  middleware: "auth",
  components: {
    FormDialog,
    UploadButton,
    NewContact
  },
  data() {
    return {
      selected: [],
      search: "",
      headers: [
        { text: "NAME", value: "name", align: "left" },
        { text: "NUMBER", value: "number", align: "left" },
        { text: "COUNTRY", value: "country", align: "left" },
        { text: "STATUS", value: "is_phone_number", align: "left" }
        // { text: "DETAIL", value: "detail", align: "left" }
      ],
      filename: "",
      file: null,
      loadfile: false,
      pagination: {},
      helpImport: {
        headers: [
          {text: "Column", value: "field"},
          {text: "Type", value: "type"},
          {text: "Example", value: "example"},
          {text: "Detail", value: "detail"}
        ],
        items: [
          {field: "name", type: "required", example: "John doe", detail: "name for your contact"},
          {field: "number", type: "required", example: "6285xxx or 085xxx", detail: "number for your contact"},
          {field: "country", type: "required", example: "ID, US, UK, etc", detail: "this field used to validate number. so, make sure country code is correct for your number"},
          {field: "gender", type: "optional", example: "M, W, O", detail: "M = Man, W = Woman, O = Other"},
          {field: "birthday", type: "optional", example: "2019-09-19", detail: "name for your contact"},
          {field: "profession", type: "optional", example: "manager", detail: "profession for your contact"},
          {field: "location", type: "optional", example: "jakarta", detail: "location for your contact"},
          {field: "greeting", type: "optional", example: "Mr, Mrs, Pak, Buk", detail: "used for template message"},
          {field: "additional", type: "optional", example: "bulk marketing 01", detail: "used for extra contact identification"},
        ]
      }
    };
  },
  mounted() {
    if (!this.contacts) {
      this.$store.dispatch("contacts/GET_CONTACTS");
    }
  },
  computed: {
    ...mapGetters({
      contacts: "contacts/contacts"
    }),
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
    fileChanged(file) {
      this.file = file;
      this.filename = file.name;
    },
    onSave() {
      let fileform = new FormData();
      fileform.append("file", this.file);
      this.$store.dispatch("contacts/IMPORT_CONTACTS", fileform);
      this.$refs.importcontact.close();
      this.file = null;
      this.filename = "";
    },
    onDelete() {
      this.$store.dispatch("contacts/DELETE_CONTACTS", this.selected);
    },
    refresh() {
      this.$store.dispatch("contacts/GET_CONTACTS");
    }
  }
};
</script>

<style>
</style>
