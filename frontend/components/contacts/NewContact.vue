<template>
  <form-dialog
    title="Add new contact"
    label="add"
    color="blue"
    icon="add"
    :onSave="onSave"
    ref="addcontact"
  >
    <template v-slot:form>
      <v-flex lg12 sm12 xs12>
        <v-text-field v-model="contact.name" label="name"></v-text-field>
      </v-flex>
      <v-flex lg12 sm12 xs12>
        <vue-tel-input
          v-model="contact.number"
          :defaultCountry="'id'"
          :preferredCountries="['id']"
          @onInput="onInput"
        ></vue-tel-input>
      </v-flex>
      <v-flex lg12 sm12 xs12>
        <v-checkbox v-model="contact.is_friend" label="is friend?"></v-checkbox>
      </v-flex>
      <!-- optional -->
      <v-flex lg12 sm12 xs12>
        <p>
          <em>optionals:</em>
        </p>
      </v-flex>
      <v-flex lg6 sm6 xs6>
        <v-select v-model="contact.gender" label="gender"></v-select>
      </v-flex>
      <v-flex lg6 sm6 xs6>
        <v-menu
          v-model="menu"
          ref="birthday"
          :close-on-content-click="false"
          :nudge-right="40"
          :return-value.sync="contact.birthday"
          lazy
          transition="scale-transition"
          offset-y
          full-width
          min-width="290px"
        >
          <template v-slot:activator="{ on }">
            <v-text-field
              v-model="contact.birthday"
              label="Birthday"
              prepend-icon="event"
              readonly
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker v-model="date" no-title scrollable>
            <v-spacer></v-spacer>
            <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
            <v-btn flat color="primary" @click="$refs.birthday.save(date)">OK</v-btn>
          </v-date-picker>
        </v-menu>
      </v-flex>
      <v-flex lg6 sm6 xs6>
        <v-text-field v-model="contact.profession" label="profession"></v-text-field>
      </v-flex>
      <v-flex lg6 sm6 xs6>
        <v-text-field v-model="contact.location" label="location"></v-text-field>
      </v-flex>
      <v-flex lg12 sm12 xs12>
        <v-text-field v-model="contact.greeting" label="greeting"></v-text-field>
      </v-flex>
      <v-flex lg12 sm12 xs12>
        <v-text-field v-model="contact.additional" label="additional"></v-text-field>
      </v-flex>
    </template>
  </form-dialog>
</template>

<script>
import FormDialog from "@/components/contacts/FormDialog";
const defaultContact = {
  name: "",
  number: "",
  country: "",
  is_friend: false,
  gender: "",
  birthday: "",
  profession: "",
  location: "",
  additional: "",
  greeting: ""
};
export default {
  components: {
    FormDialog
  },
  data() {
    return {
      contact: defaultContact,
      menu: false,
      date: new Date().toISOString().substr(0, 10)
    };
  },
  methods: {
    validateNumber(number) {
      return number
        .toString()
        .replace(/\s/g, "")
        .replace("+", "");
    },
    onInput({ number, isValid, country }) {
      this.contact.country = country.iso2;
      this.contact.number = number;
    },
    onSave() {
      this.contact.birthday = this.contact.birthday
        ? this.contact.birthday
        : null;
      this.contact.number = this.validateNumber(this.contact.number);
      this.$store.dispatch("contacts/POST_CONTACTS", this.contact);
      this.$refs.addcontact.close();
    }
  }
};
</script>

<style>
</style>
