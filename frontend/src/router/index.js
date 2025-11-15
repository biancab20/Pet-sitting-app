import { createRouter, createWebHistory } from 'vue-router'
import PetsView from '@/components/PetsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'pets',
      component: PetsView,
    },
  ],
})

export default router
