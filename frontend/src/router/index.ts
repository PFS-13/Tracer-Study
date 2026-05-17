import { createRouter, createWebHistory } from 'vue-router'

// import RecommendationView from '../components/recommendation/RecommendationView.vue'
import App from '../App.vue'
const routes = [
  {
    path: '/',
    component: App
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router