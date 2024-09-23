// eslint.config.mjs
import antfu from '@antfu/eslint-config'
// import vueI18n from '@intlify/eslint-plugin-vue-i18n'

export default antfu(
  {
    // Override stylistic rules
    stylistic: {
      indent: 2,
      quotes: 'single',
      semi: false,
      overrides: {
        'style/comma-dangle': 'error',
        'style/max-statements-per-line': 'off'
      }
    },
    vue: true,
    typescript: true
  },
  {
    rules: {
      // eslint-disable-next-line node/prefer-global/process
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      // eslint-disable-next-line node/prefer-global/process
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
    }
  }

  // I18n
//   ...vueI18n.configs['flat/recommended'],
//   {
//     rules: {
//       '@intlify/vue-i18n/no-dynamic-keys': 'error',
//       '@intlify/vue-i18n/no-unused-keys': [
//         'error',
//         {
//           extensions: ['.ts', '.vue']
//         }
//       ]
//     },
//     settings: {
//       'vue-i18n': {
//         localeDir: 'locales/*.{json}',
//         messageSyntaxVersion: '^10.0.1'
//       }
//     }
//   }
)
