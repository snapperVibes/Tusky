import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: () =>
      import(/* webpackChunkName: "home" */ "../views/HomeView.vue"),  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/room/:roomCodeProp",
    name: "Room",
    props: true,
    component: () =>
      import(/* webpackChunkName: "roomview" */ "../views/RoomView.vue")
  },
  {
    path: "/hello/",
    name: "Hello",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Hello.vue"),
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
