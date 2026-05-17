import { createRouter, createWebHistory } from 'vue-router'

import RecommendationView from '../components/recommendation/RecommendationView.vue'

const routes = [
  {
    path: '/',
    component: RecommendationView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router