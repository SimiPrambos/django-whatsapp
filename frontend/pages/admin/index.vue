<template>
  <div id="pageAdmin">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <!-- active -->
        <v-flex lg12 sm12 xs12>
          <v-card>
            <v-toolbar card dense color="transparent">
              <v-btn v-if="selectedActive.length > 0" flat outline color="red" @click="setInactive">
                <v-icon left>mdi-account-off</v-icon>
                set inactive ({{selectedActive.length===(usersActive.length)?"ALL":selectedActive.length}})
              </v-btn>
              <v-card-title v-else>
                <v-icon left>mdi-account</v-icon>
                <span class="title font-weight-light">Active users</span>
              </v-card-title>
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
              <div>
                <v-data-table
                  v-model="selectedActive"
                  :headers="headers"
                  :items="usersActive"
                  :search="search"
                  hide-actions
                  item-key="id"
                  select-all
                  :pagination.sync="pagination"
                  class="elevation-1"
                >
                  <template v-slot:items="props">
                    <td>
                      <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
                    </td>
                    <td class="text-xs-left">{{ props.item.username }}</td>
                    <td class="text-xs-left">{{ props.item.email }}</td>
                    <td class="text-xs-left">{{ formateDate(props.item.api_expired) }}</td>
                    <td class="text-xs-center">
                      <v-dialog v-model="dialog" max-width="500px" scrollable>
                        <template v-slot:activator="{ on }">
                          <v-btn small outline color="green" v-on="on">renew api expiration</v-btn>
                        </template>
                        <v-card>
                          <v-card-title>
                            <span class="headline">Renew Api Expiration</span>
                          </v-card-title>

                          <v-card-text>
                            <v-container fluid grid-list-md>
                              <v-layout row wrap>
                                <v-flex>
                                  <v-text-field
                                    :value="formateDate(props.item.api_expired)"
                                    readonly
                                    label="Current date expired"
                                    prepend-icon="event"
                                  ></v-text-field>
                                </v-flex>
                                <v-flex>
                                  <v-menu
                                    ref="menu"
                                    v-model="menu"
                                    :close-on-content-click="false"
                                    :nudge-right="40"
                                    :return-value.sync="newExpiration"
                                    lazy
                                    transition="scale-transition"
                                    offset-y
                                    full-width
                                    min-width="290px"
                                  >
                                    <template v-slot:activator="{ on }">
                                      <v-text-field
                                        v-model="dateFormatted"
                                        label="New date expired"
                                        prepend-icon="event"
                                        readonly
                                        v-on="on"
                                      ></v-text-field>
                                    </template>
                                    <v-date-picker v-model="date" no-title scrollable>
                                      <v-spacer></v-spacer>
                                      <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                                      <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                                    </v-date-picker>
                                  </v-menu>
                                </v-flex>
                              </v-layout>
                            </v-container>
                          </v-card-text>

                          <v-card-actions>
                            <v-btn flat outline block color="red" @click="dialog=false">Close</v-btn>
                            <v-btn
                              flat
                              outline
                              block
                              color="blue"
                              @click="setExpiration(props.item.id)"
                            >Save</v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-dialog>
                    </td>
                  </template>
                </v-data-table>
                <div class="text-xs-center pt-2">
                  <v-pagination v-model="pagination.page" :length="pages"></v-pagination>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- Inactive -->
        <v-flex lg12 sm12 xs12>
          <v-card>
            <v-toolbar card dense color="transparent">
              <div v-if="selectedInactive.length > 0">
                <v-btn flat outline color="green" @click="setActive">
                  <v-icon left>mdi-account</v-icon>
                  set to active ({{selectedInactive.length===(usersInactive.length)?"ALL":selectedInactive.length}})
                </v-btn>
                <v-btn flat outline color="red" @click="deleteUsers">
                  <v-icon left>delete</v-icon>
                  delete ({{selectedInactive.length===(usersInactive.length)?"ALL":selectedInactive.length}})
                </v-btn>
              </div>
              <v-card-title v-else>
                <v-icon left>mdi-account-off</v-icon>
                <span class="title font-weight-light">Inactive users</span>
              </v-card-title>
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
              <div>
                <v-data-table
                  v-model="selectedInactive"
                  :headers="headers"
                  :items="usersInactive"
                  :search="search"
                  hide-actions
                  item-key="id"
                  select-all
                  :pagination.sync="pagination"
                  class="elevation-1"
                >
                  <template v-slot:items="props">
                    <td>
                      <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
                    </td>
                    <td class="text-xs-left">{{ props.item.username }}</td>
                    <td class="text-xs-left">{{ props.item.email }}</td>
                    <td class="text-xs-left">{{ formateDate(props.item.api_expired) }}</td>
                  </template>
                </v-data-table>
                <div class="text-xs-center pt-2">
                  <v-pagination v-model="pagination.page" :length="pages"></v-pagination>
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

export default {
  layout: "dashboard",
  middleware: "admin",
  data() {
    return {
      headers: [
        { text: "USERNAME", align: "left", sortable: true, value: "username" },
        { text: "EMAIL", align: "left", sortable: true, value: "email" },
        {
          text: "EXPIRED API ACCESS",
          align: "left",
          sortable: true,
          value: "api_expired"
        },
        { text: "Action", align: "center", value: "action" }
      ],
      search: "",
      pagination: {},
      selectedActive: [],
      selectedInactive: [],
      newExpiration: "",
      date: new Date().toISOString().substr(0, 10),
      dialog: false,
      menu: false
    };
  },
  mounted() {
    this.$store.dispatch("admin/GET_USERS");
  },
  computed: {
    ...mapGetters({
      users: "admin/users",
      usersActive: "admin/usersActive",
      usersInactive: "admin/usersInactive"
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
    },
    dateFormatted() {
      return this.formateDate(this.date);
    }
  },
  methods: {
    formateDate(string) {
      return string ? new Date(string).toLocaleDateString() : "";
    },
    setInactive() {
      this.selectedActive.map(user => {
        this.$store.dispatch("admin/PUT_USERS_ACTIVE", {
          id: user.id,
          data: { username: user.username, is_active: false }
        });
      });
    },
    setActive() {
      this.selectedInactive.map(user => {
        this.$store.dispatch("admin/PUT_USERS_ACTIVE", {
          id: user.id,
          data: { username: user.username, is_active: true }
        });
      });
    },
    deleteUsers() {
      this.selectedInactive.map(user => {
        this.$store.dispatch("admin/DELETE_USERS", user.id);
      });
    },
    setExpiration(id) {
      let user = this.users.find(u => u.id === id);
      this.$store.dispatch("admin/PUT_EXPIRATION", {
        id: user.id,
        data: { username: user.username, api_expired: this.newExpiration }
      });
      this.dialog = false;
      this.newExpiration = "";
    }
  }
};
</script>

<style>
</style>
