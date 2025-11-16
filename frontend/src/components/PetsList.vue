<script setup>
import { onMounted, computed } from 'vue'
import { usePetsStore } from '@/stores/pets'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const petsStore = usePetsStore()

const pets = computed(() => petsStore.pets)
const loading = computed(() => petsStore.loading)
const error = computed(() => petsStore.error)

const emit = defineEmits(['edit', 'appointment'])

function handleEdit(pet) {
  emit('edit', pet)
}

function handleMakeAppointment(pet) {
  emit('appointment', pet)
}

function handleDelete(pet) {
  $q.dialog({
    title: 'Delete pet',
    message: `Are you sure you want to delete ${pet.name}?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      await petsStore.deletePet(pet.id)
      $q.notify({ type: 'positive', message: 'Pet deleted' })
    } catch (err) {
      console.error(err)
      $q.notify({
        type: 'negative',
        message: petsStore.error || 'Failed to delete pet',
      })
    }
  })
}

function reload() {
  petsStore.fetchPets()
}

onMounted(() => {
  petsStore.fetchPets()
})
</script>

<template>
  <div class="column q-gutter-md">
    <!-- Top bar: title + reload -->
    <div class="row items-center">
      <div class="text-h6">Pets</div>
      <q-space />
      <q-btn flat icon="refresh" label="Reload" :loading="loading" @click="reload" />
    </div>

    <!-- Error banner -->
    <q-banner v-if="error" class="bg-red-2 text-red-10" rounded>
      {{ error }}
    </q-banner>

    <!-- Loading state -->
    <div v-if="loading" class="row justify-center q-my-lg">
      <q-spinner />
    </div>

    <!-- Empty state -->
    <div v-else-if="!pets.length" class="text-grey-7 q-mt-md">
      No pets yet. Use the “+” button in the header to add one.
    </div>

    <!-- Card grid -->
    <div v-else class="row q-col-gutter-lg q-mt-md">
      <div v-for="pet in pets" :key="pet.id" class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2">
        <q-card class="pet-card full-height q-pa-sm">
          <!-- Image section -->
          <q-img
            v-if="pet.image_url"
            :src="pet.image_url"
            :ratio="16 / 9"
            class="pet-card__image q-mb-sm"
            spinner-color="primary"
          >
          </q-img>

          <div v-else class="pet-card__placeholder q-mb-sm column items-center justify-center">
            <q-icon name="pets" size="32px" class="q-mb-xs" />
            <div class="text-caption">No image</div>
          </div>
          <!-- Header section -->
          <q-card-section class="row items-start justify-between">
            <div>
              <div class="text-h6">{{ pet.name }}</div>
              <div class="text-subtitle2 text-grey-7">{{ pet.breed }}</div>
            </div>

            <q-btn flat round dense icon="more_vert">
              <q-menu auto-close>
                <q-list style="min-width: 150px">
                  <q-item clickable @click="handleEdit(pet)">
                    <q-item-section avatar><q-icon name="edit" /></q-item-section>
                    <q-item-section>Edit</q-item-section>
                  </q-item>

                  <q-item clickable @click="handleMakeAppointment(pet)">
                    <q-item-section avatar><q-icon name="event" /></q-item-section>
                    <q-item-section>Make appointment</q-item-section>
                  </q-item>

                  <q-item clickable @click="handleDelete(pet)">
                    <q-item-section avatar>
                      <q-icon color="negative" name="delete" />
                    </q-item-section>
                    <q-item-section class="text-negative">Delete</q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </q-card-section>

          <!-- Body section -->
          <q-card-section>
            <div class="q-mb-sm">
              <q-chip
                size="sm"
                icon="category"
                outline
                color="primary"
                text-color="primary"
                v-if="pet.pet_type"
              >
                {{ pet.pet_type }}
              </q-chip>

              <q-chip size="sm" icon="pets" outline color="secondary" text-color="secondary">
                {{ pet.size }}
              </q-chip>

              <q-chip size="sm" icon="cake" outline color="primary" text-color="primary">
                {{ pet.birthdate }}
              </q-chip>
            </div>

            <div class="text-caption text-grey-6"><strong>ID:</strong> {{ pet.id }}</div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<style>
.pet-card {
  min-height: 200px;
  min-width: 260px;
  border-radius: 16px;

  /* Light mode card background */
  background: #f7f8ec;

  /* Subtle border */
  border: 1px solid rgba(167, 190, 174, 0.7);

  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.pet-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.16);
}

body.body--dark .pet-card {
  background: #3a3c35;
  border-color: #a7beae;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
}

.pet-card__image {
  border-radius: 12px;
  overflow: hidden;
}

.pet-card__placeholder {
  height: 140px;
  border-radius: 12px;
  background: rgba(184, 80, 66, 0.08); /* #B85042-ish */
  color: #b85042;
  border: 1px dashed rgba(184, 80, 66, 0.6);
}
</style>
