import {
  DEVICE_ALIVE_STATUS,
  DEVICE_CLASSIFICATION,
  DEVICE_LIST,
  MANUFACTURER_LIST,
  SERVICE_AVAILABILITY,
  MATERIAL_TYPE,
  USE_CASE_TYPE,
  USE_CASE_SUPPLEMENTARY,
  TARGET_UTILIZATION_TYPE,
  PREFECTURE,
  OPERATION_CLASSIFICATION_CODE,
  DEVICE_OPERATION_STATUS
} from '@/setting/setting'

import { defineStore } from 'pinia'

import type {
  AliveMonitoring,
  AliveMonitoringForDisplay,
  AliveMonitoringStore,
  DeviceAliveMonitoringForDisplay,
  DeviceAliveMonitoringStore,
  DeviceClassificationAliveInfo,
  ServiceLocation,
  ServiceLocationForDisplay,
  ServiceLocationStore,
  ServiceLocationRoadsideUnitForDisplay,
  ServiceLocationRoadsideUnitStore,
  RoadsideUnitList,
  RoadsideUnit,
  RoadsideUnitForDisplay,
  RoadsideUnitStore,
  UseCase,
  UseCaseForDisplay,
  UseCaseStore,
  Signal,
  SignalForDisplay,
  SignalStore,
  CommunicationMedia,
  CommunicationMediaForDisplay,
  CommunicationMediaStore
} from '@/types/interfaces'

// 死活監視情報
export const useAliveMonitoringStore = defineStore('aliveMonitoringStore', {
  state: () => ({
    aliveMonitoringList: [] as AliveMonitoring[],
  }),
  getters: {
    dataForDisplay: (state: AliveMonitoringStore): AliveMonitoringForDisplay[] => {
      const dataListForDisplay: AliveMonitoringForDisplay[] = []
      for (const aliveInfo of state.aliveMonitoringList) {
        const dataForDisplay: AliveMonitoringForDisplay = {
          serviceLocationID: '',
          roadsideUnitID: '',
          operationClassificationCode: '',
          serviceAvailability: '',
          deviceNum: 0,
          updateTimeInfo: '',
          deviceClassificationAliveInfo: []
        }
        const attribute = aliveInfo.attribute
        // サービス地点ID
        dataForDisplay.serviceLocationID = '0x' + attribute.serviceLocationID.toString(16).padStart(8, '0')
        // 路側機ID
        dataForDisplay.roadsideUnitID = '0x' + attribute.roadsideUnitID.toString(16).padStart(8, '0')
        // 運用状態
        dataForDisplay.operationClassificationCode = OPERATION_CLASSIFICATION_CODE[attribute.operationClassificationCode]
        // 稼働状態
        dataForDisplay.serviceAvailability = SERVICE_AVAILABILITY[attribute.serviceAvailability]
        // 使用センサ数
        for (const deviceInfo of attribute.deviceClassificationAliveInfo) {
          dataForDisplay.deviceNum += deviceInfo.deviceNum
        }
        // Last Update
        dataForDisplay.updateTimeInfo = getJstTime(attribute.updateTimeInfo)

        dataForDisplay.deviceClassificationAliveInfo = attribute.deviceClassificationAliveInfo

        dataListForDisplay.push(dataForDisplay)
      }
      return dataListForDisplay
    }
  },
  actions: {
    setAliveMonitoringList(val: AliveMonitoring[]) {
      this.aliveMonitoringList = val
    },
    clearData() {
      this.aliveMonitoringList = []
    }
  }
})

