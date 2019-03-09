<template>
  <div id="newContact">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg4 sm4 xs4>
          <v-card flat>
            <v-toolbar card dense color="transparent">
              <v-toolbar-title>Groups</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="pa-0">
              <v-list>
                <template v-for="(group, index) in groups">
                  <v-divider></v-divider>
                  <v-list-tile :key="index" @click="currentGroup = group">
                    <v-list-tile-action>
                      <v-btn flat icon>
                        <v-icon>delete</v-icon>
                      </v-btn>
                    </v-list-tile-action>
                    <v-list-tile-content>{{group.name.toUpperCase()}}</v-list-tile-content>
                  </v-list-tile>
                </template>
              </v-list>
              <v-btn flat outline block color="blue">add group</v-btn>
            </v-card-text>
          </v-card>
        </v-flex>
        <v-flex lg8 sm8 xs8>
          <v-card flat>
            <v-toolbar card dense color="transparent">
              <v-btn
                v-if="selected.length > 0"
                flat
                outline
                color="red"
              >Delete selected ({{selected.length}})</v-btn>
              <v-btn
                flat
                outline
                color="blue"
              >add contact</v-btn>
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
                  :items="currentGroup? ContactsByGroup(currentGroup.id) : []"
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
                  </template>
                  <v-alert
                    slot="no-results"
                    :value="true"
                    color="error"
                    icon="warning"
                  >No results for "{{ search }}".</v-alert>
                </v-data-table>
              </template>
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
  data: () => ({
    length: 3,
    window: 0,
    search: "",
    selected: [],
    currentGroup: null,
    headers: [
      { text: "NAME", value: "name", align: "left" },
      { text: "NUMBER", value: "number", align: "left" },
      { text: "STATUS", value: "status", align: "left", sortable: true }
    ]
  }),
  mounted() {
    this.$store.dispatch("contacts/GET_CONTACTS");
    this.$store.dispatch("contacts/GET_GROUPS");
  },
  computed: {
    ...mapGetters({
      contacts: "contacts/contacts",
      ContactsByGroup: "contacts/contactsByGroup",
      groups: "contacts/groups"
    })
  }
};
</script>