// src/utils/appointments.js
export function toDateTime(appt) {
  const [y, m, d] = appt.date.split('-').map(Number)
  const parts = appt.start_time ? appt.start_time.split(':').map(Number) : [0, 0, 0]
  const [hh = 0, mm = 0, ss = 0] = parts
  return new Date(y, m - 1, d, hh, mm, ss)
}

export function isUpcoming(appt, now = new Date()) {
  return toDateTime(appt) >= now
}
