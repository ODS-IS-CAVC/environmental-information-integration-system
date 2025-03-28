<script setup lang="ts">
/**
 * UseCase.vue
 * ユースケース情報コンポーネント
 */
// ==================================
// import
// ==================================
import { onBeforeMount, ref } from 'vue'

import { apiResponseErrorCode, updateUseCaseList } from '@/mixins/communicationFunction'
import { sortByDate } from '@/mixins/dataTableFunction'

import { DIALOG_ERROR_INFO } from '@/setting/setting'

import DataTable from '@/components/common/DataTable.vue'
import ErrorDialog from '@/components/common/ErrorDialog.vue'
import Loading from '@/components/common/Loading.vue'
import TitleHeader from '@/components/common/TitleHeader.vue'
import { useUseCaseStore } from '@/stores/app'
import type { ErrorDialogInfo, TableHeader, UseCaseForDisplay } from '@/types/interfaces'

// ==================================
// data
// ==================================
const useCaseStore = useUseCaseStore()

const headers = ref<TableHeader[]>([])

const items = ref<UseCaseForDisplay[]>([])

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
    { title: '対象ユースケース類型', key: 'useCaseType' },
    { title: '対象ユースケースケース補足', key: 'useCaseSupplementary' },
    { title: '対象活用類型', key: 'targetUtilizationType' },
    { title: '物標情報対象方路', key: 'targetDirection' },
    { title: '物標情報対象センサ番号', key: 'targetSensorNumber' },
    { title: 'Last Update', key: 'updateTimeInfo', sort: sortByDate },
  ]
  setUseCaseList()
}

/**
 * ユースケース情報設定
 */
const setUseCaseList = async () => {
  isLoading.value = true
  updateUseCaseList()
    .then(() => {
      items.value = useCaseStore.dataForDisplay
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
