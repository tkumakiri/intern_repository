<template>
  <v-app>
    <v-app-bar app color="primary" dark> </v-app-bar>

    <v-main>
      <!-- <HelloWorld /> -->
      <search />
      <dmList />
      <LiveDetail />
      <!-- <Myprofile /> -->
      <home />
      <login />
      <register />
      <liveRegister />
      <v-content>
        <router-view />
      </v-content>
    </v-main>
  </v-app>
</template>

<script>
// import HelloWorld from "./components/HelloWorld";
import LiveDetail from "./components/LiveDetail";
import login from "./components/login";
import register from "./components/register";
import home from "./components/home";
import liveRegister from "./components/liveRegister"
import dmList from "./components/dmList";
import search from "./components/search";

export default {
  name: "App",

  components: {
    // HelloWorld,
    LiveDetail,
    login,
    register,
    home,
    liveRegister,
    dmList,
    search
},  

  data: () => ({
    //
  }),
};
</script>
