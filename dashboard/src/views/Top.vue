<script setup lang="ts">
/**
 * Top.vue
 * TOP画面コンポーネント
 */
// ==================================
// import
// ==================================
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import { MENU } from '@/setting/setting'

import TitleHeader from '@/components/common/TitleHeader.vue'
import type { MenuInfo } from '@/types/interfaces'

// ==================================
// data
// ==================================
const router = useRouter()

// ==================================
// computed
// ==================================
const menuListWithPath = computed(() => {
  const menuExceptForCurrent: MenuInfo[] = MENU.filter((val) => {
    return val.name !== 'top'
  })
  for (const menu of menuExceptForCurrent) {
    menu.path = router.resolve({ name: menu.name }).href
  }
  return menuExceptForCurrent
})
</script>
<template>
  <TitleHeader />
  <v-container fill-height>
    <v-list>
      <v-list-item
        v-for="menu in menuListWithPath"
        :key="menu.name"
        :title="menu.text"
        :to="menu.path"
      >
      </v-list-item>
    </v-list>
  </v-container>
</template>
