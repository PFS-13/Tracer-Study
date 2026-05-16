import { createRouter, createWebHistory } from 'vue-router'

import RecommendationView from '../components/recommendation/RecommendationView.vue'

const routes = [
  {
    path: '/login',
    component: RecommendationView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router