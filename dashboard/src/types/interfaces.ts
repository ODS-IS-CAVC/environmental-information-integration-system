/**
 * Interfaces.ts
 * インターフェース保存用ファイル
 */

// ==================================
// Common
// ==================================
// メニュー情報
export interface MenuInfo {
  name: string;
  text: string;
  path?: string;
}

// テーブルヘッダ
export interface TableHeader {
  title: string;
  key: string;
  sort?: any;
}

// エラーダイアログ
export interface ErrorDialogInfo {
  message: string;
  title: string;
  isShow: boolean;
}

// ==================================
// 死活監視
// ==================================
// API
export interface AliveMonitoring {
  dataModelType: string;
  attribute: AliveMonitoringAttribute
}
export interface AliveMonitoringAttribute {
  serviceLocationID: number;
  roadsideUnitID: number;
  updateTimeInfo: string;
  formatVersion: number;
  operationClassificationCode: number;
  serviceAvailability: number;
  deviceClassificationNum: number;
  deviceClassificationAliveInfo: DeviceClassificationAliveInfo[]
}
export interface DeviceClassificationAliveInfo {
  deviceClassification: number;
  deviceNum: number;
  deviceAliveInfo: DeviceAliveInfo[];
}
export interface DeviceAliveInfo {
  deviceID: number;
  deviceOperationStatus: number;
  deviceAliveStatus: number;
}

// Store
export interface AliveMonitoringStore {
  aliveMonitoringList: AliveMonitoring[]
}

export interface AliveMonitoringForDisplay {
  serviceLocationID: string;
  roadsideUnitID: string;
  operationClassificationCode: string;
  serviceAvailability: string;
  deviceNum: number;
  updateTimeInfo: string;
  deviceClassificationAliveInfo: DeviceClassificationAliveInfo[]
}

export interface DeviceAliveMonitoringStore {
  deviceAliveMonitoringList: DeviceClassificationAliveInfo[]
}

export interface DeviceAliveMonitoringForDisplay {
  deviceClassification: string;
  deviceID: string;
  deviceType: string;
  manufacturerID: string;
  deviceUniqueNumber: string;
  deviceOperationStatus: string;
  deviceAliveStatus: string;
}

// ==================================
// サービス地点
// ==================================
// API
export interface ServiceLocation {
  dataModelType: string;
  attribute: ServiceLocationAttribute
}
export interface ServiceLocationAttribute {
  updateTimeInfo: string;
  formatVersion: number;
  serviceLocationID: number;
  latitude: number;
  longitude: number;
  elevation: number;
  approachAttributeSize: number;
  approachAttributeInfo: ApproachAttributeInfo[];
  roadsideUnitList: RoadsideUnitList[];
}

export interface ApproachAttributeInfo {
  approachID: number;
  approachHeading: number;
}

export interface RoadsideUnitList {
  dataModelType: string;
  attribute: RoadsideUnitAttribute
}

export interface RoadsideUnitAttribute {
  serviceLocationID: number;
  roadsideUnitID: number;
  updateTimeInfo: string;
  formatVersion: number;
  roadsideUnitName: string;
  productNumber: string;
  manufacturer: string;
  customer: string;
  licensingInfo: string;
  initialRegistrationDate: string;
  powerConsumption: number;
  grossWeight: number;
  materialType: number;
  dateOfInstallation: string;
  latitude: number;
  longitude: number;
  roadsideUnitManager: string;
  installationSiteManager: string;
  lastInspectionDate: string;
  nextInspectionDate: string;
}

// Store
export interface ServiceLocationStore {
  serviceLocationList: ServiceLocation[]
}

export interface ServiceLocationForDisplay {
  serviceLocationID: string;
  latitude: number | string;
  longitude: number | string;
  elevation: number | string;
  approachAttributeSize: number;
  approachID: string;
  approachHeading: string;
  updateTimeInfo: string;
  roadsideUnitList: RoadsideUnitList[]
}

export interface ServiceLocationRoadsideUnitStore {
  serviceLocationRoadsideUnitList: RoadsideUnitList[]
}

