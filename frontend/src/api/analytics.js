/**
 * 数据分析 API
 */
import request from './axios'

/**
 * 获取数据分析总览
 */
export function getAnalyticsOverview(params) {
  return request({
    url: '/analytics/overview',
    method: 'get',
    params
  })
}

/**
 * 获取活动详细分析
 */
export function getAnalyticsEvents(params) {
  return request({
    url: '/analytics/events',
    method: 'get',
    params
  })
}

/**
 * 获取人员参与分析
 */
export function getAnalyticsMembers(params) {
  return request({
    url: '/analytics/members',
    method: 'get',
    params
  })
}




