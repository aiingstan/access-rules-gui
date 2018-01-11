import Vue from 'vue'
import Router from 'vue-router'
import Navigation from '@/components/Navigation'
import Help from '@/components/Help'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Navigation',
      component: Navigation
    },
    {
      path: '/help',
      name: 'Help',
      component: Help
    }
  ]
})
