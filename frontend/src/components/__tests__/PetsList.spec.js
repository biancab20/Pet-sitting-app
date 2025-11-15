import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { defineComponent, h } from 'vue'   // 👈 add h here

// ---- Mock Quasar (composables + components) ----
vi.mock('quasar', () => {
  const stub = (name) =>
    defineComponent({
      name,
      setup(_, { slots }) {
        // 👇 render the default slot content so inner text is visible
        return () => h('div', {}, slots.default ? slots.default() : [])
      },
    })

  return {
    // composables
    useQuasar: () => ({
      dialog: vi.fn(() => ({
        onOk: (cb) => ({ onOk: cb }), // simple chainable mock
      })),
      notify: vi.fn(),
    }),

    // components used in PetsList.vue
    QSpace: stub('QSpace'),
    QBtn: stub('QBtn'),
    QCard: stub('QCard'),
    QCardSection: stub('QCardSection'),
    QBanner: stub('QBanner'),
    QSpinner: stub('QSpinner'),
    QChip: stub('QChip'),
    QIcon: stub('QIcon'),
    QMenu: stub('QMenu'),
    QList: stub('QList'),
    QItem: stub('QItem'),
    QItemSection: stub('QItemSection'),
  }
})


// ---- Mock pets store ----
const state = {
  pets: [],
  loading: false,
  error: null,
}

const mockFetchPets = vi.fn()
const mockDeletePet = vi.fn()

vi.mock('@/stores/pets', () => ({
  usePetsStore: () => ({
    pets: state.pets,
    loading: state.loading,
    error: state.error,
    fetchPets: mockFetchPets,
    deletePet: mockDeletePet,
  }),
}))

// ---- Import component AFTER mocks ----
import PetsList from '../PetsList.vue'

describe('PetsList', () => {
  beforeEach(() => {
    state.pets = []
    state.loading = false
    state.error = null
    mockFetchPets.mockClear()
    mockDeletePet.mockClear()
  })

  it('calls fetchPets on mount', () => {
    mount(PetsList)

    expect(mockFetchPets).toHaveBeenCalled()
  })

  it('shows empty state message when there are no pets', () => {
    state.pets = []

    const wrapper = mount(PetsList)

    expect(wrapper.text()).toContain('No pets yet')
  })

  it('renders a card for each pet', () => {
    state.pets = [
      { id: 1, name: 'Bella', breed: 'Labrador', size: 'large', birthdate: '2018-06-12' },
      { id: 2, name: 'Milo', breed: 'Beagle', size: 'medium', birthdate: '2020-02-08' },
    ]

    const wrapper = mount(PetsList)

    expect(wrapper.text()).toContain('Bella')
    expect(wrapper.text()).toContain('Milo')
  })
})
