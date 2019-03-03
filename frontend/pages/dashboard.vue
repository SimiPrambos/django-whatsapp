<template>
  <div id="pageDashboard">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <h1>Hwllo dashboard</h1>
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
