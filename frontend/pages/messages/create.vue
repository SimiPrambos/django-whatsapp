<template>
  <div id="pageCreateMessage">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg5 sm5 xs12>
          <v-card>
            <v-card-title primary-title>
              <div>
                <h3 class="headline mb-0">Shortcut Message</h3>
              </div>
            </v-card-title>
            <v-card-text>
              <template>
                <form>
                  <v-select
                    v-model="message.from"
                    v-validate="'required'"
                    :items="items"
                    :error-messages="errors.collect('number')"
                    label="Send From"
                    data-vv-name="number"
                    required
                  ></v-select>
                  <br>
                  <vue-tel-input
                    v-model="message.to"
                    :defaultCountry="'id'"
                    :preferredCountries="['id']"
                  ></vue-tel-input>
                  <br>
                  <v-select v-model="message.media" :items="mediaList" label="Media File"></v-select>
                  <v-textarea
                    v-model="message.message"
                    outline
                    name="input-7-4"
                    label="Message"
                    value
                  ></v-textarea>
                  <v-btn @click="clear('one')" flat outline color="red">clear</v-btn>
                  <v-btn @click="send('one')" flat outline color="blue">Send</v-btn>
                </form>
              </template>
            </v-card-text>
          </v-card>
        </v-flex>

        <v-flex lg7 sm7 xs12>
          <v-card>
            <v-card-title primary-title>
              <div>
                <h3 class="headline mb-0">Multiple Message</h3>
              </div>
            </v-card-title>
            <v-card-text>
              <template>
                <form>
                  <v-select
                    v-model="multiMessage.from"
                    v-validate="'required'"
                    :items="items"
                    :error-messages="errors.collect('number')"
                    label="Send From"
                    data-vv-name="number"
                    required
                  ></v-select>
                  <v-select
                    v-model="multiMessage.group"
                    v-validate="'required'"
                    :items="groupList"
                    :error-messages="errors.collect('group')"
                    label="Group Contact"
                    data-vv-name="group"
                    required
                  ></v-select>
                  <v-select v-model="multiMessage.media" :items="mediaList" label="Media File"></v-select>
                  <v-textarea
                    v-model="multiMessage.message"
                    outline
                    name="input-7-4"
                    label="Message"
                    value
                  ></v-textarea>
                  <v-btn @click="clear('multi')" flat outline color="red">clear</v-btn>
                  <v-btn @click="send('multi')" flat outline color="blue">Send</v-btn>
                </form>
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
  data() {
    return {
      message: {
        from: null,
        to: "",
        message: "",
        media: null
      },
      multiMessage: {
        from: null,
        group: null,
        message: "",
        media: null
      }
    };
  },
  computed: {
    ...mapGetters({
      LoggedInNumber: "numbers/numbersIsLoggedIn",
      getGroups: "contacts/groups",
      getContactsFromGroup: "contacts/contactsByGroup",
      media: "media/media"
    }),
    items() {
      let numbers = [];
      this.LoggedInNumber.map(number => {
        numbers.push({ text: number.lable, value: number.id });
      });
      return numbers;
    },
    groupList() {
      let groups = [];
      this.getGroups.map(group => {
        groups.push({ text: group.name, value: group.id });
      });
      return groups;
    },
    mediaList() {
      let files = [];
      this.media.map(file => {
        files.push({ text: file.filename, value: file.id });
      });
      return files;
    }
  },
  methods: {
    validatedNumber(number) {
      return number
        .toString()
        .replace(/\s/g, "")
        .replace("+", "");
    },
    clear(type) {
      if (type === "one") {
        this.message.from = "";
        this.message.to = "";
        this.message.message = "";
        this.message.media = null;
      } else if (type === "multi") {
        this.multiMessage.from = null;
        this.multiMessage.group = null;
        this.multiMessage.message = null;
        this.multiMessage.media = null;
      }
      this.$validator.reset();
    },
    send(type) {
      let payload = {
        numberId: null,
        media: null,
        messages: []
      };
      if (type === "one") {
        payload.numberId = this.message.from;
        payload.media = this.message.media;
        payload.messages.push({
          message_number: this.validatedNumber(this.message.to),
          message_content: this.message.message
        });
      } else if (type === "multi") {
        payload.numberId = this.multiMessage.from;
        payload.media = this.multiMessage.media;
        let numbers = this.getContactsFromGroup(this.multiMessage.group);
        numbers.map(number => {
          payload.messages.push({
            message_number: this.validatedNumber(number.number),
            message_content: this.multiMessage.message
          });
        });
      }
      this.$store.dispatch("messages/POST_MESSAGES", payload);
      this.clear(type);
    }
  }
};
</script>

