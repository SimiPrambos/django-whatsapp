<template>
  <v-dialog v-model="formDialog" :max-width="maxWidth" scrollable>
    <template v-slot:activator="{ on }">
      <v-btn flat outline :block="block" :color="color" v-on="on">
        <v-icon v-if="icon">{{icon}}</v-icon>
        {{label}}
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">{{title}}</span>
      </v-card-title>

      <v-card-text>
        <v-container fluid grid-list-md>
          <v-layout row wrap>
            <slot name="form"></slot>
          </v-layout>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <slot name="action">
          <v-btn flat outline block color="red" @click="formDialog=false">Close</v-btn>
          <v-btn flat outline block color="blue" :disabled="disabled" @click="onSave">Save</v-btn>
        </slot>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    title: String,
    label: String,
    color: String,
    icon: String,
    block: Boolean,
    onSave: Function,
    disabled: Boolean,
    maxWidth: {
      type: String,
      default: "500px"
    }
  },
  data() {
    return {
      formDialog: false
    };
  },
  methods: {
    close() {
      this.formDialog = false;
    }
  }
};
</script>
