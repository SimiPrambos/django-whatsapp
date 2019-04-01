<template>
  <div id="numberSetting">
    <v-container fluid grid-list-sm>
      <v-layout row wrap>
        <!-- detail -->
        <v-flex d-flex sm5>
          <v-card>
            <v-card-title>
              <v-icon left>details</v-icon>
              <span class="title font-weight-light">Details</span>
            </v-card-title>
            <v-card-text>
              <v-data-table :items="items" hide-headers hide-actions>
                <template v-slot:items="props">
                  <tr>
                    <td class="text-xs-left subheading">ID</td>
                    <td class="text-xs-left subheading">{{number.id}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Name</td>
                    <td class="text-xs-left subheading">{{number.lable}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Number</td>
                    <td class="text-xs-left subheading">{{number.number}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Created</td>
                    <td class="text-xs-left subheading">{{formateDate(number.created_at)}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Total Inbox</td>
                    <td class="text-xs-left subheading">{{message('IN')}}</td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Total Outbox</td>
                    <td class="text-xs-left subheading">{{message('OUT')}}</td>
                  </tr>
                </template>
              </v-data-table>
            </v-card-text>
            <v-card-actions>
              <v-btn flat block outline color="red" @click="onDelete">REMOVE THIS NUMBER</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>

        <!-- action -->
        <v-flex d-flex sm7>
          <v-card>
            <v-card-title>
              <v-icon left>mdi-information-outline</v-icon>
              <span class="title font-weight-light">Status</span>
              <v-spacer></v-spacer>
              <v-chip small outline :color="number.is_running?'green':'red'" label>
                <v-avatar>
                  <v-icon>mdi-whatsapp</v-icon>
                </v-avatar>
                {{number.is_running?'Online':'Offline'}}
              </v-chip>
              <v-chip small outline :color="number.is_logged_in?'green':'red'" label>
                <v-avatar>
                  <v-icon>mdi-lock-outline</v-icon>
                </v-avatar>
                {{number.is_logged_in?'LoggedIn':'NotLoggedIn'}}
              </v-chip>
            </v-card-title>
            <v-layout justify-space-around fill-height row wrap>
              <v-flex sm7 xs12 offset-xs2>
                <v-img
                  :src="qrcode"
                  aspect-ratio="1"
                  max-height="250"
                  max-width="250"
                  position="center"
                  class="grey lighten-2"
                >
                  <template v-slot:placeholder v-if="number.is_running && !number.is_logged_in">
                    <v-layout fill-height align-center justify-center ma-0>
                      <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                    </v-layout>
                  </template>
                </v-img>
              </v-flex>
              <v-flex sm12 xs12>
                <v-card-actions>
                  <v-btn
                    flat
                    outline
                    block
                    :color="number.is_running?'red':'blue'"
                    @click="switchNumber(number.id, number.is_running)"
                  >{{number.is_running?'Stop':'Start'}} Whatsapp</v-btn>
                  <v-btn
                    flat
                    outline
                    block
                    color="blue"
                    :disabled="!number.is_running||number.is_logged_in"
                    @click="scan"
                  >{{qrcode?'Reload':'Scan'}} QrCode</v-btn>
                </v-card-actions>
              </v-flex>
            </v-layout>
          </v-card>
        </v-flex>

        <!-- settings -->
        <v-flex lg12 sm12 xs12>
          <v-card>
            <v-card-title>
              <v-icon left>settings</v-icon>
              <span class="title font-weight-light">Setting</span>
              <v-spacer></v-spacer>
              <!-- <v-btn flat v-if="!update" @click="onUpdate" outline color="blue">
                <v-icon left>edit</v-icon>edit
              </v-btn>
              <v-btn flat v-if="update" @click="onSave" outline color="green">
                <v-icon left>save</v-icon>save
              </v-btn>-->
              <v-btn small flat icon color="blue" v-if="!update" @click="onUpdate">
                <v-icon>edit</v-icon>
              </v-btn>
              <v-btn small flat icon color="green" v-if="update" @click="onSave">
                <v-icon>save</v-icon>
              </v-btn>
              <v-btn small flat icon color="red" v-if="update" @click="update=false">
                <v-icon>mdi-cancel</v-icon>
              </v-btn>
              <!-- <v-btn-toggle mandatory multiple> -->

              <!-- </v-btn-toggle> -->
            </v-card-title>
            <v-card-text v-if="setting">
              <v-data-table :items="items" hide-headers hide-actions>
                <template v-slot:items="props">
                  <tr>
                    <td class="text-xs-left subheading">Auto Record Inbox</td>
                    <td class="text-xs-left">
                      <v-layout row wrap justify-end>
                        <v-flex sm4>
                          <v-select
                            :items="options"
                            v-model="setting.record_inbox"
                            flat
                            dense
                            :readonly="!update"
                          ></v-select>
                        </v-flex>
                      </v-layout>
                    </td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Auto Read Inbox</td>
                    <td class="text-xs-left">
                      <v-layout row wrap justify-end>
                        <v-flex sm4>
                          <v-select
                            :items="options"
                            v-model="setting.auto_read"
                            flat
                            dense
                            :readonly="!update"
                          ></v-select>
                        </v-flex>
                      </v-layout>
                    </td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Auto Reboot</td>
                    <td class="text-xs-left">
                      <v-layout row wrap justify-end>
                        <v-flex sm4>
                          <v-dialog
                            ref="auto_reboot"
                            v-model="dialog.reboot"
                            :return-value.sync="time.reboot"
                            persistent
                            :disabled="!update"
                            lazy
                            full-width
                            width="290px"
                          >
                            <template v-slot:activator="{ on }">
                              <v-text-field
                                :label="setting.auto_reboot"
                                prepend-inner-icon="access_time"
                                :readonly="!update"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-time-picker
                              v-model="setting.auto_reboot"
                              full-width
                              format="24hr"
                              use-seconds
                            >
                              <v-spacer></v-spacer>
                              <v-btn flat color="primary" @click="dialog.reboot = false">Cancel</v-btn>
                              <v-btn
                                flat
                                color="primary"
                                @click="$refs.auto_reboot.save(time.reboot)"
                              >OK</v-btn>
                            </v-time-picker>
                          </v-dialog>
                        </v-flex>
                      </v-layout>
                    </td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Max Delay Send Per Message (second)</td>
                    <td class="text-xs-left">
                      <v-layout row wrap justify-end>
                        <v-flex sm4>
                          <v-text-field
                            :readonly="!update"
                            type="number"
                            v-model="setting.max_delay"
                          ></v-text-field>
                        </v-flex>
                      </v-layout>
                    </td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Delay after send few messages (digit)</td>
                    <td class="text-xs-left">
                      <v-layout row wrap justify-end>
                        <v-flex sm4>
                          <v-text-field
                            :readonly="!update"
                            type="number"
                            v-model="setting.delay_after"
                          ></v-text-field>
                        </v-flex>
                      </v-layout>
                    </td>
                  </tr>
                  <tr>
                    <td class="text-xs-left subheading">Send Message Schedule</td>
                    <td class="text-xs-left">
                      <v-layout row wrap justify-end>
                        <v-flex sm4>
                          <v-dialog
                            ref="send_schedule_from"
                            v-model="dialog.from"
                            :return-value.sync="time.from"
                            persistent
                            :disabled="!update"
                            lazy
                            full-width
                            width="290px"
                          >
                            <template v-slot:activator="{ on }">
                              <v-text-field
                                :label="setting.send_schedule_from"
                                prepend-inner-icon="mdi-clock-start"
                                :readonly="!update"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-time-picker
                              v-model="setting.send_schedule_from"
                              full-width
                              format="24hr"
                              use-seconds
                            >
                              <v-spacer></v-spacer>
                              <v-btn flat color="primary" @click="dialog.from = false">Cancel</v-btn>
                              <v-btn
                                flat
                                color="primary"
                                @click="$refs.send_schedule_from.save(time.from)"
                              >OK</v-btn>
                            </v-time-picker>
                          </v-dialog>
                        </v-flex>
                        <v-flex sm4>
                          <v-dialog
                            ref="send_schedule_to"
                            v-model="dialog.to"
                            :return-value.sync="time.to"
                            persistent
                            :disabled="!update"
                            lazy
                            full-width
                            width="290px"
                          >
                            <template v-slot:activator="{ on }">
                              <v-text-field
                                :label="setting.send_schedule_to"
                                prepend-inner-icon="mdi-clock-end"
                                :readonly="!update"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-time-picker
                              v-model="setting.send_schedule_to"
                              full-width
                              format="24hr"
                              use-seconds
                            >
                              <v-spacer></v-spacer>
                              <v-btn flat color="primary" @click="dialog.to = false">Cancel</v-btn>
                              <v-btn
                                flat
                                color="primary"
                                @click="$refs.send_schedule_to.save(time.to)"
                              >OK</v-btn>
                            </v-time-picker>
                          </v-dialog>
                        </v-flex>
                      </v-layout>
                    </td>
                  </tr>
                </template>
              </v-data-table>
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
  middleware: ["auth","HasApiAccess"],
  data() {
    return {
      update: false,
      time: {
        reboot: null,
        from: null,
        to: null
      },
      dialog: {
        reboot: false
      },
      expand: [true],
      qrcode: "",
      items: [
        {
          record_inbox: true,
          auto_read: true,
          auto_reboot: "01:00:20",
          max_delay: 10,
          send_schedule_from: "00:00:00",
          send_schedule_to: "23:00:00"
        }
      ],
      options: [
        { text: "Active", value: true },
        { text: "Non Active", value: false }
      ],
      newsetting: {}
    };
  },
  mounted() {
    this.$store.dispatch("numbers/GET_NUMBER_SETTING", this.getId);
  },
  computed: {
    getId() {
      return parseInt(this.$route.params.Id);
    },
    ...mapGetters({
      getNumber: "numbers/numbersById",
      getSetting: "numbers/setting",
      getMessage: "messages/messageByNumber"
    }),
    number() {
      return this.getNumber(this.getId);
    },
    setting() {
      return this.update ? this.newsetting : this.getSetting(this.getId);
    }
  },
  methods: {
    message(type) {
      return this.getMessage(this.getId, type).length;
    },
    formateDate(string) {
      return string ? new Date(string).toLocaleDateString() : "";
    },
    switchNumber(id, currentStatus) {
      this.$store.dispatch("numbers/SWITCH_NUMBER", {
        id: id,
        status: currentStatus
      });
      this.$store.dispatch("numbers/GET_NUMBERS");
    },
    scan() {
      let id = this.getId;
      this.$axios.setHeader("Api-Key", this.$store.state.auth.user.api_key);
      this.$axios
        .get(`numbers/${id}/login/`, { progress: true })
        .then(response => {
          if (response.status === 200) {
            let qrcode = "";
            if (response.data.status === "isLoggedIn") {
              this.qrcode = "";
              this.$store.commit("numbers/UPDATE_STATUS_LOGIN", {
                numberId: this.getId,
                status: true
              });
            } else {
              this.qrcode = `data:image/png;base64,${response.data.qrcode}`;
            }
          }
        });
    },
    onUpdate() {
      this.newsetting = Object.assign({}, this.getSetting(this.getId));
      this.update = true;
    },
    onSave() {
      if (this.update) {
        this.$store.dispatch("numbers/UPDATE_NUMBER_SETTING", this.setting);
        this.update = false;
      }
    },
    onDelete() {
      this.$store.dispatch("numbers/DELETE_NUMBERS", this.getId);
      this.$router.push("/numbers");
    }
  }
};
</script>

<style>
</style>
