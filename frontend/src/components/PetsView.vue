<script setup>
import PetsList from '@/components/PetsList.vue'
import { ref } from 'vue'

// we'll plug this into the header "+" dialog later
const selectedPet = ref(null)

function handleEdit(pet) {
  selectedPet.value = pet
  // Later: emit to App or use a store/event to open the edit form dialog
  // For now this just proves wiring works.
  console.log('Edit pet clicked:', pet)
}
</script>

<template>
  <q-page class="q-pa-md">
    <PetsList @edit="handleEdit" />
  </q-page>
</template>
