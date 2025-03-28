<script lang="ts" setup>
/**
 * MenuList.vue
 * 共通メニューコンポーネント
 * 
 * 親コンポーネント
 * @/components/common/TitleHeader.vue
 */
// ==================================
// import
// ==================================
import { computed } from 'vue'

import { useAuthenticator } from '@aws-amplify/ui-vue'

import type { MenuInfo } from '@/types/interfaces'

// ==================================
// interface
// ==================================
interface Props {
  menuList: MenuInfo[];
}

interface Emits {
  (e: 'on-select-menu', value: MenuInfo): void;
}

// ==================================
// data
// ==================================
const props = defineProps<Props>()

const auth = useAuthenticator()

// ==================================
// computed
// ==================================
// メニューリスト表示
const menuList = computed(() => {
  return props.menuList
})

// ==================================
// method
// ==================================
const emit = defineEmits<Emits>()
/**
 * メニュータブから画面遷移
 * @param value - クリックしたメニュー情報
 */
const onClickMenu = (value: MenuInfo) => {
  emit('on-select-menu', value)
}
</script>
<template>
  <v-list class="menu-list">
    <v-list-subheader class="menu-list__text">
      メニュー
    </v-list-subheader>
    <v-list-item
      v-for="(item, index) in menuList"
      :key="index"
      @click="onClickMenu(item)"
    >
      <v-list-item-title class="menu-list__text">
        {{
          item.text
        }}
      </v-list-item-title>
    </v-list-item>
    <v-list-item @click="auth.signOut">
      <v-list-item-title>ログアウト</v-list-item-title>
    </v-list-item>
  </v-list>
</template>
<style lang="scss" scoped>
.menu-list {
  &__text {
    font-size: 15px;
  }
}
</style>
