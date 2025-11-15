<script setup>
import { RouterView } from 'vue-router'
import { Dark, useQuasar } from 'quasar'
import { ref } from 'vue'

const $q = useQuasar()

const showCreatePetDialog = ref(false)

function toggleDarkMode() {
  Dark.toggle()
}

function openCreatePetDialog() {
  showCreatePetDialog.value = true
}
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <!-- HEADER / TOP BAR -->
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>
          Pet Sitting App
        </q-toolbar-title>

        <q-space />

        <!-- "+" button to open pet form dialog -->
        <q-btn
          flat
          round
          dense
          icon="add"
          aria-label="Add pet"
          @click="openCreatePetDialog"
        />

        <!-- Dark / light toggle -->
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

    <!-- MAIN CONTENT -->
   <q-page-container class="app-page-container">
  <RouterView />
</q-page-container>

    <!-- DIALOG FOR CREATING A PET (placeholder for now) -->
    <q-dialog v-model="showCreatePetDialog">
      <q-card class="q-pa-md" style="min-width: 360px">
        <div class="text-h6 q-mb-sm">
          Add a new pet
        </div>

        <div class="text-body2 text-grey-7 q-mb-md">
          Here we will place the pet form component in the next step.
        </div>

        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<style>
html,
body,
#app {
  height: 100%;
  margin: 0;
}
</style>
