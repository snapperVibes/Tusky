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
    path: "/editor",
    name: "Editor",
    component: () =>
      import(/* webpackChunkName: "editor" */ "../views/Editor.vue"),
  },
  {
    path: "/editor2",
    name: "Editor2",
    component: () =>
      import(/* webpackChunkName: "editor2" */ "../views/Editor2.vue"),
  },
  {
    path: "/room/:roomcode",
    name: "Room",
    props: true,
    component: () =>
      import(/* webpackChunkName: "roomview" */ "../views/RoomView.vue")

  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
