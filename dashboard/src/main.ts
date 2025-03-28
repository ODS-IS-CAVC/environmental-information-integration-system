import { createApp } from 'vue'

import App from './App.vue'
// @ts-expect-error: AWS Amplifyで生成されるファイルがjs形式のため
import api_exports from './aws-api-exports.js'
// @ts-expect-error: AWS Amplifyで生成されるファイルに合わせてjs形式なため
import aws_exports from './aws-exports.js' 
import vuetify from './plugins/vuetify.ts'
import router from './router'

import AmplifyVue from '@aws-amplify/ui-vue'
import { Amplify } from 'aws-amplify'
import { createPinia } from 'pinia'

aws_exports.aws_cloud_logic_custom = api_exports
Amplify.configure(aws_exports)
const app = createApp(App)

app.use(createPinia())
app.use(AmplifyVue)
app.use(router)
app.use(vuetify)

app.mount('#app')
