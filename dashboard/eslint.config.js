import pluginVitest from '@vitest/eslint-plugin'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'
import vueTsEslintConfig from '@vue/eslint-config-typescript'
import importSort from 'eslint-plugin-import' 
import pluginVue from 'eslint-plugin-vue'

export default [
  {
    name: 'app/files-to-lint',
    files: ['**/*.{ts,mts,tsx,vue}'],
  },

  {
    name: 'app/files-to-ignore',
    ignores: ['**/dist/**', '**/dist-ssr/**', '**/coverage/**'],
  },

  ...pluginVue.configs['flat/essential'],
  ...vueTsEslintConfig(),
  
  {
    ...pluginVitest.configs.recommended,
    files: ['src/**/__tests__/*'],
  },
  skipFormatting,

  {
    plugins: {
      importSort
    },
    languageOptions: {
      parserOptions: {
        ecmaVersion: 2020
      }
    },
    rules: {
      '@typescript-eslint/no-explicit-any': ['off'],
      'vue/multi-word-component-names': 'off',
      'vue/valid-v-slot': 'off',
      'semi': ['error', 'never'],
      'no-extra-semi': 'error',
      'no-unexpected-multiline': 'error',
      'no-unreachable': 'error',
      'prefer-const': 'off',
      'vue/no-reserved-props': 'off',
      'ts-plugin': 'off',
      'quotes' : ['warn', 'single'],
      'importSort/order': [
        'warn',
        {
          'groups': [
            'builtin',
            'parent',
            'sibling',
            'object',
            'internal',
            'external'
          ],
          'pathGroups': [
            {
              pattern: '{vue,vue-router}',
              group: 'builtin',
              position: 'before'
            }, 
            {
              pattern: '@/components/parts/**',
              group: 'parent',
              position: 'before'
            }, 
            {
              pattern: '@/store/app',
              group: 'parent',
              position: 'after'
            },
            {
              pattern: '@/{mixins,utils}/**',
              group: 'sibling',
              position: 'before'
            }, 
            {
              pattern: '@/types/Interfaces',
              group: 'sibling',
              position: 'after'
            },
            {
              pattern: '@/setting/**',
              group: 'object',
              position: 'before'
            },
            {
              pattern: '*.css',
              group: 'object',
              position: 'after'
            },
          ],
          'pathGroupsExcludedImportTypes': ['builtin'],
          'newlines-between': 'always',
          'alphabetize': {
            'order': 'asc',
            'caseInsensitive': true
          }
        }
      ]
    }
  }
]
