export const MENU = [
  { name: 'top', text: 'TOP'},
  { name: 'aliveMonitoring', text: '死活監視情報'},
  { name: 'serviceLocation', text: 'サービス地点情報'},
  { name: 'roadsideUnit', text: '路側機属性情報'},
  { name: 'useCase', text: 'ユースケース情報'},
  { name: 'signal', text: '信号情報'},
  { name: 'communicationMedia', text: '通信メディア情報'},
]

export const DIALOG_ERROR_INFO = {
  title: {
    getError: '取得エラー',
  },
  message: {
    getError:'情報が取得できませんでした',
    getErrorNoContent: '情報が存在しませんでした'
  },
}

// 死活監視情報
export const OPERATION_CLASSIFICATION_CODE: Record<number, string> = {
  0: '調整中',
  1: '運用中'
}

export const SERVICE_AVAILABILITY: Record<number, string> = {
  0: '● サービス提供可',
  1: '● 縮退動作中',
  2: '× サービス提供不可'
}

export const DEVICE_CLASSIFICATION: Record<number, string> = {
  0: 'センサ',
  1: '信号機',
  2: 'I2X通信機'
}

/**
 * インフラ機器情報
 * Key: インフラ機器ID
 * Value: IDが表現する機器種別名
 */
export const DEVICE_LIST: Record<string, string> = {
  '0x01': '機器01',
  '0x02': '機器02',
  '0x03': '機器03',
  '0x04': '機器04',
  '0x05': '機器05',
  '0x06': '機器06',
  '0x07': '機器07',
  '0x08': '機器08',
  '0x09': '機器09',
  '0x0a': '機器10',
  '0x0b': '機器11',
  '0x0c': '機器12',
  '0x0d': '機器13',
  '0x0e': '機器14',
  '0x0f': '機器15',
  '0x10': '機器16',
  '0x11': '機器17',
  '0x12': '機器18',
  '0x13': '機器19',
  '0x14': '機器20',
  '0x15': '機器21',
  '0x16': '機器22',
  '0x17': '機器23'
}

/**
 * 機器メーカー情報
 * Key: メーカーID
 * Value: IDが表現するメーカー名
 */
export const MANUFACTURER_LIST: Record<string, string> = {
  '0x01': 'メーカー01',
  '0x02': 'メーカー02',
  '0x03': 'メーカー03',
  '0x04': 'メーカー04',
  '0x05': 'メーカー05',
  '0x06': 'メーカー06',
  '0x07': 'メーカー07',
  '0x08': 'メーカー08',
  '0x09': 'メーカー09',
  '0x0a': 'メーカー10',
  '0x0b': 'メーカー11',
  '0x0c': 'メーカー12',
  '0x0d': 'メーカー13',
  '0x0e': 'メーカー14',
  '0x0f': 'メーカー15'
}

export const DEVICE_OPERATION_STATUS: Record<number, string> = {
  0: '運用中',
  1: '試験中'
}

export const DEVICE_ALIVE_STATUS: Record<number, string> = {
  0: '● 正常稼働中',
  1: '● 縮退稼働中',
  2: '× 停止中'
}

//路側機属性情報
export const MATERIAL_TYPE: Record<number, string> = {
  0:  'コンクリート柱',
  1:  'ステンレス鋼柱',
  2:  '鋼管柱',
  15: '不定',
}

// ユースケース情報
export const USE_CASE_TYPE: Record<number, string> = {
  1:  '信号灯火認識支援',
  2:  '信号交差点進入判断支援',
  3:  '一時停止見落とし',
  5:  '踏切(先詰まり)通過支援',
  11: '左折支援',
  12: '右折支援',
  20: '(見通しが悪いカーブ等での)追突防止支援',
  21: '退避エリアへの進入支援',
  22: '出発時の後方車両追突防止支援',
  30: '優先出会い頭',
  35: '非優先出会い頭',
  36: '(優先関係不明確)出会い頭',
  41: '合流部での合流支援(他車合流)',
  42: '合流部での合流支援(自車合流)',
  53: '(自方路)横断者情報見落とし',
  61: '狭路対向車すれ違い支援',
  62: '対向車線はみだし追越支援',
}

export const USE_CASE_SUPPLEMENTARY: Record<number, string> = {
  1: '踏みとどまり支援',
  2: 'アプローチ支援'
}

export const TARGET_UTILIZATION_TYPE: Record<number, string> = {
  0: '縮退動作',
  1: '情報提供/注意喚起',
  2: 'ADAS/自動運転レベル2',
  4: '自動運転レベル4'
}

// 信号情報
export const PREFECTURE: Record<number, string> = {
  1:  '北海道',
  2:  '青森県',
  3:  '岩手県',
  4:  '宮城県',
  5:  '秋田県',
  6:  '山形県',
  7:  '福島県',
  8:  '茨城県',
  9:  '栃木県',
  10: '群馬県',
  11: '埼玉県',
  12: '千葉県',
  13: '東京都',
  14: '神奈川県',
  15: '新潟県',
  16: '富山県',
  17: '石川県',
  18: '福井県',
  19: '山梨県',
  20: '長野県',
  21: '岐阜県',
  22: '静岡県',
  23: '愛知県',
  24: '三重県',
  25: '滋賀県',
  26: '京都府',
  27: '大阪府',
  28: '兵庫県',
  29: '奈良県',
  30: '和歌山県',
  31: '鳥取県',
  32: '島根県',
  33: '岡山県',
  34: '広島県',
  35: '山口県',
  36: '徳島県',
  37: '香川県',
  38: '愛媛県',
  39: '高知県',
  40: '福岡県',
  41: '佐賀県',
  42: '長崎県',
  43: '熊本県',
  44: '大分県',
  45: '宮崎県',
  46: '鹿児島県',
  47: '沖縄県'
}
