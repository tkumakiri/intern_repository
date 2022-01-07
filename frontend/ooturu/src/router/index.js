import Vue from "vue";
import Router from "vue-router";

import LiveDetail from "../components/LiveDetail.vue";
import Myprofile from "../components/Myprofile.vue";
import Userprofile from "../components/Userprofile.vue";
import Login from "../components/login.vue";
import Tweet from "../components/Tweet.vue";

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
    {
      path: "/userprofile",
      name: "userprofile",
      component: Userprofile,
    },
    {
      path: "/tweet",
      name: "tweet",
      component: Tweet,
    },
  ],
});
