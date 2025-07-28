import { createApp } from "vue";
import { createWebHistory, createRouter } from 'vue-router'

import './style.css';
import App from "./App.vue";

const app = createApp(App);
const router = createRouter({
  routes: [
    { path: '/', component: () => import('./pages/Home.vue') },
    { name: 'story', path: '/story/:id', component: () => import('./pages/Story.vue') },
    { name: 'chat', path: '/chat/:id', component: () => import('./pages/Chat.vue') }
  ],
  history: createWebHistory()
});

app.use(router);
app.mount('#app');