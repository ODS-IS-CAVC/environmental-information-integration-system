<script lang="ts" setup>
import { Authenticator, translations } from '@aws-amplify/ui-vue'
import { I18n } from 'aws-amplify/utils'
import '@aws-amplify/ui-vue/styles.css'

I18n.putVocabularies(translations)
I18n.setLanguage('ja')

// サインアップ処理無効にするための関数
const handleSignUp = () => {}
const services = {
  handleSignUp
}
</script>
<template>
  <authenticator
    :services="services"
    class="app">
    <v-app>
      <v-main>
        <RouterView />
      </v-main>
    </v-app>
  </authenticator>
</template>
<style lang="scss">
.app {
  margin-top: 10vh;
  .amplify-tabs {
    display: none;
  }
  .amplify-button--primary {
    background: rgb(var(--v-theme-primary));
  }
}
</style>
