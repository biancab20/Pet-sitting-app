import { defineStore } from 'pinia'
import { api } from '@/plugins/axios'

export const useAppointmentsStore = defineStore('appointments', {
  state: () => ({
    appointments: [],
    loading: false,
    error: null,
    formError: null,
  }),

  actions: {
    async fetchAppointments() {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.get('/appointments')
        this.appointments = data
      } catch (err) {
        this.error = this._extractError(err)
      } finally {
        this.loading = false
      }
    },

    async createAppointment(payload) {
      this.formError = null
      try {
        const { data } = await api.post('/appointments', payload)
        this.appointments.push(data)
        return data
      } catch (err) {
        this.formError = this._extractError(err)
        throw err
      }
    },

    async deleteAppointment(id) {
      this.error = null
      try {
        await api.delete(`/appointments/${id}`)
        this.appointments = this.appointments.filter((a) => a.id !== id)
      } catch (err) {
        this.error = this._extractError(err)
        throw err
      }
    },

    _extractError(err) {
      const detail = err?.response?.data?.detail
      if (!detail) return 'Something went wrong'
      if (Array.isArray(detail)) {
        return detail.map((d) => d.msg || JSON.stringify(d)).join(', ')
      }
      if (typeof detail === 'string') return detail
      return JSON.stringify(detail)
    },
  },
})
