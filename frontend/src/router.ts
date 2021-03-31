import Vue from "vue";
import Router from "vue-router";

import RouterComponent from "./components/RouterComponent.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      component: () => import(/* webpackChunkName: "start" */ "./views/main/Start.vue"),
    },
    {
        path: "/*", redirect: "/",
    },
  ],
});
