<template>
  <div id="pageNumberDetail">
    <v-container fluid grid-list-sm>
      <v-layout row wrap>
        <v-flex xs12 sm4>
          <v-card flat hover>
            <v-card-title>
              <span class="title font-weight-light">Details</span>
            </v-card-title>
            <v-list>
              <v-list-tile dense @click>
                <v-list-tile-content>ID</v-list-tile-content>
                <v-list-tile-content class="align-end">{{number.id}}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile dense @click>
                <v-list-tile-content>Name</v-list-tile-content>
                <v-list-tile-content class="align-end">{{number.lable}}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile dense @click>
                <v-list-tile-content>Number</v-list-tile-content>
                <v-list-tile-content class="align-end">{{number.number}}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile dense @click>
                <v-list-tile-content>Message Received</v-list-tile-content>
                <v-list-tile-content class="align-end">{{message("IN").length}}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile dense @click>
                <v-list-tile-content>Message Send</v-list-tile-content>
                <v-list-tile-content class="align-end">{{message("OUT").length}}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile dense>
                <v-list-tile-content class="align-center">
                  <v-btn flat outline color="red" @click="deleteNumber(number.id)">REMOVE THIS NUMBER</v-btn>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-card>
        </v-flex>
        <v-flex xs12 sm8>
          <v-card flat hover>
            <v-card-title>
              <template>
                <v-progress-linear :height="loading" :indeterminate="true"></v-progress-linear>
              </template>
              <span class="title font-weight-light">Actions</span>
            </v-card-title>
            <v-container fluid grid-list-sm>
              <v-layout row wrap>
                <v-flex xs12 sm6>
                  <v-list>
                    <v-list-tile>
                      <v-list-tile-content>Instance</v-list-tile-content>
                      <v-list-tile-action>
                        <v-switch
                          :input-value="number.is_running"
                          @change="switchNumber(number.id, number.is_running)"
                        ></v-switch>
                      </v-list-tile-action>
                      <v-list-tile-content>
                        <v-chip
                          label
                          small
                          :color="getColorByStatus(getLabelInstance(number.is_running))"
                          text-color="white"
                        >{{ getLabelInstance(number.is_running) }}</v-chip>
                      </v-list-tile-content>
                    </v-list-tile>
                    <v-list-tile>
                      <v-list-tile-content>Status</v-list-tile-content>
                      <v-list-tile-action></v-list-tile-action>
                      <v-list-tile-content>
                        <v-chip
                          label
                          small
                          :color="getColorByStatus(getLabelStatus(number.is_running, number.is_logged_in))"
                          text-color="white"
                        >{{ getLabelStatus(number.is_running, number.is_logged_in) }}</v-chip>
                      </v-list-tile-content>
                    </v-list-tile>
                  </v-list>
                </v-flex>
                <v-flex xs12 sm6>
                  <v-card color="blue">
                    <v-img
                      v-if="qrcode"
                      :src="qrcode"
                      aspect-ratio="1"
                      position="center"
                      class="grey lighten-2"
                    ></v-img>
                    <v-img
                      v-else
                      :src="defaultImage"
                      aspect-ratio="1"
                      position="center"
                      class="grey lighten-2"
                    >
                      <template v-if="scan>=10">
                        <v-layout fill-height align-center justify-center ma-0>
                          <v-btn large color="primary" @click="scan = 0">
                            <v-icon>cached</v-icon>REFRESH
                          </v-btn>
                        </v-layout>
                      </template>
                    </v-img>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
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
      colors: {
        Running: "green",
        NotRunning: "red",
        LoggedIn: "green",
        NotLoggedIn: "red",
        WaitForLogin: "blue"
      },
      scan: 0,
      defaultImage:
        "data:image/png;base64,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",
      loading: 0
    };
  },
  computed: {
    ...mapGetters({
      numberId: "numbers/numbersById",
      messageId: "messages/messageByNumber",
      getqrcode: "numbers/getQrCode"
    }),
    number() {
      return this.numberId(parseInt(this.$route.params.numberId));
    },
    qrcode() {
      if (this.number.is_running === true) {
        if (this.scan <= 10 && !this.number.is_logged_in) {
          this.$store.dispatch("numbers/SCAN_QRCODE", this.number.id);
          this.sleep(10000).then(() => {
            this.scan += 1;
          });
        } else {
          this.$store.commit("numbers/REMOVE_QRCODE", {
            numberId: this.number.id
          });
        }
      } else {
        this.scan = 0;
        this.$store.commit("numbers/REMOVE_QRCODE", {
          numberId: this.number.id
        });
      }
      return this.getqrcode(this.number.id);
    },
    randomColor() {
      let item = Math.floor(Math.random() * this.colors.length);
      return this.colors[item];
    }
  },
  methods: {
    message(type) {
      return this.messageId(parseInt(this.$route.params.numberId), type);
    },
    getColorByStatus(status) {
      return this.colors[status];
    },
    getLabelInstance(status) {
      return status === true ? "Running" : "NotRunning";
    },
    getLabelStatus(instance, status) {
      return status ? "LoggedIn" : instance ? "WaitForLogin" : "NotLoggedIn";
    },
    switchNumber(id, currentStatus) {
      this.$store.dispatch("numbers/SWITCH_NUMBER", {
        id: id,
        status: currentStatus
      });
    },
    sleep(milliseconds) {
      return new Promise(resolve => setTimeout(resolve, milliseconds));
    },
    deleteNumber(id) {
      this.$store.dispatch("numbers/DELETE_NUMBERS", id);
      this.$router.push("/numbers")
    }
  }
};
</script>
