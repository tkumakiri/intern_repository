<template>
  <v-app>
    <v-app-bar app color="primary" dark> </v-app-bar>

    <v-main>
      <!-- <HelloWorld /> -->
      <!-- <Search /> -->
      <!-- <DmList /> -->
      <!-- <LiveDetail /> -->
      <!-- <Myprofile /> -->
      <!-- <Home />
      <Login />
      <Register />
      <LiveRegister /> -->
      <v-content>
        <router-view />
      </v-content>
    </v-main>
  </v-app>
</template>

<script>
// import HelloWorld from "./components/HelloWorld";
//import LiveDetail from "./components/LiveDetail";
// import login from "./components/Login";
// import register from "./components/Register";
// import home from "./components/Home";
// import liveRegister from "./components/LiveRegister"
// import dmList from "./components/DmList";
// import search from "./components/Search";

export default {
  name: "App",

  components: {
    // HelloWorld,
    // LiveDetail,
    // Login,
    // Register,
    // Home,
    // LiveRegister,
    // DmList,
    // Search
},  

  data: () => ({
    //
  }),
};
</script>
