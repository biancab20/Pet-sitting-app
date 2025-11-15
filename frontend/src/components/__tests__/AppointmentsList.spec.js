import { describe, it, expect, vi, beforeEach, beforeAll, afterAll } from 'vitest'
import { mount } from '@vue/test-utils'
import { defineComponent, h } from 'vue'

// ---- Mock Quasar (composables + components) ----
vi.mock('quasar', () => {
  const stub = (name) =>
    defineComponent({
      name,
      setup(_, { slots }) {
        return () => h('div', {}, slots.default ? slots.default() : [])
      },
    })

  return {
    useQuasar: () => ({
      dialog: vi.fn(() => ({
        onOk: (cb) => ({ onOk: cb }),
      })),
      notify: vi.fn(),
    }),

    QSpace: stub('QSpace'),
    QBtn: stub('QBtn'),
    QCard: stub('QCard'),
    QCardSection: stub('QCardSection'),
    QBanner: stub('QBanner'),
    QSpinner: stub('QSpinner'),
    QList: stub('QList'),
    QItem: stub('QItem'),
    QItemSection: stub('QItemSection'),
    QItemLabel: stub('QItemLabel'),
    QIcon: stub('QIcon'),
  }
})


// ---- Mock appointments store ----
const apptState = {
  appointments: [],
  loading: false,
  error: null,
}

const mockFetchAppointments = vi.fn()
const mockDeleteAppointment = vi.fn()

vi.mock('@/stores/appointments', () => ({
  useAppointmentsStore: () => ({
    appointments: apptState.appointments,
    loading: apptState.loading,
    error: apptState.error,
    fetchAppointments: mockFetchAppointments,
    deleteAppointment: mockDeleteAppointment,
  }),
}))

// ---- Mock pets store (for pet names) ----
const petsState = {
  pets: [],
}

vi.mock('@/stores/pets', () => ({
  usePetsStore: () => ({
    pets: petsState.pets,
  }),
}))

// ---- Import component AFTER mocks ----
import AppointmentsList from '../AppointmentsList.vue'

describe('AppointmentsList', () => {
  beforeAll(() => {
    // Fix "now" so upcoming/past classification is stable
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2025-01-10T12:00:00')) // 10 Jan 2025, 12:00
  })

  afterAll(() => {
    vi.useRealTimers()
  })

  beforeEach(() => {
    apptState.appointments = []
    apptState.loading = false
    apptState.error = null
    petsState.pets = []
    mockFetchAppointments.mockClear()
    mockDeleteAppointment.mockClear()
  })

  it('calls fetchAppointments on mount', () => {
    mount(AppointmentsList)

    expect(mockFetchAppointments).toHaveBeenCalled()
  })

  it('shows empty state when there are no appointments', () => {
    apptState.appointments = []

    const wrapper = mount(AppointmentsList)

    expect(wrapper.text()).toContain('No appointments yet')
  })

  it('splits appointments into upcoming and past', () => {
    // Pets for naming
    petsState.pets = [
      { id: 1, name: 'Bella' },
      { id: 2, name: 'Milo' },
    ]

    // Now = 2025-01-10 12:00 (from beforeAll)
    apptState.appointments = [
      {
        id: 1,
        pet_id: 1,
        sitter_name: 'Future Sitter',
        date: '2025-01-11',
        start_time: '10:00:00',
        duration_minutes: 60,
      },
      {
        id: 2,
        pet_id: 2,
        sitter_name: 'Past Sitter',
        date: '2025-01-09',
        start_time: '15:00:00',
        duration_minutes: 30,
      },
    ]

    const wrapper = mount(AppointmentsList)

    const text = wrapper.text()

    // Section titles
    expect(text).toContain('Upcoming appointments')
    expect(text).toContain('Past appointments')

    // Check assignment by sitter name or pet name
    const cards = wrapper.findAllComponents({ name: 'QCard' })

    // 1st card: Upcoming
    const upcomingText = cards[0].text()
    expect(upcomingText).toContain('Bella')
    expect(upcomingText).toContain('Future Sitter')

    // 2nd card: Past
    const pastText = cards[1].text()
    expect(pastText).toContain('Milo')
    expect(pastText).toContain('Past Sitter')
  })
})
