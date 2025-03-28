<script setup lang="ts">
/**
 * Signal.vue
 * 信号情報コンポーネント
 */
// ==================================
// import
// ==================================
import { onBeforeMount, ref } from 'vue'

import { apiResponseErrorCode, updateSignalList } from '@/mixins/communicationFunction'
import { sortByDate } from '@/mixins/dataTableFunction'

import { DIALOG_ERROR_INFO } from '@/setting/setting'

import DataTable from '@/components/common/DataTable.vue'
import ErrorDialog from '@/components/common/ErrorDialog.vue'
import Loading from '@/components/common/Loading.vue'
import TitleHeader from '@/components/common/TitleHeader.vue'
import { useSignalStore } from '@/stores/app'
import type { ErrorDialogInfo, SignalForDisplay, TableHeader } from '@/types/interfaces'

// ==================================
// data
// ==================================
const signalStore = useSignalStore()

const headers = ref<TableHeader[]>([])

const items = ref<SignalForDisplay[]>([])

const isLoading = ref<boolean>(false)

const errorDialog = ref<ErrorDialogInfo>({
  message: '',
  title: '',
  isShow: false,
})

// ==================================
// hook
// ==================================
onBeforeMount(() => {
  initialize()
})

// ==================================
// method
// ==================================
/**
 * 初期化処理
 */
const initialize = () => {
  headers.value = [
    { title: 'サービス地点ID', key: 'serviceLocationID' },
    { title: '路側機ID', key: 'roadsideUnitID' },
    { title: '都道府県', key: 'prefecture' },
    { title: '提供点種別', key: 'roadType' },
    { title: '交差点ID/単路ID', key: 'intersectionID' },
    { title: 'Last Update', key: 'updateTimeInfo', sort: sortByDate },
  ]
  setSignalList()
}

/**
 * 信号情報設定
 */
const setSignalList = async () => {
  isLoading.value = true
  updateSignalList()
    .then(() => {
      items.value = signalStore.dataForDisplay
      isLoading.value = false
    })
    .catch(statusCode => {
      errorDialog.value.title = DIALOG_ERROR_INFO.title.getError
      errorDialog.value.message = DIALOG_ERROR_INFO.message.getError
      if (statusCode === apiResponseErrorCode.noContent) {
        errorDialog.value.message = DIALOG_ERROR_INFO.message.getErrorNoContent
      }
      errorDialog.value.isShow = true
      isLoading.value = false
    })
}

/**
 * エラーダイアログクローズ処理
 */
const onClickCloseErrorDialog = () => {
  errorDialog.value.isShow = false
}
</script>
<template>
  <TitleHeader />
  <v-container fill-height>
    <DataTable
      :headers="headers"
      :items="items"
    />
  </v-container>
  <Loading v-show="isLoading" />
  <ErrorDialog
    :error-dialog="errorDialog"
    @on-click-close-error-dialog="onClickCloseErrorDialog"
  />
</template>
<style lang="scss" scoped>
@use '@/assets/styles/data-table-sticky-columns.scss'
</style>
