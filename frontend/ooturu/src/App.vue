<template>
  <v-app>
    <v-app-bar app color="primary" dark> </v-app-bar>

    <v-main>
      <!-- <HelloWorld /> -->
      <!-- <LiveDetail /> -->
      <!-- <Myprofile /> -->
      <v-content>
        <router-view />
      </v-content>
    </v-main>
  </v-app>
</template>

<script>
// import HelloWorld from "./components/HelloWorld";
// import LiveDetail from "./components/LiveDetail";
// import Myprofile from "./components/Myprofile";

export default {
  name: "App",

  components: {
    // HelloWorld,
    // LiveDetail,
    // Myprofile,
  },

  data: () => ({
    //
  }),
};
</script>
