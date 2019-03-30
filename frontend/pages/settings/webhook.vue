<template>
  <div id="pageWebhook">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex lg8 sm8 xs12>
          <v-card>
            <v-toolbar card dense color="transparent">
              <v-card-title>
                <span class="headline">Webhook</span>
              </v-card-title>
              <v-spacer></v-spacer>
              <form-dialog
                title="Edit Webhook"
                label="edit"
                color="blue"
                :onSave="onSave"
                ref="updatewebhook"
              >
                <template v-slot:form v-if="newSetting">
                  <v-flex>
                    <v-select
                    v-model="newSetting.webhook_enable"
                      label="Status"
                      :items="[{text:'Enable',value:true},{text:'Disable',value:false}]"
                    ></v-select>
                  </v-flex>
                  <v-flex>
                    <v-text-field label="URL" outline v-model="newSetting.webhook_url"></v-text-field>
                  </v-flex>
                </template>
              </form-dialog>
            </v-toolbar>
            <v-card-text>
              <v-list subheader>
                <v-list-tile>
                  <v-list-tile-content>Status</v-list-tile-content>
                  <v-list-tile-content
                    :class="'align-end ' + (setting.webhook_enable?'green':'red') + '--text'"
                  >{{ setting.webhook_enable?'Enabled':'Disabled' }}</v-list-tile-content>
                </v-list-tile>
                <v-list-tile>
                  <v-list-tile-content>URL</v-list-tile-content>
                  <v-list-tile-content class="align-end">{{setting.webhook_url}}</v-list-tile-content>
                </v-list-tile>
              </v-list>
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
  mounted() {
    this.$store.dispatch("settings/GET_SETTING");
    this.newSetting = this.setting;
  },
  data() {
    return {
      newSetting: null
    };
  },
  computed: {
    ...mapGetters(
      { setting: "settings/setting" },
    )
  },
  methods: {
    onSave() {
      let payload = {
        webhook_enable: this.newSetting.webhook_enable,
        webhook_url: this.newSetting.webhook_url
      };
      this.$store.dispatch("settings/UPDATE_SETTING", payload);
      this.$refs.updatewebhook.close();
    }
  }
};
</script>

<style>
</style>