// 死活監視情報(デバイス別)
export const useDeviceAliveMonitoringStore = defineStore('deviceAliveMonitoringStore', {
  state: () => ({
    deviceAliveMonitoringList: [] as DeviceClassificationAliveInfo[],
  }),
  getters: {
    dataForDisplay: (state: DeviceAliveMonitoringStore): DeviceAliveMonitoringForDisplay[] => {
      const dataListForDisplay: DeviceAliveMonitoringForDisplay[] = []
      for (const aliveInfo of state.deviceAliveMonitoringList) {
        for (const deviceInfo of aliveInfo.deviceAliveInfo) {
          const dataForDisplay: DeviceAliveMonitoringForDisplay = {
            deviceClassification: '',
            deviceID: '',
            deviceType: '',
            manufacturerID: '',
            deviceUniqueNumber: '',
            deviceOperationStatus: '',
            deviceAliveStatus: ''
          }
          // 機器種別
          dataForDisplay.deviceClassification = DEVICE_CLASSIFICATION[aliveInfo.deviceClassification]

          const hexDeviceID = deviceInfo.deviceID.toString(16).padStart(6, '0')
          // 機器識別ID
          dataForDisplay.deviceID = '0x' + hexDeviceID

          const splittedDeviceID = hexDeviceID.match(/.{2}/g)
          if (splittedDeviceID != null) {
            // 機器タイプ
            const deviceType: string = '0x' + splittedDeviceID[0]
            dataForDisplay.deviceType = deviceType in DEVICE_LIST ? DEVICE_LIST[deviceType] : deviceType
            // メーカ番号
            const manufacturerID: string = '0x' + splittedDeviceID[1]
            dataForDisplay.manufacturerID = manufacturerID in MANUFACTURER_LIST ? MANUFACTURER_LIST[manufacturerID] : manufacturerID
            // 機器固有番号
            dataForDisplay.deviceUniqueNumber = '0x' + splittedDeviceID[2]
          }
          // 運用状態
          dataForDisplay.deviceOperationStatus = DEVICE_OPERATION_STATUS[deviceInfo.deviceOperationStatus]
          // 稼働状態
          dataForDisplay.deviceAliveStatus = DEVICE_ALIVE_STATUS[deviceInfo.deviceAliveStatus]

          dataListForDisplay.push(dataForDisplay)
        }
      }
      return dataListForDisplay
    }
  },
  actions: {
    setDeviceAliveMonitoringList(val: DeviceClassificationAliveInfo[]) {
      this.deviceAliveMonitoringList = val
    }
  }
})

// サービス地点情報
export const useServiceLocationStore = defineStore('serviceLocationStore', {
  state: () => ({
    serviceLocationList: [] as ServiceLocation[],
  }),
  getters: {
    dataForDisplay: (state: ServiceLocationStore): ServiceLocationForDisplay[] => {
      const dataListForDisplay: ServiceLocationForDisplay[] = []
      for (const ServiceLocation of state.serviceLocationList) {
        const dataForDisplay: ServiceLocationForDisplay = {
          serviceLocationID: '',
          latitude: 0,
          longitude: 0,
          elevation: 0,
          approachAttributeSize: 0,
          approachID: '',
          approachHeading: '',
          updateTimeInfo: '',
          roadsideUnitList: []
        }
        const attribute = ServiceLocation.attribute
        // サービス地点ID
        dataForDisplay.serviceLocationID = '0x' + attribute.serviceLocationID.toString(16).padStart(8, '0')
        // 緯度
        dataForDisplay.latitude = attribute.latitude === -2147483648 ? '不定値' : attribute.latitude/10 ** 7
        // 経度
        dataForDisplay.longitude = attribute.longitude === -2147483648 ? '不定値' : attribute.longitude/10 ** 7
        // 高度
        dataForDisplay.elevation = attribute.elevation === 61440 ? '不定値' : attribute.elevation/10
        // 接続方路数
        dataForDisplay.approachAttributeSize = attribute.approachAttributeSize
        const approachIDArray = []
        const approachHeadingArray = []
        for (const approachAttributeInfo of attribute.approachAttributeInfo) {
          approachIDArray.push(approachAttributeInfo.approachID)
          approachHeadingArray.push(approachAttributeInfo.approachHeading)
        }
        // 方路ID
        dataForDisplay.approachID = approachIDArray.join(', ')
        // 方路接続方位
        dataForDisplay.approachHeading = approachHeadingArray.join(', ')
        // Last Update
        dataForDisplay.updateTimeInfo = getJstTime(attribute.updateTimeInfo)

        dataForDisplay.roadsideUnitList = attribute.roadsideUnitList

        dataListForDisplay.push(dataForDisplay)
      }
      return dataListForDisplay
    }
  },
  actions: {
    setServiceLocationList(val: ServiceLocation[]) {
      this.serviceLocationList = val
    },
    clearData() {
      this.serviceLocationList = []
    }
  }
})

