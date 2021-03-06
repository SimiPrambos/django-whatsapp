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
                label="Choose your whatsapp number"
                hint="you can select more then one."
                persistent-hint
                prepend-icon="mdi-whatsapp"
                multiple
                chips
                @change="messages.from.length > 1? multiple = true : multiple = false"
              ></v-select>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2">
            <v-card-text>
              <v-layout row wrap>
                <v-flex lg6 sm6 xs12>
                  <v-checkbox
                    v-model="multiple"
                    label="Multiple contact?"
                    :disabled="messages.from.length > 1"
                  ></v-checkbox>
                </v-flex>
                <v-flex lg6 sm6 xs12>
                  <v-checkbox v-model="includeFriend">
                    <span slot="label">
                      Include friend list? (used for blocking anticipation). click
                      <a
                        href="/messages/friends"
                      >here</a> to manage your friend number and message
                    </span>
                  </v-checkbox>
                </v-flex>
              </v-layout>
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
                  <v-flex sm6>
                    <v-autocomplete
                      v-model="myFilter.profession"
                      :items="additionals"
                      label="Additionals"
                      @change="setFilter(myFilter.profession, 'adt')"
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
              <v-layout row wrap>
                <v-flex lg6 sm6 xs12 v-for="(item, index) in messages.content" :key="index">
                  <v-card>
                    <v-card-text>
                      <v-textarea
                        v-model="messages.content[index].text"
                        :label="'Message '+(index+1)"
                        auto-grow
                        clearable
                      ></v-textarea>
                      <v-item-group multiple>
                        <v-subheader>Text Formatting</v-subheader>
                        <v-item>
                          <v-chip>
                            <i>italic</i> : _text_
                          </v-chip>
                        </v-item>
                        <v-item>
                          <v-chip>
                            <b>bold</b> : *text*
                          </v-chip>
                        </v-item>
                        <v-item>
                          <v-chip>
                            <strike>strikerough</strike>: ~text~
                          </v-chip>
                        </v-item>
                      </v-item-group>
                      <v-item-group multiple v-if="multiple">
                        <v-subheader>Available template</v-subheader>
                        <v-item>
                          <v-chip>
                            <span v-pre>{{greeting}}</span>
                          </v-chip>
                        </v-item>
                        <v-item>
                          <v-chip>
                            <span v-pre>{{name}}</span>
                          </v-chip>
                        </v-item>
                        <v-item>
                          <v-chip>
                            <span v-pre>{{number}}</span>
                          </v-chip>
                        </v-item>
                        <v-item>
                          <v-chip label>
                            <span v-pre>example: Hello {{greeting}} {{name}}, are you fine?</span>
                          </v-chip>
                        </v-item>
                        <v-item>
                          <v-chip label>
                            <span>output: Hello Mr John, are you fine?</span>
                          </v-chip>
                        </v-item>
                      </v-item-group>
                      <v-select
                        v-model="messages.content[index].media"
                        :items="selectMedia"
                        label="With media file (optional)"
                        prepend-inner-icon="perm_media"
                      ></v-select>
                      <v-btn
                        flat
                        outline
                        block
                        color="red"
                        @click="messages.content.splice(index, 1)"
                        :disabled="messages.content.length <= 1"
                      >remove</v-btn>
                    </v-card-text>
                  </v-card>
                </v-flex>
                <v-flex lg12 sm12 xs12>
                  <v-btn
                    flat
                    outline
                    color="blue"
                    @click="messages.content.push({text:'Hello, how are you?', media:null})"
                    :disabled="!multiple || filteredContact.length === messages.content.length"
                  >add more message</v-btn>
                </v-flex>
              </v-layout>
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
  middleware: ["auth", "HasApiAccess"],
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
      from: [],
      to: "",
      content: [{ text: "Hello, are you fine?", media: null }]
    },
    includeFriend: false
  }),
  mounted() {
    if (!this.numbers) {
      this.$store.dispatch("numbers/GET_NUMBERS");
    }
    if (!this.contacts) {
      this.$store.dispatch("contacts/GET_CONTACTS");
    }
    if (!this.media) {
      this.$store.dispatch("media/GET_MEDIA");
    }
    if (!this.friendMessages) {
      this.$store.dispatch("messages/GET_FRIEND_MESSAGES");
    }
    this.filteredContact = this.contacts;
  },
  computed: {
    ...mapGetters({
      numbers: "numbers/numbers",
      contacts: "contacts/contacts",
      locations: "contacts/locations",
      professions: "contacts/professions",
      additionals: "contacts/additionals",
      media: "media/media",
      friendContacts: "contacts/friends",
      friendMessages: "messages/friendMessages"
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
      this.messages.from = [];
      this.messages.to = "";
      this.messages.content = [{ text: "Hello, are you fine?", media: null }];
      this.step = 1;
    },
    getRandomFriendMessages() {
      let messages = [];
      if (this.friendContacts.length > 0 && this.friendMessages.length > 0) {
        this.friendContacts.map(contact => {
          messages.push({
            message_number: contact.number,
            message_content: this.friendMessages[
              Math.floor(Math.random() * Math.floor(this.friendMessages.length))
            ].message,
            template: contact
          });
        });
      }
      return messages;
    },
    send() {
      if (this.multiple) {
        let from = this.messages.from;
        let to = this.filteredContact;
        let contents = this.messages.content;
        let withMedia = [];
        let nonMedia = [];

        let div = parseInt(to.length / from.length);
        let rem = to.length % from.length;
        let nStep = 1;
        let cStep = 0;

        from.map((number, nIndex) => {
          let wMedia = {
            numberId: number,
            messages: []
          };
          let nMedia = {
            numberId: number,
            messages: []
          };
          let fStep = 0;
          to.map((contact, cIndex) => {
            let friendMsg = this.getRandomFriendMessages();
            if (this.includeFriend && friendMsg.length > 0) {
              if (cIndex % parseInt(to.length / friendMsg.length) === 0) {
                nMedia.messages.push(friendMsg[fStep]);
                fStep++;
              }
            }
            if (cIndex >= cStep && cIndex < div * nStep) {
              let content =
                contents[
                  Math.floor(Math.random() * Math.floor(contents.length))
                ];
              let message = {
                message_number: contact.number,
                message_content: content.text,
                template: contact
              };
              if (content.media) {
                message["message_media"] = content.media;
                wMedia.messages.push(message);
              } else {
                nMedia.messages.push(message);
              }
              cStep++;
            }
          });

          nStep++;
          if (nIndex === from.length - 1) {
            if (rem > 0) {
              to.slice(to.length - rem).map(contact => {
                let content =
                  contents[
                    Math.floor(Math.random() * Math.floor(contents.length))
                  ];
                let message = {
                  message_number: contact.number,
                  message_content: content.text,
                  template: contact
                };
                if (content.media) {
                  message["message_media"] = content.media;
                  wMedia.messages.push(message);
                } else {
                  nMedia.messages.push(message);
                }
              });
            }
          }
          withMedia.push(wMedia);
          nonMedia.push(nMedia);
        });

        nonMedia.map(messages => {
          if (messages)
            this.$store.dispatch("messages/POST_TEXT_MESSAGE", messages);
        });
        withMedia.map(messages => {
          if (messages)
            this.$store.dispatch("messages/POST_MEDIA_MESSAGE", messages);
        });
      } else {
        let payload = {
          numberId: this.messages.from[0],
          messages: [
            {
              message_number: this.validateNumber(this.messages.to),
              message_content: this.messages.content[0].text
            }
          ]
        };
        if (this.messages.content[0].media) {
          payload.messages[0]["message_media"] = this.messages.content[0].media;
          this.$store.dispatch("messages/POST_MEDIA_MESSAGE", payload);
        } else {
          this.$store.dispatch("messages/POST_TEXT_MESSAGE", payload);
        }
      }
      this.clear();
      this.$router.push("/messages/outbox");
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
        case "adt":
          index = 4;
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
          if (contact.additional && contact.additional.includes(filterby)) {
            return contact.additional.includes(filterby);
          }
        });
      });
    }
  }
};
</script>