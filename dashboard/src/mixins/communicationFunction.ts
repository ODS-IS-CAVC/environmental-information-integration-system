import { ApiError, get } from 'aws-amplify/api'

import {
  useAliveMonitoringStore,
  useSignalStore,
  useCommunicationMediaStore,
  useUseCaseStore,
  useRoadsideUnitStore,
  useServiceLocationStore
} from '@/stores/app'

// エラーコード種別
export const apiResponseErrorCode = {
  success: 200,
  noContent: 204,
  badRequest: 400,
  internalServerError: 500,
}

/**
 * 死活監視情報更新
 * @returns statusCode ステータスコード
 */
export const updateAliveMonitoringList = async () => {
  const aliveMonitoringStore = useAliveMonitoringStore()
  aliveMonitoringStore.clearData()
  try {
    const restOperation = get({
      apiName: 'admin',
      path: '/aliveMonitoringInfo',
      options: {
        headers: {
          'X-Api-Key': import.meta.env.VITE_ADMIN_API_KEY,
        }
      }
    })

    const { statusCode, body } = await restOperation.response
    if (statusCode === apiResponseErrorCode.noContent) {
      throw apiResponseErrorCode.noContent
    }

    const response = await body.text()
    let data = JSON.parse(response)

    aliveMonitoringStore.setAliveMonitoringList(data)
    return statusCode
  } catch (e) {
    if (e instanceof ApiError) {
      if (e.response) throw e.response.statusCode
    }
    throw e
  }
}

/**
 * サービス地点情報更新
 * @returns statusCode ステータスコード
 */
export const updateServiceLocationList = async () => {
  const serviceLocationStore = useServiceLocationStore()
  serviceLocationStore.clearData()
  try {
    const restOperation = get({
      apiName: 'admin',
      path: '/serviceLocationInfo',
      options: {
        headers: {
          'X-Api-Key': import.meta.env.VITE_ADMIN_API_KEY,
        }
      }
    })

    const { statusCode, body } = await restOperation.response
    if (statusCode === apiResponseErrorCode.noContent) {
      throw apiResponseErrorCode.noContent
    }

    const response = await body.text()
    let data = JSON.parse(response)

    serviceLocationStore.setServiceLocationList(data)
    return statusCode
  } catch (e) {
    if (e instanceof ApiError) {
      if (e.response) throw e.response.statusCode
    }
    throw e
  }
}

/**
 * 路側機属性情報更新
 * @returns statusCode ステータスコード
 */
export const updateRoadsideUnitList = async () => {
  const roadsideUnitStore = useRoadsideUnitStore()
  roadsideUnitStore.clearData()
  try {
    const restOperation = get({
      apiName: 'admin',
      path: '/roadsideUnitInfo',
      options: {
        headers: {
          'X-Api-Key': import.meta.env.VITE_ADMIN_API_KEY,
        }
      }
    })

    const { statusCode, body } = await restOperation.response
    if (statusCode === apiResponseErrorCode.noContent) {
      throw apiResponseErrorCode.noContent
    }

    const response = await body.text()
    let data = JSON.parse(response)

    roadsideUnitStore.setRoadsideUnitList(data)
    return statusCode
  } catch (e) {
    if (e instanceof ApiError) {
      if (e.response) throw e.response.statusCode
    }
    throw e
  }
}

/**
 * ユースケース情報更新
 * @returns statusCode ステータスコード
 */
export const updateUseCaseList = async () => {
  const useCaseStore = useUseCaseStore()
  useCaseStore.clearData()
  try {
    const restOperation = get({
      apiName: 'admin',
      path: '/useCaseInfo',
      options: {
        headers: {
          'X-Api-Key': import.meta.env.VITE_ADMIN_API_KEY,
        }
      }
    })

    const { statusCode, body } = await restOperation.response
    if (statusCode === apiResponseErrorCode.noContent) {
      throw apiResponseErrorCode.noContent
    }

    const response = await body.text()
    let data = JSON.parse(response)
    useCaseStore.setUseCaseList(data)
    return statusCode
  } catch (e) {
    if (e instanceof ApiError) {
      if (e.response) throw e.response.statusCode
    }
    throw e
  }
}

/**
 * 信号情報更新
 * @returns statusCode ステータスコード
 */
export const updateSignalList = async () => {
  const signalStore = useSignalStore()
  signalStore.clearData()
  try {
    const restOperation = get({
      apiName: 'admin',
      path: '/signalInfo',
      options: {
        headers: {
          'X-Api-Key': import.meta.env.VITE_ADMIN_API_KEY,
        }
      }
    })

    const { statusCode, body } = await restOperation.response
    if (statusCode === apiResponseErrorCode.noContent) {
      throw apiResponseErrorCode.noContent
    }

    const response = await body.text()
    let data = JSON.parse(response)

    signalStore.setSignalList(data)
    return statusCode
  } catch (e) {
    if (e instanceof ApiError) {
      if (e.response) throw e.response.statusCode
    }
    throw e
  }
}

/**
 * 通信メディア情報更新
 * @returns statusCode ステータスコード
 */
export const updateCommunicationMediaList = async () => {
  const communicationMediaStore = useCommunicationMediaStore()
  communicationMediaStore.clearData()
  try {
    const restOperation = get({
      apiName: 'admin',
      path: '/communicationMediaInfo',
      options: {
        headers: {
          'X-Api-Key': import.meta.env.VITE_ADMIN_API_KEY,
        }
      }
    })

    const { statusCode, body } = await restOperation.response
    if (statusCode === apiResponseErrorCode.noContent) {
      throw apiResponseErrorCode.noContent
    }

    const response = await body.text()
    let data = JSON.parse(response)

    communicationMediaStore.setCommunicationMediaList(data)
    return statusCode
  } catch (e) {
    if (e instanceof ApiError) {
      if (e.response) throw e.response.statusCode
    }
    throw e
  }
}
