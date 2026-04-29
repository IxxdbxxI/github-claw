import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/image',
      name: 'image',
      component: () => import('../views/ImageView.vue'),
    },
    {
      path: '/audio',
      name: 'audio',
      component: () => import('../views/AudioView.vue'),
    },
    {
      path: '/video',
      name: 'video',
      component: () => import('../views/VideoView.vue'),
    },
  ],
})

export default router
