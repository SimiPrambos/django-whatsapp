<template>
  <div id="media" class="media">
    <v-toolbar class="elevation-0 transparent media-toolbar">
      <v-btn flat outline color="red" v-if="selected.length > 0" @click="deleteFile">
        <v-icon>delete</v-icon>
        &nbsp;Delete Selected ({{selected.length}})
      </v-btn>
      <v-dialog v-model="dialog" max-width="500px">
        <template v-slot:activator="{ on }">
          <v-btn flat outline color="primary" v-on="on">
            <v-icon>cloud_upload</v-icon>&nbsp;Upload
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">Upload File</span>
          </v-card-title>

          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs4 sm4 md4>
                  <upload-button
                    title
                    large
                    outline
                    :ripple="false"
                    :fileChangedCallback="fileChanged"
                  >
                    <template slot="icon">
                      <v-icon>attach_file</v-icon>
                    </template>
                  </upload-button>
                </v-flex>
                <v-flex xs8 sm8 md8>
                  <v-text-field
                    label="Save as Name"
                    v-model="filename"
                    :hint="originalName"
                    persistent-hint
                    required
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
            <v-btn color="blue darken-1" flat @click="save">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-spacer></v-spacer>
      <v-btn-toggle v-model="view">
        <v-btn flat value="list">
          <v-icon color="primary">view_headline</v-icon>
        </v-btn>
        <v-btn flat value="grid">
          <v-icon color="primary">view_list</v-icon>
        </v-btn>
      </v-btn-toggle>
    </v-toolbar>
    <v-divider></v-divider>
    <div class="layout row media-layout">
      <div class="media-content flex transparent">
        <vue-perfect-scrollbar class="media-content--warp">
          <v-container fluid v-if="view ==='grid'">
            <v-layout row wrap class="x-grid-lg">
              <v-flex lg3 sm12 xs12 class="pa-2" v-for="(item, index) in media" :key="index">
                <a class="d-flex">
                  <v-card flat tile>
                    <!-- if is image -->
                    <img
                      style="height: 150px; width: 100%"
                      :src="item.filepath"
                      alt
                      v-if="isImage(item.filepath)"
                    >
                    <v-icon class="mx-auto" size="150" v-else-if="isAudio(item.filepath)">music_note</v-icon>
                    <v-icon
                      class="mx-auto"
                      size="150"
                      v-else-if="isVideo(item.filepath)"
                    >video_library</v-icon>
                    <v-icon class="mx-auto" size="135" v-else>insert_drive_file</v-icon>
                    <v-divider></v-divider>
                    <v-card-title>{{item.filename}}</v-card-title>
                  </v-card>
                </a>
              </v-flex>
            </v-layout>
          </v-container>
          <v-layout column v-else>
            <v-list dense class="transparent">
              <v-list-tile avatar v-for="(item, index) in media" :key="index">
                <v-list-tile-action>
                  <v-checkbox v-model="selected" :value="item.id"></v-checkbox>
                </v-list-tile-action>
                <v-list-tile-avatar>
                  <v-icon v-if="isImage(item.filepath)">image</v-icon>
                  <v-icon v-else-if="isAudio(item.filepath)">music_note</v-icon>
                  <v-icon v-else-if="isVideo(item.filepath)">video_library</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <div class="container pl-0">
                    <div class="layout row">
                      <div class="flex">{{item.filename}}</div>
                      <v-spacer></v-spacer>
                      <div class="caption">{{item ? formateDate(item.created) : ''}}</div>
                    </div>
                  </div>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-layout>
        </vue-perfect-scrollbar>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import VuePerfectScrollbar from "vue-perfect-scrollbar";
import UploadButton from "vuetify-upload-button";
export default {
  layout: "dashboard",
  components: {
    VuePerfectScrollbar,
    UploadButton
  },
  data: () => ({
    view: "list",
    imageMime: ["jpg", "jpeg", "png"],
    audioMime: ["mp3"],
    videoMime: ["mp4", "3gp"],
    dialog: false,
    selected: [],
    filename: "",
    filepath: ""
  }),
  mounted() {
    this.$store.dispatch("media/GET_MEDIA");
  },
  computed: {
    ...mapGetters({ media: "media/media" }),
    originalName() {
      return this.filepath ? `Original name : ${this.filepath.name}` : "";
    }
  },
  methods: {
    fileType(file) {
      return file.split(".").pop();
    },
    isImage(file) {
      return this.imageMime.includes(this.fileType(file));
    },
    isAudio(file) {
      return this.audioMime.includes(this.fileType(file));
    },
    isVideo(file) {
      return this.videoMime.includes(this.fileType(file));
    },
    formateDate(string) {
      return string ? new Date(string).toLocaleDateString() : "";
    },
    fileChanged(file) {
      this.filepath = file;
    },
    close() {
      this.dialog = false;
      this.filename = "";
      this.filepath = "";
    },
    save() {
      let payload = {
        filename: this.filename ? this.filename : this.filepath.name,
        filepath: this.filepath
      };
      this.$store.dispatch("media/POST_MEDIA", payload);
      this.close();
    },
    deleteFile() {
      this.$store.dispatch("media/DELETE_MEDIA", this.selected);
      this.selected = [];
    }
  }
};
</script>
<style lang="stylus" scoped>
.media {
  &-cotent--wrap, &-menu {
    min-width: 260px;
    border-right: 1px solid #eee;
    min-height: calc(100vh - 50px - 64px);
  }

  &-detail {
    min-width: 300px;
    border-left: 1px solid #eee;
  }
}
</style>
