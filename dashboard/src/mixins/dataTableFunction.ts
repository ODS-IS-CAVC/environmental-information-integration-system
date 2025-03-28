/**
 * 日付ソート
 * @param datetimeA - 日時A
 * @param datetimeB - 日時B
 * @return 日時Aと日時Bの差
 */
export const sortByDate = (datetimeA: string, datetimeB: string): number => {
    return new Date(datetimeA).getTime() - new Date(datetimeB).getTime()
}