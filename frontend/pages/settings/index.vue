<template>
  <h1>settings</h1>
</template>

<script>
import {mapGetters} from 'vuex';
export default {
  layout: "dashboard",
  middleware: "auth",
  data() {
    return {};
  },
  computed: {
    ...mapGetters(
      {user:"loggedInUser"},
      {numbers:"numbers/numbers"}
    )
  }
};
</script>

<style>
</style>
