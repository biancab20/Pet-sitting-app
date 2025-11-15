<script setup>
import { ref, watch, computed } from 'vue'
import { useAppointmentsStore } from '@/stores/appointments'
import { usePetsStore } from '@/stores/pets'
import { useQuasar } from 'quasar'

const props = defineProps({
  pet: {
    type: Object,
    default: null, // if provided, pet is pre-selected and not changeable
  },
})

const emit = defineEmits(['success', 'cancel'])

const $q = useQuasar()
const appointmentsStore = useAppointmentsStore()
const petsStore = usePetsStore()

const sitterName = ref('')
const date = ref('')
const startTime = ref('')
const durationMinutes = ref(60)
const selectedPetId = ref(null)

const submitLoading = ref(false)
const formError = computed(() => appointmentsStore.formError)

// Today formats
const todayIso = new Date().toISOString().slice(0, 10) // "YYYY-MM-DD"
const todaySlash = todayIso.replace(/-/g, '/') // "YYYY/MM/DD"

const isSelectedDateToday = computed(() => date.value === todayIso)

// Pet options for QSelect (user sees name, we send id)
const petOptions = computed(() =>
  petsStore.pets.map((p) => ({
    label: p.name,
    value: p.id,
  })),
)

// disable past dates in date picker
function dateOptions(d) {
  // d is "YYYY/MM/DD"
  return d >= todaySlash
}

// block past dates on manual input
function isPast(dateStr) {
  if (!dateStr) return false
  // dateStr is "YYYY-MM-DD"
  return dateStr < todayIso
}

// --- Time options for q-time ---
function getCurrentTimeHHMM() {
  const now = new Date()
  return now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false })
}

// q-time -> time is "HH:mm"
function timeOptions(time) {
  if (!isSelectedDateToday.value) {
    return true // any time acceptable for future date
  }
  const nowHHMM = getCurrentTimeHHMM()
  return time >= nowHHMM
}

// Initialize selectedPetId when prop.pet changes
watch(
  () => props.pet,
  (pet) => {
    if (pet) {
      selectedPetId.value = pet.id
    } else {
      selectedPetId.value = null
    }
  },
  { immediate: true },
)

async function handleSubmit() {
  appointmentsStore.formError = null
  submitLoading.value = true

  const payload = {
    pet_id: selectedPetId.value,
    sitter_name: sitterName.value,
    date: date.value, // "YYYY-MM-DD"
    // 👇 transform "HH:MM" into "HH:MM:00"
    start_time: startTime.value ? `${startTime.value}:00` : null,
    duration_minutes: durationMinutes.value,
  }

  try {
    await appointmentsStore.createAppointment(payload)
    $q.notify({ type: 'positive', message: 'Appointment created' })
    emit('success')
  } catch (err) {
    console.error(err)
  } finally {
    submitLoading.value = false
  }
}

function handleCancel() {
  emit('cancel')
}

function setDurationPreset(min) {
  durationMinutes.value = min
}
</script>

<template>
  <q-form @submit.prevent="handleSubmit" class="q-gutter-md">
    <div class="text-h6 q-mb-sm">Schedule appointment</div>

    <q-banner v-if="formError" class="bg-red-2 text-red-10" rounded>
      {{ formError }}
    </q-banner>

    <!-- Pet selector -->
    <q-select
      v-if="!pet"
      v-model="selectedPetId"
      :options="petOptions"
      label="Pet"
      filled
      :rules="[(val) => !!val || 'Please select a pet']"
    />

    <q-input v-else :model-value="pet.name" label="Pet" filled disable />

    <q-input
      v-model="sitterName"
      label="Pet sitter's name"
      filled
      :rules="[(val) => !!val || 'Sitter name is required']"
    />

    <!-- DATE picker -->
    <q-input
      v-model="date"
      label="Date"
      filled
      mask="####-##-##"
      hint="YYYY-MM-DD"
      :rules="[
        (val) => !!val || 'Date is required',
        (val) => !isPast(val) || 'Date cannot be in the past',
      ]"
    >
      <template #prepend>
        <q-icon name="event" class="cursor-pointer">
          <q-popup-proxy cover transition-show="scale" transition-hide="scale">
            <q-date v-model="date" mask="YYYY-MM-DD" :options="dateOptions" />
          </q-popup-proxy>
        </q-icon>
      </template>
    </q-input>

    <!-- TIME picker -->
    <q-input
      v-model="startTime"
      label="Start time"
      filled
      mask="##:##"
      hint="HH:MM"
      :rules="[(val) => !!val || 'Start time is required']"
    >
      <template #prepend>
        <q-icon name="schedule" class="cursor-pointer">
          <q-popup-proxy cover transition-show="scale" transition-hide="scale">
            <q-time v-model="startTime" format24h :options="timeOptions" />
          </q-popup-proxy>
        </q-icon>
      </template>
    </q-input>

    <q-input
      v-model.number="durationMinutes"
      type="number"
      label="Duration (minutes)"
      filled
      :rules="[
        (val) => !!val || 'Duration is required',
        (val) => val > 0 || 'Duration must be greater than 0',
      ]"
    >
      <template #after>
        <div class="column q-gutter-xs">
          <q-btn
            dense
            outline
            label="15"
            @click="setDurationPreset(15)"
            :color="durationMinutes === 15 ? 'primary' : 'secondary'"
          />
          <q-btn
            dense
            outline
            label="30"
            @click="setDurationPreset(30)"
            :color="durationMinutes === 30 ? 'primary' : 'secondary'"
          />
          <q-btn
            dense
            outline
            label="60"
            @click="setDurationPreset(60)"
            :color="durationMinutes === 60 ? 'primary' : 'secondary'"
          />
        </div>
      </template>
    </q-input>

    <div class="row justify-end q-gutter-sm q-mt-sm">
      <q-btn flat label="Cancel" color="primary" type="button" @click="handleCancel" />
      <q-btn label="Schedule" color="primary" type="submit" :loading="submitLoading" />
    </div>
  </q-form>
</template>
