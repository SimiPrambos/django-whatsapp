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
              <v-select
                v-model="messages.to"
                :items="selectCategory"
                label="Category contacts"
                prepend-icon="contacts"
              ></v-select>
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
          <v-btn :disabled="step === 3" color="primary" depressed @click="step++">Next</v-btn>
          <v-btn v-if="step===3" flat outline color="blue" @click="send">Send</v-btn>
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
    this.$store.dispatch("contacts/GET_CATEGORY");
    this.$store.dispatch("media/GET_MEDIA");
  },
  computed: {
    ...mapGetters({
      numbers: "numbers/numbers",
      contacts: "contacts/contacts",
      category: "contacts/category",
      contactsByCategory: "contacts/contactsByCategory",
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
    selectCategory() {
      let categorylist = [];
      this.category.map(cat => {
        categorylist.push({ text: cat.name, value: cat.name });
      });
      return categorylist;
    },
    selectMedia() {
      let medialist = [];
      this.media.map(med => {
        medialist.push({ text: med.filename, value: med.id });
      });
      return medialist;
    }
  },
  methods: {
    clear() {
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
      this.contactsByCategory(this.messages.to).map(contact => {
        payload.messages.push({
          message_number: contact.number,
          message_content: this.messages.content
        });
      });
      this.$store.dispatch("messages/POST_MESSAGES", payload);
      this.clear();
    }
  }
};
</script>