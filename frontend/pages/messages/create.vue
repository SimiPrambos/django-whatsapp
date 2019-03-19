<template>
  <div id="messageCreate">
    <v-container grid-list-xl fluid>
      <v-card class="mx-auto" max-width="1000">
        <v-card-title class="title font-weight-regular justify-space-between">
          <span>{{ currentTitle }}</span>
          <v-avatar
            color="primary lighten-2"
            class="subheading white--text"
            size="24"
            v-text="step"
          ></v-avatar>
        </v-card-title>

        <v-window v-model="step">
          <v-window-item :value="1">
            <v-card-text>
              <v-select
                v-model="messages.from"
                :items="selectNumbers"
                label="Select your number"
                prepend-icon="mdi-whatsapp"
              ></v-select>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2">
            <v-card-text>
              <v-checkbox v-model="multiple" label="Multiple?"></v-checkbox>
              <div v-if="!multiple">
                <vue-tel-input
                  v-model="messages.to"
                  :defaultCountry="'id'"
                  :preferredCountries="['id']"
                ></vue-tel-input>
              </div>
              <div v-else>
                <v-layout row wrap>
                  <v-flex sm6>
                    <v-autocomplete
                      v-model="myFilter.gender"
                      :items="selectGender"
                      label="Gender"
                      @change="setFilter(myFilter.gender, 'gen')"
                    ></v-autocomplete>
                  </v-flex>
                  <v-flex sm6>
                    <v-autocomplete
                      v-model="myFilter.location"
                      :items="locations"
                      label="Location"
                      @change="setFilter(myFilter.location, 'loc')"
                    ></v-autocomplete>
                  </v-flex>
                  <v-flex sm6>
                    <v-autocomplete
                      v-model="myFilter.profession"
                      :items="professions"
                      label="Professions"
                      @change="setFilter(myFilter.profession, 'prof')"
                    ></v-autocomplete>
                  </v-flex>
                </v-layout>
                <v-chip outline :color="filteredContact.length>0?'green':'red'" label>
                  <v-avatar>
                    <v-icon>mdi-account-multiple-outline</v-icon>
                  </v-avatar>
                  {{filteredContact.length}} contact found
                </v-chip>
              </div>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="3">
            <v-card-text>
              <v-textarea
                v-model="messages.content"
                label="Input message"
                auto-grow
                clearable
                prepend-inner-icon="edit"
              ></v-textarea>
              <v-select
                v-model="messages.media"
                :items="selectMedia"
                label="With media file (optional)"
                prepend-inner-icon="perm_media"
              ></v-select>
            </v-card-text>
          </v-window-item>
        </v-window>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn :disabled="step === 1" flat @click="step--">Back</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            v-if="step === 1"
            :disabled="!messages.from"
            color="primary"
            depressed
            @click="step++"
          >Next</v-btn>
          <v-btn
            v-else-if="step === 2"
            :disabled="multiple ? filteredContact.length <= 0 : !messages.to"
            color="primary"
            depressed
            @click="step++"
          >Next</v-btn>
          <v-btn
            v-else-if="step === 3"
            :disabled="!messages.content"
            color="primary"
            depressed
            @click="send"
          >Send</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  layout: "dashboard",
  middleware: "auth",
  data: () => ({
    step: 1,
    multiple: false,
    filterBy: [],
    myFilter: {
      gender: "",
      location: "",
      profession: "",
      birthday: ""
    },
    filteredContact: [],
    messages: {
      from: null,
      media: null,
      to: null,
      content: null
    }
  }),
  mounted() {
    this.$store.dispatch("numbers/GET_NUMBERS");
    this.$store.dispatch("contacts/GET_CONTACTS");
    this.$store.dispatch("media/GET_MEDIA");
    this.filteredContact = this.contacts;
  },
  computed: {
    ...mapGetters({
      numbers: "numbers/numbers",
      contacts: "contacts/contacts",
      locations: "contacts/locations",
      professions: "contacts/professions",
      media: "media/media"
    }),
    currentTitle() {
      switch (this.step) {
        case 1:
          return "Send From";
        case 2:
          return "Send To";
        case 3:
          return "Message";
        default:
          return "Account created";
      }
    },
    selectNumbers() {
      let numberlist = [];
      this.numbers.map(number => {
        numberlist.push({ text: number.lable, value: number.id });
      });
      return numberlist;
    },
    selectMedia() {
      let medialist = [];
      this.media.map(med => {
        medialist.push({ text: med.filename, value: med.id });
      });
      return medialist;
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
    clear() {
      this.multiple = false;
      this.messages.from = null;
      this.messages.to = null;
      this.messages.media = null;
      this.messages.content = null;
      this.step = 1;
    },
    send() {
      let payload = {
        numberId: this.messages.from,
        media: this.messages.media,
        messages: []
      };
      let contacts = [];
      this.multiple
        ? this.filteredContact.map(contact => {
            contacts.push(contact.number);
          })
        : contacts.push(this.validateNumber(this.messages.to));
      contacts.map(contact => {
        payload.messages.push({
          message_number: contact,
          message_content: this.messages.content
        });
      });
      this.$store.dispatch("messages/POST_MESSAGES", payload);
      this.clear();
    },
    setFilter(value, type) {
      let index = null;
      switch (type) {
        case "gen":
          index = 1;
          break;
        case "loc":
          index = 2;
          break;
        case "prof":
          index = 3;
          break;
        default:
          break;
      }
      this.filterBy[index] = value;
      this.filterContact();
    },
    filterContact() {
      this.filteredContact = this.contacts.filter(contact => {
        return this.filterBy.every(filterby => {
          if (contact.gender && contact.gender.includes(filterby)) {
            return contact.gender.includes(filterby);
          }
          if (contact.location && contact.location.includes(filterby)) {
            return contact.location.includes(filterby);
          }
          if (contact.profession && contact.profession.includes(filterby)) {
            return contact.profession.includes(filterby);
          }
        });
      });
    }
  }
};
</script>