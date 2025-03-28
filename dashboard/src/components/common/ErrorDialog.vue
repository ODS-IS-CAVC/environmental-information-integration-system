<script lang="ts" setup>
/**
 * ErrorDialog.vue
 * 共通エラーダイアログ
 * 
 * 親コンポーネント
 * @/components/aliveMonitoring/Alive
 * @/components/aliveMonitoring/AliveMonitoringTable.vue
 * @/components/communicationMedia/CommunicationMediaTable.vue
 * @/components/roadsideUnit/RoadsideUnitTable.vue
 * @/components/serviceLocation/ServiceLocationTable.vue
 * @/components/signal/SignalTable.vue
 * @/components/useCase/UseCaseTable.vue
 */
// ==================================
// import
// ==================================
import { computed } from 'vue'

import type { ErrorDialogInfo } from '@/types/interfaces'

// ==================================
// interface
// ==================================
interface Props {
  errorDialog: ErrorDialogInfo;
}

interface Emits {
  (e: 'on-click-close-error-dialog'): void;
}

// ==================================
// data
// ==================================
const props = defineProps<Props>()

// ==================================
// computed
// ==================================
const isShowDialog = computed(() => {
  return props.errorDialog.isShow
})

const showTitle = computed(() => {
  return props.errorDialog.title
})

const showMessage = computed(() => {
  return props.errorDialog.message
})

// ==================================
// method
// ==================================
const emit = defineEmits<Emits>()
/**
 * エラーダイアログを閉じる
 */
const closeDialog = () => {
  emit('on-click-close-error-dialog')
}
</script>
<template>
  <v-dialog
    v-model="isShowDialog"
    class="error-dialog"
    nav
    dense
    width="20vw"
    persistent
  >
    <v-card>
      <v-container>
        <v-card-title class="error-dialog__title">
          <span v-text="showTitle" />
        </v-card-title>
        <v-divider />
        <v-card-text class="error-dialog__message">
          <span v-text="showMessage" />
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-spacer />
          <v-btn
            variant="flat"
            color="blue-grey"
            dark
            rounded
            @click="closeDialog"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-container>
    </v-card>
  </v-dialog>
</template>
<style lang="scss" scoped>
  .error-dialog {
    &__title {
      height: 5vh;
      font-size: 20px;
      font-weight: bold;
    }
    &__message {
      height: 15vh;
      font-size: 15px;
      & > span {
        white-space: pre-line;
      }
    }
  }
</style>
