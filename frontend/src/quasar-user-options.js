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
    brand: {
      primary: '#73605B', // terracotta
      secondary: '#A7BEAE', // muted green
      accent: '#E7E8D1', // beige accent
      dark: '#2B2C28', // dark background base
      positive: '#A7BEAE',
      negative: '#B85042',
      info: '#A7BEAE',
      warning: '#E7E8D1',
    },
  },
  plugins: {
    Notify,
    Dialog,
    Dark,
  },
  lang,
  iconSet,
}
