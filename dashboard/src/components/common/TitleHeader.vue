<script lang="ts" setup>
/**
 * TitleHeader.vue
 * 共通タイトルヘッダー
 * 
 * 親コンポーネント
 * @/views/AliveMonitoringInfo.vue
 */
// ==================================
// import
// ==================================
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { MENU } from '@/setting/setting'

import MenuList from '@/components/common/MenuList.vue'
import type { MenuInfo } from '@/types/interfaces'

// ==================================
// data
// ==================================
const routeName = ref<string>('')
const route = useRoute()
if (route.name !== undefined) {
  routeName.value = route.name.toString()
}

const router = useRouter()

const showMenu = ref<boolean>(false)

// ==================================
// computed
// ==================================
// タイトル表示
const showTitle = computed(() => {
  const menuExceptForCurrent = MENU.filter((val) => {
    return val.name === routeName.value
  })
  return menuExceptForCurrent[0].text
})

// メニューリスト表示
const menuList = computed(() => {
  const menuExceptForCurrent = MENU.filter((val) => {
    return val.name !== routeName.value
  })
  return menuExceptForCurrent
})

// ==================================
// method
// ==================================
/**
 * メニューリストアイコン押下
 */
const onClickMenu = () => {
  showMenu.value = !showMenu.value
}

/**
 * メニュータブから画面遷移
 * @param menu - 選択したメニュー情報
 */
const selectMenu = (menu: MenuInfo) => {
  showMenu.value = false
  router.push({ name: menu.name })
}
</script>
<template>
  <v-app-bar
    color="primary"
    class="title-header"
  >
    <v-app-bar-title>
      <span class="title-header__title">
        <span v-text="showTitle" />
      </span>
    </v-app-bar-title>
    <v-app-bar-nav-icon
      @click="onClickMenu"
    >
      <v-icon color="white">
        mdi-menu
      </v-icon>
    </v-app-bar-nav-icon>
  </v-app-bar>
  <v-navigation-drawer
    v-model="showMenu"
    theme="dark"
    location="right"
    width="350"
  >
    <MenuList
      :menu-list="menuList"
      @on-select-menu="selectMenu"
    />
  </v-navigation-drawer>
</template>
<style lang="scss" scoped>
  .title-header {
    &__title {
      font-size: 1.5rem;
    }
  }
</style>
