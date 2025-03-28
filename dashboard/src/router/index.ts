import { createRouter, createWebHistory } from 'vue-router'

import AliveMonitoring from '@/views/AliveMonitoring.vue'
import CommunicationMedia from '@/views/CommunicationMedia.vue'
import RoadsideUnit from '@/views/RoadsideUnit.vue'
import ServiceLocation from '@/views/ServiceLocation.vue'
import Signal from '@/views/Signal.vue'
import Top from '@/views/Top.vue'
import UseCase from '@/views/UseCase.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'top',
      component: Top,
    },
    {
      path: '/alive-monitoring',
      name: 'aliveMonitoring',
      component: AliveMonitoring,
    },
    {
      path: '/service-location',
      name: 'serviceLocation',
      component: ServiceLocation,
    },
    {
      path: '/roadside-unit',
      name: 'roadsideUnit',
      component: RoadsideUnit,
    },
    {
      path: '/use-case',
      name: 'useCase',
      component: UseCase,
    },
    {
      path: '/signal',
      name: 'signal',
      component: Signal,
    },
    {
      path: '/communication-media',
      name: 'communicationMedia',
      component: CommunicationMedia,
    },
  ],
})

export default router