// 路側機属性情報(サービス地点別)
export const useServiceLocationRoadsideUnitStore = defineStore('serviceLocationRoadsideUnitStore', {
  state: () => ({
    serviceLocationRoadsideUnitList: [] as RoadsideUnitList[],
  }),
  getters: {
    dataForDisplay: (state: ServiceLocationRoadsideUnitStore): ServiceLocationRoadsideUnitForDisplay[] => {
      const dataListForDisplay: ServiceLocationRoadsideUnitForDisplay[] = []
      for (const serviceLocationInfo of state.serviceLocationRoadsideUnitList) {
          const dataForDisplay: ServiceLocationRoadsideUnitForDisplay = {
            roadsideUnitID: '',
            roadsideUnitName: '',
            productNumber: '',
            manufacturer: '',
            customer: '',
            licensingInfo: '',
            initialRegistrationDate: '',
            powerConsumption: 0,
            grossWeight: 0,
            materialType: '',
            dateOfInstallation: '',
            latitude: 0,
            longitude: 0,
            roadsideUnitManager: '',
            installationSiteManager: '',
            lastInspectionDate: '',
            nextInspectionDate: '',
            updateTimeInfo: '',
          }
          const attribute = serviceLocationInfo.attribute
          // 路側機ID
          dataForDisplay.roadsideUnitID = '0x' + attribute.roadsideUnitID.toString(16).padStart(8, '0')
          // 路側機名称
          dataForDisplay.roadsideUnitName = attribute.roadsideUnitName
          // 路側機型番
          dataForDisplay.productNumber = attribute.productNumber
          // 路側機製造者
          dataForDisplay.manufacturer = attribute.manufacturer
          // 路側機発注者
          dataForDisplay.customer = attribute.customer
          // 認可関連情報
          dataForDisplay.licensingInfo = attribute.licensingInfo
          // 初期登録日
          dataForDisplay.initialRegistrationDate = attribute.initialRegistrationDate.replace(/T[\d:.]+Z$/, '')
          // 路側機消費電力
          dataForDisplay.powerConsumption = attribute.powerConsumption
          // 路側機重量
          dataForDisplay.grossWeight = attribute.grossWeight
          // 路側機設置種別
          dataForDisplay.materialType = MATERIAL_TYPE[attribute.materialType]
          // 路側機設置年月日
          dataForDisplay.dateOfInstallation = attribute.dateOfInstallation.replace(/T[\d:.]+Z$/, '')
          // 緯度
          dataForDisplay.latitude = attribute.latitude === -2147483648 ? '不定値' : attribute.latitude/10 ** 7
          // 経度
          dataForDisplay.longitude = attribute.longitude === -2147483648 ? '不定値' : attribute.longitude/10 ** 7
          // 路側機管理者
          dataForDisplay.roadsideUnitManager = attribute.roadsideUnitManager
          // 設置地管理者
          dataForDisplay.installationSiteManager = attribute.installationSiteManager
          // 最終点検日
          dataForDisplay.lastInspectionDate = attribute.lastInspectionDate.replace(/T[\d:.]+Z$/, '')
          // 次回点検日
          dataForDisplay.nextInspectionDate = attribute.nextInspectionDate.replace(/T[\d:.]+Z$/, '')
          // Last Update
          dataForDisplay.updateTimeInfo = getJstTime(attribute.updateTimeInfo)

          dataListForDisplay.push(dataForDisplay)
      }
      return dataListForDisplay
    }
  },
  actions: {
    setServiceLocationRoadsideUnitList(val: RoadsideUnitList[]) {
      this.serviceLocationRoadsideUnitList = val
    }
  }
})

