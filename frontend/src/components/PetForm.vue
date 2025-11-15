<script setup>
import { ref, watch, computed } from 'vue'
import { usePetsStore } from '@/stores/pets'
import { useQuasar } from 'quasar'

const props = defineProps({
  mode: {
    type: String,
    default: 'create', // 'create' | 'edit'
  },
  pet: {
    type: Object,
    default: null, // used later for edit
  },
})

const emit = defineEmits(['success', 'cancel'])

const $q = useQuasar()
const petsStore = usePetsStore()

// Form state
const name = ref('')
const breed = ref('')
const size = ref(null)
const birthdate = ref('')

// Loading & error
const submitLoading = ref(false)
const formError = computed(() => petsStore.formError)

// Pre-fill when editing (we'll use this later)
watch(
  () => props.pet,
  (pet) => {
    if (pet && props.mode === 'edit') {
      name.value = pet.name
      breed.value = pet.breed
      size.value = pet.size
      birthdate.value = pet.birthdate
    } else if (props.mode === 'create') {
      resetForm()
    }
  },
  { immediate: true },
)

function resetForm() {
  name.value = ''
  breed.value = ''
  size.value = null
  birthdate.value = ''
}

async function handleSubmit() {
  submitLoading.value = true
  petsStore.formError = null

  const payload = {
    name: name.value,
    breed: breed.value,
    size: size.value,
    birthdate: birthdate.value,
  }

  try {
    if (props.mode === 'edit' && props.pet) {
      await petsStore.updatePet(props.pet.id, payload)
      $q.notify({ type: 'positive', message: 'Pet updated' })
    } else {
      await petsStore.createPet(payload)
      $q.notify({ type: 'positive', message: 'Pet created' })
      resetForm()
    }

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

function isFuture(dateStr) {
  const today = new Date().toISOString().slice(0, 10) // YYYY-MM-DD
  return dateStr > today
}

const today = new Date().toISOString().slice(0, 10)
</script>

<template>
  <q-form @submit.prevent="handleSubmit" class="q-gutter-md">
    <div class="text-h6 q-mb-sm">
      {{ mode === 'edit' ? 'Edit pet' : 'Add a new pet' }}
    </div>

    <q-banner v-if="formError" class="bg-red-2 text-red-10" rounded>
      {{ formError }}
    </q-banner>

    <q-input v-model="name" label="Name" filled :rules="[(val) => !!val || 'Name is required']" />

    <q-input
      v-model="breed"
      label="Breed"
      filled
      :rules="[(val) => !!val || 'Breed is required']"
    />

    <q-select
      v-model="size"
      :options="['small', 'medium', 'large']"
      label="Size"
      filled
      :rules="[(val) => !!val || 'Size is required']"
    />

    <q-input
      v-model="birthdate"
      label="Birthdate"
      filled
      mask="####-##-##"
      :options="date => date <= today"
      hint="YYYY-MM-DD"
      :rules="[
        (val) => !!val || 'Birthdate is required',
        (val) => !isFuture(val) || 'Birthdate cannot be in the future',
      ]"
    >
      <template #prepend>
        <q-icon name="event" class="cursor-pointer">
          <q-popup-proxy cover transition-show="scale" transition-hide="scale">
            <q-date v-model="birthdate" mask="YYYY-MM-DD" />
          </q-popup-proxy>
        </q-icon>
      </template>
    </q-input>

    <div class="row justify-end q-gutter-sm q-mt-sm">
      <q-btn flat label="Cancel" color="primary" type="button" @click="handleCancel" />
      <q-btn
        :label="mode === 'edit' ? 'Save changes' : 'Create pet'"
        color="primary"
        type="submit"
        :loading="submitLoading"
      />
    </div>
  </q-form>
</template>
