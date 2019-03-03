<template>
  <div id="pageContacts">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg10 sm10 xs10>
          <v-card>
            <v-toolbar card dense color="transparent">
              <v-btn
                v-if="selected.length > 0"
                flat
                small
                outline
                color="red"
                @click="deleteContacts"
              >delete selected ({{selected.length}})</v-btn>
              <!-- add contact -->
              <v-dialog v-model="dialog.contact" max-width="500px" scrollable>
                <template v-slot:activator="{ on }">
                  <v-btn flat small outline color="primary" v-on="on">add new</v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="headline">New Contact</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container grid-list-md>
                      <v-layout row wrap>
                        <v-flex xs12 sm12 md12>
                          <v-text-field v-model="newcontact.name" label="Name"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm12 md12>
                          <vue-tel-input
                            v-model="newcontact.number"
                            :defaultCountry="'id'"
                            :preferredCountries="['id','en','us']"
                          ></vue-tel-input>
                        </v-flex>
                        <v-flex xs8 sm8 md8>
                          <v-select
                            v-model="newcontact.group"
                            v-validate="'required'"
                            :items="groupList"
                            :error-messages="errors.collect('group')"
                            label="Group"
                            data-vv-name="group"
                            required
                          ></v-select>
                        </v-flex>
                        <v-flex xs4 sm4 md4>
                          <v-dialog v-model="dialog.group" max-width="500px" scrollable>
                            <template v-slot:activator="{ on }">
                              <v-btn flat large outline color="primary" v-on="on">add new</v-btn>
                            </template>
                            <v-card>
                              <v-card-title>
                                <span class="headline">New Group</span>
                              </v-card-title>

                              <v-card-text>
                                <v-container grid-list-md>
                                  <v-layout row wrap>
                                    <v-flex xs12 sm12 md12>
                                      <v-text-field v-model="newgroup.name" label="Group Name"></v-text-field>
                                    </v-flex>
                                  </v-layout>
                                </v-container>
                              </v-card-text>

                              <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue darken-1" flat @click="closeGroup">Cancel</v-btn>
                                <v-btn color="blue darken-1" flat @click="saveGroup">Save</v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-dialog>
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
                  v-model="selected"
                  :headers="headers"
                  :items="contacts"
                  :search="search"
                  item-key="id"
                  select-all
                  class="elevation-1"
                >
                  <template slot="items" slot-scope="props">
                    <td>
                      <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
                    </td>
                    <td class="text-xs-left">{{ props.item.name }}</td>
                    <td class="text-xs-left">{{ props.item.number }}</td>
                    <td class="text-xs-left">{{ props.item.is_active }}</td>
                    <td class="text-xs-left">{{ groups(props.item.group).name }}</td>
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
  middleware: "auth",
  data() {
    return {
      search: "",
      selected: [],
      headers: [
        { text: "NAME", value: "name", align: "left" },
        { text: "NUMBER", value: "number", align: "left" },
        { text: "STATUS", value: "status", align: "left", sortable: true },
        { text: "GROUP", value: "group", align: "left", sortable: true }
      ],
      newcontact: {
        name: "",
        number: "",
        group: null
      },
      newgroup: {
        name: ""
      },
      dialog: {
        contact: false,
        group: false
      }
    };
  },
  mounted() {
    this.$store.dispatch("contacts/GET_CONTACTS");
    this.$store.dispatch("contacts/GET_GROUPS");
  },
  computed: {
    ...mapGetters({
      getContacts: "contacts/contacts",
      getGroups: "contacts/groups",
      getDetailGroup: "contacts/groupsById"
    }),
    contacts() {
      return this.getContacts.length > 0 ? this.getContacts : [];
    },
    groupList() {
      let groups = [];
      this.getGroups.map(group => {
        groups.push({ text: group.name, value: group.id });
      });
      return groups;
    }
  },
  methods: {
    groups(id) {
      return this.getDetailGroup(id);
    },
    validatedNumber(number) {
      return number
        .toString()
        .replace(/\s/g, "")
        .replace("+", "");
    },
    close() {
      this.dialog.contact = false;
      this.newcontact.name = "";
      this.newcontact.number = "";
      this.newcontact.group = null;
      this.$validator.reset();
    },
    closeGroup() {
      this.dialog.group = false;
      this.newgroup.name = "";
    },
    save() {
      let payload = {
        name: this.newcontact.name,
        number: this.validatedNumber(this.newcontact.number),
        group: this.newcontact.group
      };
      this.$store.dispatch("contacts/POST_CONTACTS", payload);
      this.close();
    },
    saveGroup() {
      let payload = {
        name: this.newgroup.name
      };
      this.$store.dispatch("contacts/POST_GROUPS", payload);
      this.closeGroup();
    },
    deleteContacts() {
      this.$store.dispatch("contacts/DELETE_CONTACTS", this.selected);
      this.selected = [];
    }
  }
};
</script>