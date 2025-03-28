<script setup lang="ts">
/**
 * AliveMonitoring.vue
 * 死活監視情報コンポーネント
 */
// ==================================
// import
// ==================================
import { onBeforeMount, ref } from 'vue'

import { apiResponseErrorCode, updateAliveMonitoringList } from '@/mixins/communicationFunction'
import { sortByDate } from '@/mixins/dataTableFunction'

import { DIALOG_ERROR_INFO } from '@/setting/setting'

import DataTable from '@/components/common/DataTable.vue'
import ErrorDialog from '@/components/common/ErrorDialog.vue'
import Loading from '@/components/common/Loading.vue'
import TitleHeader from '@/components/common/TitleHeader.vue'
import { useAliveMonitoringStore, useDeviceAliveMonitoringStore } from '@/stores/app'
import type { AliveMonitoringForDisplay, DeviceAliveMonitoringForDisplay, ErrorDialogInfo, TableHeader } from '@/types/interfaces'

// ==================================
// data
// ==================================
const aliveMonitoringStore = useAliveMonitoringStore()

const deviceAliveMonitoringStore = useDeviceAliveMonitoringStore()

const aliveMonitoringHeaders = ref<TableHeader[]>([])

const aliveMonitoringItems = ref<AliveMonitoringForDisplay[]>([])

const deviceAliveMonitoringHeaders = ref<TableHeader[]>([])

const deviceAliveMonitoringItems = ref<DeviceAliveMonitoringForDisplay[]>([])

const isLoading = ref<boolean>(false)

const clickCount = ref<number>(0)

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
  aliveMonitoringHeaders.value = [
    { title: 'サービス地点ID', key: 'serviceLocationID' },
    { title: '路側機ID', key: 'roadsideUnitID' },
    { title: '運用状態', key: 'operationClassificationCode' },
    { title: '稼働状態', key: 'serviceAvailability' },
    { title: '使用センサ数', key: 'deviceNum' },
    { title: 'Last Update', key: 'updateTimeInfo' , sort: sortByDate},
  ]

  deviceAliveMonitoringHeaders.value = [
    { title: '機器識別ID', key: 'deviceID' },
    { title: '機器種別', key: 'deviceClassification' },
    { title: '機器タイプ', key: 'deviceType' },
    { title: 'メーカ番号', key: 'manufacturerID' },
    { title: '機器固有番号', key: 'deviceUniqueNumber' },
    { title: '運用状態', key: 'deviceOperationStatus' },
    { title: '稼働状態', key: 'deviceAliveStatus' },
  ]
  setAliveMonitoringList()
}

/**
 * 死活監視情報設定
 */
const setAliveMonitoringList = () => {
  isLoading.value = true
  updateAliveMonitoringList()
    .then(() => {
      aliveMonitoringItems.value = aliveMonitoringStore.dataForDisplay
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
 * デバイス別死活監視テーブル表示
* @param item - 選択行データ
 */
const displayDeviceTable = (item: AliveMonitoringForDisplay) => {
  deviceAliveMonitoringStore.setDeviceAliveMonitoringList(item.deviceClassificationAliveInfo)
  deviceAliveMonitoringItems.value = deviceAliveMonitoringStore.dataForDisplay
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
    class="alive-monitoring"
    fill-height
  >
    <v-sheet class="alive-monitoring__sheet mb-10">
      <DataTable>
        <v-data-table
          hover
          :headers="aliveMonitoringHeaders"
          :items="aliveMonitoringItems"
          :item-per-page="10"
        >
          <template v-slot:item="{ item }">
            <tr
              class="alive-monitoring__tr"
              :class="{ 'alive-monitoring__tr--danger': item.serviceAvailability != '● サービス提供可'}"
              @click="displayDeviceTable(item)"
            >
              <td>{{ item.serviceLocationID }}</td>
              <td>{{ item.roadsideUnitID }}</td>
              <td
                class="alive-monitoring__td"
                :class="item.operationClassificationCode == '運用中' ? 'alive-monitoring__td--active' : 'alive-monitoring__td--caution'"
              >
                {{ item.operationClassificationCode }}
              </td>
              <td
                class="alive-monitoring__td"
                :class="item.serviceAvailability == '● サービス提供可' ? 'alive-monitoring__td--active' : 'alive-monitoring__td--passive'"
              >
                {{ item.serviceAvailability }}
              </td>
              <td>{{ item.deviceNum }}</td>
              <td>{{ item.updateTimeInfo }}</td>
            </tr>
          </template>
        </v-data-table>
      </DataTable>
    </v-sheet>
    <DataTable
      v-show="clickCount > 0"
      class="alive-monitoring__device-table"
    >
      <v-data-table
        hover
        :headers="deviceAliveMonitoringHeaders"
        :items="deviceAliveMonitoringItems"
        :item-per-page="10"
      >
        <template v-slot:item="{ item }">
          <tr
            :class="{ 'alive-monitoring__device-table--danger': item.deviceAliveStatus != '● 正常稼働中'}"
          >
            <td>{{ item.deviceID }}</td>
            <td>{{ item.deviceClassification }}</td>
            <td>{{ item.deviceType }}</td>
            <td>{{ item.manufacturerID }}</td>
            <td>{{ item.deviceUniqueNumber }}</td>
            <td
              :class="item.deviceOperationStatus == '運用中' ? 'alive-monitoring__device-table--active' : 'alive-monitoring__device-table--caution'"
            >
              {{ item.deviceOperationStatus }}
            </td>
            <td
              :class="item.deviceAliveStatus == '● 正常稼働中' ? 'alive-monitoring__device-table--active' : 'alive-monitoring__device-table--passive'"
            >
              {{ item.deviceAliveStatus }}
            </td>
          </tr>
        </template>
      </v-data-table>
    </DataTable>
  </v-container>
  <Loading v-show="isLoading" />
  <ErrorDialog
    :error-dialog="errorDialog"
    @on-click-close-error-dialog="onClickCloseErrorDialog"
  />
</template>
<style lang="scss" scoped>
@use '@/assets/styles/data-table.scss';
.alive-monitoring {
  &__sheet {
    min-height: 650px;
  }
  &__tr {
    cursor: pointer;
    &--danger {
      background: rgb(var(--v-theme-danger)) !important;
      td:first-child {
        background: rgb(var(--v-theme-danger)) !important;
      }
    }
  }
  &__td {
    &--active {
      color: rgb(var(--v-theme-active))
    }
    &--passive {
      color: rgb(var(--v-theme-passive))
    }
    &--caution {
      color: rgb(var(--v-theme-caution))
    }
  }
  &__device-table {
    &--danger {
      background: rgb(var(--v-theme-danger)) !important;
      td:first-child {
        background: rgb(var(--v-theme-danger)) !important;
      }
    }
    &--active {
      color: rgb(var(--v-theme-active))
    }
    &--passive {
      color: rgb(var(--v-theme-passive))
    }
    &--caution {
      color: rgb(var(--v-theme-caution))
    }
  }
}
</style>
