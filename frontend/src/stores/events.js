import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getEvents, getEvent, createEvent, updateEvent, deleteEvent, getCalendar } from '@/api/events'

export const useEventsStore = defineStore('events', () => {
  const events = ref([])
  const currentEvent = ref(null)
  const calendarData = ref({})
  const loading = ref(false)
  
  // 获取日程列表
  async function fetchEvents(params = {}) {
    loading.value = true
    try {
      const response = await getEvents(params)
      events.value = response.events
      return { success: true, events: response.events }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '获取日程失败' }
    } finally {
      loading.value = false
    }
  }
  
  // 获取单个日程详情
  async function fetchEvent(id) {
    loading.value = true
    try {
      const response = await getEvent(id)
      currentEvent.value = response
      return { success: true, event: response }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '获取日程详情失败' }
    } finally {
      loading.value = false
    }
  }
  
  // 创建日程
  async function addEvent(eventData) {
    loading.value = true
    try {
      const response = await createEvent(eventData)
      events.value.unshift(response.event)
      return { success: true, event: response.event }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '创建日程失败' }
    } finally {
      loading.value = false
    }
  }
  
  // 更新日程
  async function modifyEvent(id, eventData) {
    loading.value = true
    try {
      const response = await updateEvent(id, eventData)
      const index = events.value.findIndex(e => e.id === id)
      if (index !== -1) {
        events.value[index] = response.event
      }
      return { success: true, event: response.event }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '更新日程失败' }
    } finally {
      loading.value = false
    }
  }
  
  // 删除日程
  async function removeEvent(id) {
    loading.value = true
    try {
      await deleteEvent(id)
      events.value = events.value.filter(e => e.id !== id)
      return { success: true }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '删除日程失败' }
    } finally {
      loading.value = false
    }
  }
  
  // 获取日历数据
  async function fetchCalendar(year, month) {
    loading.value = true
    try {
      const response = await getCalendar(year, month)
      calendarData.value = response.calendar
      return { success: true, calendar: response.calendar }
    } catch (error) {
      return { success: false, message: error.response?.data?.message || '获取日历数据失败' }
    } finally {
      loading.value = false
    }
  }
  
  return {
    events,
    currentEvent,
    calendarData,
    loading,
    fetchEvents,
    fetchEvent,
    addEvent,
    modifyEvent,
    removeEvent,
    fetchCalendar
  }
})

