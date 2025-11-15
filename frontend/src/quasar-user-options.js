// src/quasar-user-options.js

// Quasar core styles
import 'quasar/src/css/index.sass'

// Icon set
import '@quasar/extras/material-icons/material-icons.css'

// Language & icon set
import lang from 'quasar/lang/en-US'
import iconSet from 'quasar/icon-set/material-icons'

// Quasar plugins
import { Notify, Dialog, Dark } from 'quasar'

// Optional: start in dark mode
Dark.set(true)

export default {
  config: {
    // You can also do: dark: true here if you want
  },
  plugins: {
    Notify,
    Dialog,
    Dark
  },
  lang,
  iconSet
}
