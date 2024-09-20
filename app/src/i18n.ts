import en from '@/locales/en.json'
import vi from '@/locales/vi.json'

import { createI18n, type I18nOptions } from 'vue-i18n'

const options: I18nOptions = {
  legacy: false,
  locale: 'en',
  fallbackLocale: 'vi',
  messages: {
    en,
    vi
  }
}

export const i18n = createI18n<false, typeof options>(options)
