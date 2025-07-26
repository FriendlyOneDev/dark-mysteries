import { createApp } from "vue";
import { createWebHistory, createRouter } from 'vue-router'

import './style.css';
import App from "./App.vue";

const app = createApp(App);
const router = createRouter({
  routes: [
    { path: '/', component: () => import('./pages/Home.vue') }
  ],
  history: createWebHistory()
});

app.use(router);
app.mount('#app');