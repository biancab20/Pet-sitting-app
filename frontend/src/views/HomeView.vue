<script setup>
import { ref } from 'vue'
import PetsList from '@/components/PetsList.vue'
import PetForm from '@/components/PetForm.vue'
import AppointmentForm from '@/components/AppointmentForm.vue'
import AppointmentsList from '@/components/AppointmentsList.vue'
import HeroInvite from '@/components/HeroInvite.vue'

const selectedPet = ref(null)
const showEditPetDialog = ref(false)

const selectedPetForAppointment = ref(null)
const showAppointmentDialog = ref(false)

function handleEdit(pet) {
  selectedPet.value = { ...pet }
  showEditPetDialog.value = true
}

function handleEditSuccess() {
  showEditPetDialog.value = false
  selectedPet.value = null
}

function handleEditCancel() {
  showEditPetDialog.value = false
  selectedPet.value = null
}

function handleAppointment(pet) {
  selectedPetForAppointment.value = { ...pet }
  showAppointmentDialog.value = true
}

function handleGenericSchedule() {
  selectedPetForAppointment.value = null
  showAppointmentDialog.value = true
}

function handleAppointmentSuccess() {
  showAppointmentDialog.value = false
  selectedPetForAppointment.value = null
}

function handleAppointmentCancel() {
  showAppointmentDialog.value = false
  selectedPetForAppointment.value = null
}

function handleBrowsePets() {
  const el = document.getElementById('pets-section')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>

<template>
  <q-page class="q-pa-lg full-width">

    <HeroInvite @browse="handleBrowsePets" />
    
    <PetsList @edit="handleEdit" @appointment="handleAppointment" />

    <!-- Edit Pet Dialog -->
    <q-dialog v-model="showEditPetDialog">
      <q-card class="q-pa-md" style="min-width: 380px; max-width: 480px">
        <PetForm
          v-if="selectedPet"
          mode="edit"
          :pet="selectedPet"
          @success="handleEditSuccess"
          @cancel="handleEditCancel"
        />
      </q-card>
    </q-dialog>

    <!-- Appointments section -->
    <AppointmentsList @schedule="handleGenericSchedule" />

    <!-- Appointment Dialog -->
    <q-dialog v-model="showAppointmentDialog">
      <q-card class="q-pa-md" style="min-width: 380px; max-width: 480px">
        <AppointmentForm
          :pet="selectedPetForAppointment"
          @success="handleAppointmentSuccess"
          @cancel="handleAppointmentCancel"
        />
      </q-card>
    </q-dialog>
  </q-page>
</template>
