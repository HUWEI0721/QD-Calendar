import axios from './axios'

// 获取日程列表
export const getEvents = (params) => {
  return axios.get('/events', { params })
}

// 获取单个日程详情
export const getEvent = (id) => {
  return axios.get(`/events/${id}`)
}

// 创建日程
export const createEvent = (data) => {
  return axios.post('/events', data)
}

// 更新日程
export const updateEvent = (id, data) => {
  return axios.put(`/events/${id}`, data)
}

// 删除日程
export const deleteEvent = (id) => {
  return axios.delete(`/events/${id}`)
}

// 获取日历数据
export const getCalendar = (year, month) => {
  return axios.get('/calendar', { params: { year, month } })
}

// 上传图片
export const uploadImage = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return axios.post('/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 获取近期活动（首页轮播用）
export const getUpcomingEvents = () => {
  return axios.get('/events/upcoming')
}

