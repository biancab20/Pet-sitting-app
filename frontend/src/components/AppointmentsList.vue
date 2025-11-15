<script setup>
import { onMounted, computed } from 'vue'
import { useAppointmentsStore } from '@/stores/appointments'
import { usePetsStore } from '@/stores/pets'
import { useQuasar } from 'quasar'

const appointmentsStore = useAppointmentsStore()
const petsStore = usePetsStore()
const $q = useQuasar()

const appointments = computed(() => appointmentsStore.appointments)
const loading = computed(() => appointmentsStore.loading)
const error = computed(() => appointmentsStore.error)

const emit = defineEmits(['schedule'])

onMounted(() => {
  appointmentsStore.fetchAppointments()
})

function petNameFor(appointment) {
  const pet = petsStore.pets.find((p) => p.id === appointment.pet_id)
  return pet ? pet.name : `Pet #${appointment.pet_id}`
}

async function handleDelete(appt) {
  $q.dialog({
    title: 'Delete appointment',
    message: `Delete appointment for ${petNameFor(appt)} on ${appt.date}?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      await appointmentsStore.deleteAppointment(appt.id)
      $q.notify({ type: 'positive', message: 'Appointment deleted' })
    } catch (err) {
      console.error(err)
      $q.notify({
        type: 'negative',
        message: appointmentsStore.error || 'Failed to delete appointment',
      })
    }
  })
}

function handleScheduleClick() {
  emit('schedule')
}

function toDateTime(appt) {
  // appt.date: "YYYY-MM-DD"
  // appt.start_time: "HH:MM:SS" or "HH:MM"
  const [y, m, d] = appt.date.split('-').map(Number)
  const timeParts = appt.start_time ? appt.start_time.split(':').map(Number) : [0, 0, 0]
  const [hh = 0, mm = 0, ss = 0] = timeParts
  return new Date(y, m - 1, d, hh, mm, ss)
}

function isUpcoming(appt, now) {
  return toDateTime(appt) >= now
}

const upcomingAppointments = computed(() => {
  const now = new Date()
  return [...appointments.value]
    .filter((a) => isUpcoming(a, now))
    .sort((a, b) => toDateTime(a) - toDateTime(b))
})

const pastAppointments = computed(() => {
  const now = new Date()
  return [...appointments.value]
    .filter((a) => !isUpcoming(a, now))
    .sort((a, b) => toDateTime(b) - toDateTime(a)) // newest past first
})
</script>

<template>
  <div class="q-mt-xl">
    <div class="row items-center q-mb-sm">
      <div class="text-h6">Appointments</div>
      <q-space />
      <q-btn flat icon="event" label="Schedule appointment" @click="handleScheduleClick" />
    </div>

    <q-banner v-if="error" class="bg-red-2 text-red-10 q-mb-md" rounded>
      {{ error }}
    </q-banner>

    <div v-if="loading" class="row justify-center q-my-lg">
      <q-spinner />
    </div>

    <div v-else-if="!appointments.length" class="text-grey-7 q-mt-md">
      <q-card class="appointments-card empty-state-card q-pa-md">
        <div class="text-subtitle1 q-mb-xs">No appointments yet</div>
        <div class="text-body2 q-mb-sm">
          You haven't scheduled any sittings. Plan the first one now.
        </div>
        <q-btn
          color="primary"
          icon="event"
          label="Schedule appointment"
          @click="handleScheduleClick"
        />
      </q-card>
    </div>

    <div v-else>
      <!-- Upcoming -->
      <q-card v-if="upcomingAppointments.length" class="appointments-card q-pa-md q-mt-sm">
        <div class="text-subtitle1 q-mb-sm">Upcoming appointments</div>
        <q-list separator>
          <q-item v-for="appt in upcomingAppointments" :key="appt.id">
            <q-item-section>
              <q-item-label class="text-body1">
                <strong>{{ petNameFor(appt) }}</strong>
                <span class="text-caption text-grey-7">
                  &nbsp;• {{ appt.date }} at {{ appt.start_time }}
                </span>
              </q-item-label>
              <q-item-label caption>
                Sitter: {{ appt.sitter_name }} — {{ appt.duration_minutes }} min
              </q-item-label>
            </q-item-section>

            <q-item-section side top>
              <q-btn dense round flat icon="delete" color="negative" @click="handleDelete(appt)" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card>

      <!-- Past -->
      <q-card v-if="pastAppointments.length" class="appointments-card q-pa-md q-mt-md">
        <div class="text-subtitle1 q-mb-sm">Past appointments</div>
        <q-list separator>
          <q-item v-for="appt in pastAppointments" :key="appt.id">
            <q-item-section>
              <q-item-label class="text-body1">
                <strong>{{ petNameFor(appt) }}</strong>
                <span class="text-caption text-grey-7">
                  &nbsp;• {{ appt.date }} at {{ appt.start_time }}
                </span>
              </q-item-label>
              <q-item-label caption>
                Sitter: {{ appt.sitter_name }} — {{ appt.duration_minutes }} min
              </q-item-label>
            </q-item-section>

            <q-item-section side top>
              <q-btn dense round flat icon="delete" color="negative" @click="handleDelete(appt)" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card>
    </div>
  </div>
</template>

<style>
.appointments-card {
  border-radius: 16px;
  background: #f7f8ec;
  border: 1px solid rgba(167, 190, 174, 0.8); /* #A7BEAE-ish */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Stronger styling for the empty state */
.empty-state-card {
  border-style: dashed;
  border-color: #b85042;
}

/* Dark mode */
body.body--dark .appointments-card {
  background: #3a3c35;
  border-color: #a7beae;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
}
</style>
