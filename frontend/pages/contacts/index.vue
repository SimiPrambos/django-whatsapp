<template>
  <div id="newContact">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg4 sm4 xs12>
          <v-card flat>
            <v-toolbar card dense color="transparent">
              <v-toolbar-title>Category</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="pa-0">
              <v-list>
                <v-list-tile
                  @click="currentCategory = null"
                  :color="!currentCategory?'blue':'black'"
                >
                  <v-list-tile-content>ALL</v-list-tile-content>
                  <v-list-tile-action v-if="currentCategory === null">
                    <v-btn flat icon color="blue">
                      <v-icon>chevron_right</v-icon>
                    </v-btn>
                  </v-list-tile-action>
                </v-list-tile>
                <template v-for="(category, index) in category">
                  <v-list-tile
                    :key="index"
                    @click="currentCategory = category"
                    :color="category === currentCategory?'blue':'black'"
                  >
                    <v-list-tile-content>{{category.name.toUpperCase()}}</v-list-tile-content>
                    <v-list-tile-action v-if="category === currentCategory">
                      <v-btn flat icon color="blue">
                        <v-icon>chevron_right</v-icon>
                      </v-btn>
                    </v-list-tile-action>
                  </v-list-tile>
                </template>
              </v-list>
            </v-card-text>
            <v-card-actions>
              <form-dialog
                title="Add Category"
                label="Add Category"
                color="blue"
                icon="add"
                :block="true"
                :onSave="addCategory"
                ref="addcategory"
              >
                <template v-slot:form>
                  <v-flex>
                    <v-text-field v-model="newCategory" label="Name"></v-text-field>
                  </v-flex>
                </template>
              </form-dialog>
            </v-card-actions>
          </v-card>
        </v-flex>
        <v-flex lg8 sm8 xs12>
          <v-card flat>
            <v-toolbar card dense color="transparent">
              <v-btn v-if="selected.length > 0" flat outline color="red">
                <v-icon>delete</v-icon>
                delete ({{selected.length===(!currentCategory?contacts.length: contactsByCategory(currentCategory.id).length||0)?"ALL":selected.length}})
              </v-btn>
              <form-dialog
                title="Add Contact"
                label="add"
                color="blue"
                icon="add"
                :onSave="addContact"
                ref="addcontact"
              >
                <template v-slot:form>
                  <v-flex>
                    <v-text-field v-model="newContact.name" label="Name"></v-text-field>
                  </v-flex>
                  <v-flex>
                    <vue-tel-input
                      v-model="newContact.number"
                      :defaultCountry="'id'"
                      :preferredCountries="['id','en','us']"
                    ></vue-tel-input>
                  </v-flex>
                  <v-flex>
                    <v-select
                      v-model="newContact.category"
                      :items="selectCategory"
                      multiple
                      chips
                      label="Category"
                    ></v-select>
                  </v-flex>
                  <v-flex xs12 md12 lg12>
                    <p>
                      <em>Optional :</em>
                    </p>
                  </v-flex>
                  <v-flex xs6 md6 lg6>
                    <v-menu
                      v-model="selectBirthday"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      lazy
                      transition="scale-transition"
                      offset-y
                      full-width
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on }">
                        <v-text-field
                          v-model="newContact.birthday"
                          label="Birthday"
                          readonly
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-date-picker v-model="newContact.birthday" @input="selectBirthday = false"></v-date-picker>
                    </v-menu>
                  </v-flex>
                  <v-flex xs6 md6 lg6>
                    <v-select v-model="newContact.gender" :items="selectGender" label="Gander"></v-select>
                  </v-flex>
                  <v-flex xs6 md6 lg6>
                    <v-text-field v-model="newContact.profession" label="profession"></v-text-field>
                  </v-flex>
                  <v-flex xs6 md6 lg6>
                    <v-text-field v-model="newContact.location" label="location"></v-text-field>
                  </v-flex>
                </template>
              </form-dialog>
              <v-btn flat outline color="blue">
                <v-icon>mdi-import</v-icon>import
              </v-btn>
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
                  :items="!currentCategory? contacts: contactsByCategory(currentCategory.id)"
                  :search="search"
                  item-key="id"
                  select-all
                  class="elevation-1"
                >
                  <template v-slot:items="props">
                    <tr @click="props.expanded = !props.expanded">
                      <td>
                        <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
                      </td>
                      <td class="text-xs-left">{{ props.item.name }}</td>
                      <td class="text-xs-left">{{ props.item.number }}</td>
                      <td class="text-xs-left">{{ props.item.is_active }}</td>
                    </tr>
                  </template>
                  <template v-slot:expand="props">
                    <v-card flat>
                      <v-card-text>Peek-a-boo!</v-card-text>
                    </v-card>
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
import FormDialog from "@/components/contacts/FormDialog";
export default {
  layout: "dashboard",
  middleware: "auth",
  components: {
    FormDialog
  },
  data: () => ({
    length: 3,
    window: 0,
    search: "",
    expand: false,
    selected: [],
    selectBirthday: false,
    currentCategory: null,
    newCategory: null,
    newContact: {
      name: "",
      number: "",
      category: [],
      gander: "",
      birthday: new Date().toISOString().substr(0, 10),
      profession: "",
      location: ""
    },
    headers: [
      { text: "NAME", value: "name", align: "left" },
      { text: "NUMBER", value: "number", align: "left" },
      { text: "STATUS", value: "status", align: "left", sortable: true }
    ]
  }),
  mounted() {
    this.$store.dispatch("contacts/GET_CONTACTS");
    this.$store.dispatch("contacts/GET_CATEGORY");
  },
  computed: {
    ...mapGetters({
      contacts: "contacts/contacts",
      contactsByCategory: "contacts/contactsByCategory",
      category: "contacts/category"
    }),
    selectCategory() {
      let listcategory = [];
      this.category.map(cat => {
        listcategory.push({ text: cat.name, value: cat.id });
      });
      return listcategory;
    },
    selectGender() {
      return [
        { text: "Man", value: "M" },
        { text: "Woman", value: "W" },
        { text: "Other", value: "O" }
      ];
    }
  },
  methods: {
    validateNumber(number) {
      return number
        .toString()
        .replace(/\s/g, "")
        .replace("+", "");
    },
    addCategory() {
      this.$store.dispatch("contacts/POST_CATEGORY", {
        name: this.newCategory
      });
      this.$refs.addcategory.close();
    },
    addContact() {
      let payload = this.newContact;
      payload.number = this.validateNumber(payload.number);
      this.$store.dispatch("contacts/POST_CONTACTS", payload);
      this.$refs.addcontact.close();
    }
  }
};
</script>