export interface ServiceLocationRoadsideUnitForDisplay {
  roadsideUnitID: string;
  roadsideUnitName: string;
  productNumber: string;
  manufacturer: string;
  customer: string;
  licensingInfo: string;
  initialRegistrationDate: string;
  powerConsumption: number;
  grossWeight: number;
  materialType: string;
  dateOfInstallation: string;
  latitude: number | string;
  longitude: number | string;
  roadsideUnitManager: string;
  installationSiteManager: string;
  lastInspectionDate: string;
  nextInspectionDate: string;
  updateTimeInfo: string;
}

// ==================================
// 路側機属性
// ==================================
// API
export interface RoadsideUnit {
  dataModelType: string;
  attribute: RoadsideUnitAttribute
}
export interface RoadsideUnitAttribute {
  serviceLocationID: number;
  roadsideUnitID: number;
  updateTimeInfo: string;
  formatVersion: number;
  roadsideUnitName: string;
  productNumber: string;
  manufacturer: string;
  customer: string;
  licensingInfo: string;
  initialRegistrationDate: string;
  powerConsumption: number;
  grossWeight: number;
  materialType: number;
  dateOfInstallation: string;
  latitude: number;
  longitude: number;
  roadsideUnitManager: string;
  installationSiteManager: string;
  lastInspectionDate: string;
  nextInspectionDate: string;
}

// Store
export interface RoadsideUnitStore {
  roadsideUnitList: RoadsideUnit[]
}

export interface RoadsideUnitForDisplay {
  serviceLocationID: string;
  roadsideUnitID: string;
  roadsideUnitName: string;
  productNumber: string;
  manufacturer: string;
  customer: string;
  licensingInfo: string;
  initialRegistrationDate: string;
  powerConsumption: number;
  grossWeight: number;
  materialType: string;
  dateOfInstallation: string;
  latitude: number | string;
  longitude: number | string;
  roadsideUnitManager: string;
  installationSiteManager: string;
  lastInspectionDate: string;
  nextInspectionDate: string;
  updateTimeInfo: string;
}

// ==================================
// ユースケース
// ==================================
// API
export interface UseCase {
  dataModelType: string;
  attribute: UseCaseAttribute
}
export interface UseCaseAttribute {
  serviceLocationID: number;
  roadsideUnitID: number;
  updateTimeInfo: string;
  formatVersion: number;
  useCaseInfo: useCaseInfo[];
}
export interface useCaseInfo {
  useCaseNum: number;
  useCaseClassificationInfo: useCaseClassificationInfo[];
}
export interface useCaseClassificationInfo {
  useCaseType: number;
  useCaseSupplementaryCode: number;
  targetUtilizationType: number;
  targetDirection: number;
  targetSensorNumber: number;
}

// Store
export interface UseCaseStore {
  useCaseList: UseCase[]
}

export interface UseCaseForDisplay {
  serviceLocationID: string;
  roadsideUnitID: string;
  useCaseType: string;
  useCaseSupplementary: string;
  targetUtilizationType: string;
  targetDirection: number | string;
  targetSensorNumber: number | string;
  updateTimeInfo: string;
}

// ==================================
// 信号
// ==================================
// API
export interface Signal {
  dataModelType: string;
  attribute: SignalAttribute
}
export interface SignalAttribute {
  serviceLocationID: number;
  roadsideUnitID: number;
  updateTimeInfo: string;
  formatVersion: number;
  prefectureID: number;
  roadType: number;
  intersectionID: number;
}

// Store
export interface SignalStore {
  signalList: Signal[]
}

export interface SignalForDisplay {
  serviceLocationID: string;
  roadsideUnitID: string;
  prefecture: string;
  roadType: string;
  intersectionID: number;
  updateTimeInfo: string;
}

// ==================================
// 通信メディア
// ==================================
// API
export interface CommunicationMedia {
  dataModelType: string;
  attribute: CommunicationMediaAttribute
}
export interface CommunicationMediaAttribute {
  serviceLocationID: number;
  roadsideUnitID: number;
  updateTimeInfo: string;
  formatVersion: number;
  communicationMediaNum: number;
  communicationMediaIDs: number[];
}

// Store
export interface CommunicationMediaStore {
  communicationMediaList: CommunicationMedia[]
}

export interface CommunicationMediaForDisplay {
  serviceLocationID: string;
  roadsideUnitID: string;
  communicationMediaNum: number;
  communicationMediaIDs: string;
  updateTimeInfo: string;
}