/**
 * 人员管理 API
 */
import request from './axios'

/**
 * 获取人员列表
 */
export function getMembers(params) {
  return request({
    url: '/members',
    method: 'get',
    params
  })
}

/**
 * 获取人员详情
 */
export function getMemberDetail(id) {
  return request({
    url: `/members/${id}`,
    method: 'get'
  })
}

/**
 * 创建人员
 */
export function createMember(data) {
  return request({
    url: '/members',
    method: 'post',
    data
  })
}

/**
 * 更新人员
 */
export function updateMember(id, data) {
  return request({
    url: `/members/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除人员
 */
export function deleteMember(id) {
  return request({
    url: `/members/${id}`,
    method: 'delete'
  })
}

/**
 * 获取人员统计
 */
export function getMemberStats() {
  return request({
    url: '/members/stats',
    method: 'get'
  })
}




