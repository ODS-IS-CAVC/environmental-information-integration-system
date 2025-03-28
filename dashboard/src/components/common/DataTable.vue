<script lang="ts" setup>
/**
 * DataTable.vue
 * テーブルコンポーネント
 * 
 * 親コンポーネント
 * @/src/views/AliveMonitoring.vue
 * @/src/views/CommunicationMedia.vue
 * @/src/views/RoadsideUnit.vue
 * @/src/views/ServiceLocation.vue
 * @/src/views/Signal.vue
 * @/src/views/UseCase.vue
 */
// ==================================
// import
// ==================================
import type { TableHeader } from '@/types/interfaces'

// ==================================
// interface
// ==================================
interface Props {
  headers?: TableHeader[];
  items?: any[];
}

// ==================================
// data
// ==================================
const props = defineProps<Props>()

</script>
<template>
  <v-card elevation="5">
    <slot>
      <v-data-table
        hover
        :headers="props.headers"
        :items="props.items"
        :item-per-page="10"
      >
      </v-data-table>
    </slot>
  </v-card>
</template>
<style lang="scss" scoped>
@use '@/assets/styles/data-table.scss';
</style>
