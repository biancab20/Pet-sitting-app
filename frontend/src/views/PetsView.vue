<script setup>
import { ref } from 'vue'
import PetsList from '@/components/PetsList.vue'
import PetForm from '@/components/PetForm.vue'

const selectedPet = ref(null)
const showEditPetDialog = ref(false)

function handleEdit(pet) {
  // Make a shallow copy so we don't mutate the store object directly
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
</script>

<template>
  <q-page class="q-pa-lg full-width">
    <PetsList @edit="handleEdit" />

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
  </q-page>
</template>
