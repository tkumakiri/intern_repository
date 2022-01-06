import Vue from "vue";
import Router from "vue-router";

import LiveDetail from "../components/LiveDetail.vue";
import Myprofile from "../components/Myprofile.vue";
import Login from "../components/login.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "login",
      component: Login,
    },
    {
      path: "/livedetail",
      name: "livedetail",
      component: LiveDetail,
    },
    {
      path: "/myprofile",
      name: "myprofile",
      component: Myprofile,
    },
  ],
});
