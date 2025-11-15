<script setup>
import { RouterView } from 'vue-router'
import { Dark, useQuasar } from 'quasar'
import { ref } from 'vue'
import PetForm from '@/components/PetForm.vue'

const $q = useQuasar()

const showCreatePetDialog = ref(false)

function toggleDarkMode() {
  Dark.toggle()
}

function openCreatePetDialog() {
  showCreatePetDialog.value = true
}

function handleFormSuccess() {
  showCreatePetDialog.value = false
}

function handleFormCancel() {
  showCreatePetDialog.value = false
}
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title> Pet Sitting App </q-toolbar-title>

        <q-space />

        <q-btn flat round dense icon="add" aria-label="Add pet" @click="openCreatePetDialog" />

        <q-btn
          flat
          round
          dense
          :icon="$q.dark.isActive ? 'light_mode' : 'dark_mode'"
          aria-label="Toggle dark mode"
          @click="toggleDarkMode"
        />
      </q-toolbar>
    </q-header>

    <q-page-container class="app-page-container">
      <RouterView />
    </q-page-container>

    <q-dialog v-model="showCreatePetDialog">
      <q-card class="q-pa-md" style="min-width: 380px; max-width: 480px">
        <PetForm mode="create" @success="handleFormSuccess" @cancel="handleFormCancel" />
      </q-card>
    </q-dialog>
  </q-layout>
</template>


