/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const customTheme = {
  dark: false,
  colors: {
    primary: '#0041c0',
    evenRow: '#F7F8F9',
    oddRow: '#FFFFFF',
    active: '#1E88E5',
    passive: '#C62828',
    caution: '#F3AE02',
    danger: '#FFCDD2'
  }
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme
    }
  }
})

export default vuetify