<script setup lang="ts">
/**
 * RoadsideUnit.vue
 * 路側機属性情報コンポーネント
 */
// ==================================
// import
// ==================================
import { onBeforeMount, ref } from 'vue'

import { apiResponseErrorCode, updateRoadsideUnitList } from '@/mixins/communicationFunction'
import { sortByDate } from '@/mixins/dataTableFunction'

import { DIALOG_ERROR_INFO } from '@/setting/setting'

import DataTable from '@/components/common/DataTable.vue'
import ErrorDialog from '@/components/common/ErrorDialog.vue'
import Loading from '@/components/common/Loading.vue'
import TitleHeader from '@/components/common/TitleHeader.vue'
import { useRoadsideUnitStore } from '@/stores/app'
import type { ErrorDialogInfo, RoadsideUnitForDisplay, TableHeader } from '@/types/interfaces'

// ==================================
// data
// ==================================
const roadsideUnitStore = useRoadsideUnitStore()

const headers = ref<TableHeader[]>([])

const items = ref<RoadsideUnitForDisplay[]>([])

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
    { title: '路側機名称', key: 'roadsideUnitName' },
    { title: '路側機型番', key: 'productNumber' },
    { title: '路側機製造者', key: 'manufacturer' },
    { title: '路側機発注者', key: 'customer' },
    { title: '認可関連情報', key: 'licensingInfo' },
    { title: '初期登録日', key: 'initialRegistrationDate' },
    { title: '路側機消費電力', key: 'powerConsumption' },
    { title: '路側機重量', key: 'grossWeight' },
    { title: '路側機設置種別', key: 'materialType' },
    { title: '路側機設置年月日', key: 'dateOfInstallation' },
    { title: '緯度(度)', key: 'latitude' },
    { title: '経度(度)', key: 'longitude' },
    { title: '路側機管理者', key: 'roadsideUnitManager' },
    { title: '設置地管理者', key: 'installationSiteManager' },
    { title: '最終点検日', key: 'lastInspectionDate' },
    { title: '次回点検日', key: 'nextInspectionDate' },
    { title: 'Last Update', key: 'updateTimeInfo', sort: sortByDate },
  ]
  setRoadsideUnitList()
}

/**
 * 路側機属性情報設定
 */
const setRoadsideUnitList = async () => {
  isLoading.value = true
  updateRoadsideUnitList()
    .then(() => {
      items.value = roadsideUnitStore.dataForDisplay
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
