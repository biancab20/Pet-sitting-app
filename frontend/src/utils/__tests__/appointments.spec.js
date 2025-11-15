import { describe, it, expect } from 'vitest'
import { toDateTime, isUpcoming } from '../appointments'

describe('appointments utils', () => {
  it('converts appointment to Date', () => {
    const appt = {
      date: '2025-01-11',
      start_time: '10:30:15',
    }

    const dt = toDateTime(appt)

    expect(dt.getFullYear()).toBe(2025)
    expect(dt.getMonth()).toBe(0) // January = 0
    expect(dt.getDate()).toBe(11)
    expect(dt.getHours()).toBe(10)
    expect(dt.getMinutes()).toBe(30)
    expect(dt.getSeconds()).toBe(15)
  })

  it('detects upcoming vs past', () => {
    const now = new Date('2025-01-10T12:00:00')

    const futureAppt = { date: '2025-01-11', start_time: '10:00:00' }
    const pastAppt = { date: '2025-01-09', start_time: '10:00:00' }

    expect(isUpcoming(futureAppt, now)).toBe(true)
    expect(isUpcoming(pastAppt, now)).toBe(false)
  })
})