// 路側機属性情報
export const useRoadsideUnitStore = defineStore('roadsideUnitStore', {
  state: () => ({
    roadsideUnitList: [] as RoadsideUnit[],
  }),
  getters: {
    dataForDisplay: (state: RoadsideUnitStore): RoadsideUnitForDisplay[] => {
      const dataListForDisplay: RoadsideUnitForDisplay[] = []
      for (const roadsideUnit of state.roadsideUnitList) {
        const dataForDisplay: RoadsideUnitForDisplay = {
          serviceLocationID: '',
          roadsideUnitID: '',
          roadsideUnitName: '',
          productNumber: '',
          manufacturer: '',
          customer: '',
          licensingInfo: '',
          initialRegistrationDate: '',
          powerConsumption: 0,
          grossWeight: 0,
          materialType: '',
          dateOfInstallation: '',
          latitude: 0,
          longitude: 0,
          roadsideUnitManager: '',
          installationSiteManager: '',
          lastInspectionDate: '',
          nextInspectionDate: '',
          updateTimeInfo: '',
        }
        const attribute = roadsideUnit.attribute
        // サービス地点ID
        dataForDisplay.serviceLocationID = '0x' + attribute.serviceLocationID.toString(16).padStart(8, '0')
        // 路側機ID
        dataForDisplay.roadsideUnitID = '0x' + attribute.roadsideUnitID.toString(16).padStart(8, '0')
        // 路側機名称
        dataForDisplay.roadsideUnitName = attribute.roadsideUnitName
        // 路側機型番
        dataForDisplay.productNumber = attribute.productNumber
        // 路側機製造者
        dataForDisplay.manufacturer = attribute.manufacturer
        // 路側機発注者
        dataForDisplay.customer = attribute.customer
        // 認可関連情報
        dataForDisplay.licensingInfo = attribute.licensingInfo
        // 初期登録日
        dataForDisplay.initialRegistrationDate = attribute.initialRegistrationDate.replace(/T[\d:.]+Z$/, '')
        // 路側機消費電力
        dataForDisplay.powerConsumption = attribute.powerConsumption
        // 路側機重量
        dataForDisplay.grossWeight = attribute.grossWeight
        // 路側機設置種別
        dataForDisplay.materialType = MATERIAL_TYPE[attribute.materialType]
        // 路側機設置年月日
        dataForDisplay.dateOfInstallation = attribute.dateOfInstallation.replace(/T[\d:.]+Z$/, '')
        // 緯度
        dataForDisplay.latitude = attribute.latitude === -2147483648 ? '不定値' : attribute.latitude/10 ** 7
        // 経度
        dataForDisplay.longitude = attribute.longitude === -2147483648 ? '不定値' : attribute.longitude/10 ** 7
        // 路側機管理者
        dataForDisplay.roadsideUnitManager = attribute.roadsideUnitManager
        // 設置地管理者
        dataForDisplay.installationSiteManager = attribute.installationSiteManager
        // 最終点検日
        dataForDisplay.lastInspectionDate = attribute.lastInspectionDate.replace(/T[\d:.]+Z$/, '')
        // 次回点検日
        dataForDisplay.nextInspectionDate = attribute.nextInspectionDate.replace(/T[\d:.]+Z$/, '')
        // Last Update
        dataForDisplay.updateTimeInfo = getJstTime(attribute.updateTimeInfo)

        dataListForDisplay.push(dataForDisplay)
      }
      return dataListForDisplay
    }
  },
  actions: {
    setRoadsideUnitList(val: RoadsideUnit[]) {
      this.roadsideUnitList = val
    },
    clearData() {
      this.roadsideUnitList = []
    }
  }
})

// ユースケース情報
export const useUseCaseStore = defineStore('useCaseStore', {
  state: () => ({
    useCaseList: [] as UseCase[],
  }),
  getters: {
    dataForDisplay: (state: UseCaseStore): UseCaseForDisplay[] => {
      const dataListForDisplay: UseCaseForDisplay[] = []
      for (const useCase of state.useCaseList) {
        for (const useCaseInfo of useCase.attribute.useCaseInfo) {
          for (const useCaseClassificationInfo of useCaseInfo.useCaseClassificationInfo) {
            const dataForDisplay: UseCaseForDisplay = {
              serviceLocationID: '',
              roadsideUnitID: '',
              useCaseType: '',
              useCaseSupplementary: '',
              targetUtilizationType: '',
              targetDirection: 0,
              targetSensorNumber: 0,
              updateTimeInfo: ''
            }
            const attribute = useCase.attribute
            // サービス地点ID
            dataForDisplay.serviceLocationID = '0x' + attribute.serviceLocationID.toString(16).padStart(8, '0')
            // 路側機ID
            dataForDisplay.roadsideUnitID = '0x' + attribute.roadsideUnitID.toString(16).padStart(8, '0')
            // 対象ユースケース類型
            dataForDisplay.useCaseType = USE_CASE_TYPE[useCaseClassificationInfo.useCaseType]
            // 対象ユースケースケース補足
            dataForDisplay.useCaseSupplementary = useCaseClassificationInfo.useCaseSupplementaryCode ? getValueFromBinaryFlags(USE_CASE_SUPPLEMENTARY, useCaseClassificationInfo.useCaseSupplementaryCode) : ''
            // 対象活用類型
            dataForDisplay.targetUtilizationType = getValueFromBinaryFlags(TARGET_UTILIZATION_TYPE, useCaseClassificationInfo.targetUtilizationType)
            // 物標情報対象方路
            dataForDisplay.targetDirection = useCaseClassificationInfo.targetDirection ? useCaseClassificationInfo.targetDirection : ''
            // 物標情報対象センサ番号
            dataForDisplay.targetSensorNumber = useCaseClassificationInfo.targetSensorNumber ? useCaseClassificationInfo.targetSensorNumber : ''
            // Last Update
            dataForDisplay.updateTimeInfo = getJstTime(attribute.updateTimeInfo)

            dataListForDisplay.push(dataForDisplay)
          }
        }
      }
      return dataListForDisplay
    }
  },
  actions: {
    setUseCaseList(val: UseCase[]) {
      this.useCaseList = val
    },
    clearData() {
      this.useCaseList = []
    }
  }
})

