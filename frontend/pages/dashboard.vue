<template>
  <div id="pageDashboard">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  layout: "dashboard",
  middleware: "auth"
};
</script>
