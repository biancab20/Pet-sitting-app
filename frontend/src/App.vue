<template>
  <div class="q-pa-md">
    <q-card class="q-pa-md">
      <div class="text-h5 q-mb-md">Backend health check</div>

      <q-btn
        label="Check API"
        color="primary"
        @click="checkHealth"
        :loading="loading"
      />

      <div class="q-mt-md">
        <q-banner
          v-if="error"
          class="bg-red-2 text-red-10"
          rounded
        >
          {{ error }}
        </q-banner>

        <q-banner
          v-else-if="status"
          class="bg-green-2 text-green-10"
          rounded
        >
          API status: {{ status }}
        </q-banner>

        <div v-else class="text-grey-7">
          Click the button to test the backend connection.
        </div>
      </div>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from './plugins/axios'


const loading = ref(false)
const status = ref(null)
const error = ref(null)

const checkHealth = async () => {
  loading.value = true
  status.value = null
  error.value = null

  try {
    const { data } = await api.get('/health')
    status.value = data.status
  } catch (e) {
    error.value = 'Could not reach backend'
  } finally {
    loading.value = false
  }
}
</script>
