import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import Navigation from '@/components/Navigation'
import Help from '@/components/Help'
import Groups from '@/components/Groups'

Vue.use(Router)
Vue.use(VueResource)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Navigation',
      component: Navigation
    },
    {
      path: '/groups',
      name: 'Groups',
      component: Groups
    },
    {
      path: '/help',
      name: 'Help',
      component: Help
    }
  ]
})
