import { defineStore } from 'pinia'
import { api } from '@/plugins/axios'

export const usePetsStore = defineStore('pets', {
  state: () => ({
    pets: [],
    loading: false,
    error: null,      // general errors (list, delete)
    formError: null,  // errors from create/update
  }),

  getters: {
    // Example: number of pets
    petsCount: (state) => state.pets.length,
  },

  actions: {
    async fetchPets() {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.get('/pets')
        this.pets = data
      } catch (err) {
        this.error = this._extractError(err)
      } finally {
        this.loading = false
      }
    },

    async createPet(payload) {
      this.formError = null
      try {
        const { data } = await api.post('/pets', payload)
        // update list without reloading page
        this.pets.push(data)
        return data
      } catch (err) {
        this.formError = this._extractError(err)
        throw err
      }
    },

    async updatePet(id, payload) {
      this.formError = null
      try {
        const { data } = await api.put(`/pets/${id}`, payload)
        const index = this.pets.findIndex(p => p.id === id)
        if (index !== -1) {
          // replace updated pet in local state
          this.pets[index] = data
        }
        return data
      } catch (err) {
        this.formError = this._extractError(err)
        throw err
      }
    },

    async deletePet(id) {
      this.error = null
      try {
        await api.delete(`/pets/${id}`)
        this.pets = this.pets.filter(p => p.id !== id)
      } catch (err) {
        this.error = this._extractError(err)
        throw err
      }
    },

    _extractError(err) {
      // Backend might return {"detail": "..."} or validation error list
      const detail = err?.response?.data?.detail

      if (!detail) return 'Something went wrong'

      if (Array.isArray(detail)) {
        // FastAPI validation errors array
        return detail
          .map(item => item.msg || JSON.stringify(item))
          .join(', ')
      }

      if (typeof detail === 'string') {
        return detail
      }

      return JSON.stringify(detail)
    }
  }
})