// 信号情報
export const useSignalStore = defineStore('signalStore', {
  state: () => ({
    signalList: [] as Signal[],
  }),
  getters: {
    dataForDisplay: (state: SignalStore): SignalForDisplay[] => {
      const dataListForDisplay: SignalForDisplay[] = []
      for (const signal of state.signalList) {
        const dataForDisplay: SignalForDisplay = {
          serviceLocationID: '',
          roadsideUnitID: '',
          prefecture: '',
          roadType: '',
          intersectionID: 0,
          updateTimeInfo: '',
        }
        const attribute = signal.attribute
        // サービス地点ID
        dataForDisplay.serviceLocationID = '0x' + attribute.serviceLocationID.toString(16).padStart(8, '0')
        // 路側機ID
        dataForDisplay.roadsideUnitID = '0x' + attribute.roadsideUnitID.toString(16).padStart(8, '0')
        // 都道府県
        dataForDisplay.prefecture = PREFECTURE[attribute.prefectureID]
        // 提供点種別
        dataForDisplay.roadType = attribute.roadType ? '交差点' : '単路'
        // 交差点ID／単路ID
        dataForDisplay.intersectionID = attribute.intersectionID
        // Last Update
        dataForDisplay.updateTimeInfo = getJstTime(attribute.updateTimeInfo)

        dataListForDisplay.push(dataForDisplay)
      }
      return dataListForDisplay
    }
  },
  actions: {
    setSignalList(val: Signal[]) {
      this.signalList = val
    },
    clearData() {
      this.signalList = []
    }
  }
})

// 通信メディア情報
export const useCommunicationMediaStore = defineStore('communicationMediaStore', {
  state: () => ({
    communicationMediaList: [] as CommunicationMedia[],
  }),
  getters: {
    dataForDisplay: (state: CommunicationMediaStore): CommunicationMediaForDisplay[] => {
      const dataListForDisplay: CommunicationMediaForDisplay[] = []
      for (const communicationMedia of state.communicationMediaList) {
        const dataForDisplay: CommunicationMediaForDisplay = {
          serviceLocationID: '',
          roadsideUnitID: '',
          communicationMediaNum: 0,
          communicationMediaIDs: '',
          updateTimeInfo: '',
        }
        const attribute = communicationMedia.attribute
        // サービス地点ID
        dataForDisplay.serviceLocationID = '0x' + attribute.serviceLocationID.toString(16).padStart(8, '0')
        // 路側機ID
        dataForDisplay.roadsideUnitID = '0x' + attribute.roadsideUnitID.toString(16).padStart(8, '0')
        // 対応通信メディア数
        dataForDisplay.communicationMediaNum = attribute.communicationMediaNum
        // 機器識別ID
        dataForDisplay.communicationMediaIDs = attribute.communicationMediaIDs.join(', ')
        // Last Update
        dataForDisplay.updateTimeInfo = getJstTime(attribute.updateTimeInfo)

        dataListForDisplay.push(dataForDisplay)
      }
      return dataListForDisplay
    }
  },
  actions: {
    setCommunicationMediaList(val: CommunicationMedia[]) {
      this.communicationMediaList = val
    },
    clearData() {
      this.communicationMediaList = []
    }
  }
})

/**
 * UTC表記をJST表記に変換
 * @param utcTime - UTC表記の時間
 * @return JST表記の時間
 */
function getJstTime(utcTime: string):string {
  let jstTime = '' 
  const date = new Date(utcTime)
  jstTime = date.toLocaleString('ja-JP', {
      timeZone: 'Asia/Tokyo',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
  })
  return jstTime
}

/**
 * 2進数のフラグでオブジェクトから値を取得する
 * @param messages - 定義されているオブジェクト
 * @param value - オブジェクトから取得するための数値
 * @return 取得された値をコンマ区切りの文字列にして返却
 */
function getValueFromBinaryFlags(messages: Record<number, string>, value: number):string {
  const array = []
  if (value === 0) {
    array.push(messages[0])
  } else {
    const bin = value.toString(2)
    for (let i = 0; i < bin.length; i++) {
      const digitVal = value & 1<<i
      if (digitVal > 0) array.push(messages[digitVal])
    }
  }
  return array.join(',')
}