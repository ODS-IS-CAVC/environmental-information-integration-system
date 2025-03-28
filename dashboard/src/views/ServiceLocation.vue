<script setup lang="ts">
/**
 * ServiceLocation.vue
 * サービス地点情報コンポーネント
 */
// ==================================
// import
// ==================================
import { onBeforeMount, ref } from 'vue'

import { apiResponseErrorCode, updateServiceLocationList } from '@/mixins/communicationFunction'
import { sortByDate } from '@/mixins/dataTableFunction'

import { DIALOG_ERROR_INFO } from '@/setting/setting'

import DataTable from '@/components/common/DataTable.vue'
import ErrorDialog from '@/components/common/ErrorDialog.vue'
import Loading from '@/components/common/Loading.vue'
import TitleHeader from '@/components/common/TitleHeader.vue'
import { useServiceLocationRoadsideUnitStore, useServiceLocationStore } from '@/stores/app'
import type { ErrorDialogInfo, ServiceLocationForDisplay, ServiceLocationRoadsideUnitForDisplay, TableHeader } from '@/types/interfaces'

// ==================================
// data
// ==================================
const serviceLocationStore = useServiceLocationStore()

const serviceLocationRoadsideUnitStore = useServiceLocationRoadsideUnitStore()

const serviceLocationHeaders = ref<TableHeader[]>([])

const serviceLocationItems = ref<ServiceLocationForDisplay[]>([])

const roadsideUnitHeaders = ref<TableHeader[]>([])

const roadsideUnitItems = ref<ServiceLocationRoadsideUnitForDisplay[]>([])

const isLoading = ref<boolean>(false)

const errorDialog = ref<ErrorDialogInfo>({
  message: '',
  title: '',
  isShow: false,
})

const clickCount = ref<number>(0)

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
  serviceLocationHeaders.value = [
    { title: 'サービス地点ID', key: 'serviceLocationID' },
    { title: '緯度(度)', key: 'latitude' },
    { title: '経度(度)', key: 'longitude' },
    { title: '高度(m)', key: 'elevation' },
    { title: '接続方路数', key: 'approachAttributeSize' },
    { title: '方路ID', key: 'approachID' },
    { title: '方路接続方位', key: 'approachHeading' },
    { title: 'Last Update', key: 'updateTimeInfo', sort: sortByDate },
  ]

  roadsideUnitHeaders.value = [
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
    { title: 'Last Update', key: 'updateTimeInfo', sort:sortByDate },
  ]
  setServiceLocationList()
}

/**
 * サービス地点情報設定
 */
const setServiceLocationList = () => {
  isLoading.value = true
  updateServiceLocationList()
    .then(() => {
      serviceLocationItems.value = serviceLocationStore.dataForDisplay
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
* サービス地点別路側機属性情報テーブル表示
* @param item - 選択行データ
*/
 const displayRoadsideUnitTable = (item: ServiceLocationForDisplay) => {
  serviceLocationRoadsideUnitStore.setServiceLocationRoadsideUnitList(item.roadsideUnitList)
  roadsideUnitItems.value = serviceLocationRoadsideUnitStore.dataForDisplay
  clickCount.value += 1
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
  <v-container
    class="service-location"
    fill-height
  >
    <v-sheet class="service-location__sheet mb-10">
      <DataTable>
        <v-data-table
          hover
          :headers="serviceLocationHeaders"
          :items="serviceLocationItems"
          :item-per-page="10"
        >
          <template v-slot:item="{ item }">
              <tr @click="displayRoadsideUnitTable(item)">
                <td>{{ item.serviceLocationID }}</td>
                <td>{{ item.latitude }}</td>
                <td>{{ item.longitude }}</td>
                <td>{{ item.elevation }}</td>
                <td>{{ item.approachAttributeSize }}</td>
                <td>{{ item.approachID }}</td>
                <td>{{ item.approachHeading }}</td>
                <td>{{ item.updateTimeInfo }}</td>
              </tr>
          </template>
        </v-data-table>
      </DataTable>
    </v-sheet>
    <DataTable
      v-show="clickCount > 0"
      :headers="roadsideUnitHeaders"
      :items="roadsideUnitItems"
    />
  </v-container>
  <Loading v-show="isLoading" />
  <ErrorDialog
    :error-dialog="errorDialog"
    @on-click-close-error-dialog="onClickCloseErrorDialog"
  />
</template>
<style lang="scss" scoped>
@use '@/assets/styles/data-table.scss';
.service-location {
  &__sheet {
    min-height: 650px;
  }
  .v-data-table {
    tr {
      cursor: pointer;
    }
  }
}
</style>
