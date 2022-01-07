<template>
  <v-app>
    <v-app-bar app color="primary" dark> </v-app-bar>

    <!-- <v-main>
      <HelloWorld />
      <LiveDetail />
      <Myprofile />
    </v-main> -->
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
// import HelloWorld from "./components/HelloWorld";
// import LiveDetail from "./components/LiveDetail";
// import login from './components/login'
// import register from './components/register';
// import home from './components/home'

export default {
  name: "App",

  components: {
    // HelloWorld,
    // LiveDetail,
    // login,
    // register,
    // home
  },

  data: () => ({
    //
  }),
};
</script>
