<template>
  <div id="limitedaccessPage">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
        <v-flex>
          <error-page :error="limitedAccess"></error-page>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import ErrorPage from "@/layouts/error";
export default {
  layout: "dashboard",
  components: {
    ErrorPage
  },
  data() {
    return {
      limitedAccess: {
        statusCode: 403,
        message: "Sorry, Your Api Access was expired."
      }
    };
  }
};
</script>

<style>
</style>
