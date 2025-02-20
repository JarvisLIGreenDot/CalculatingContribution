import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// 创建 Vuetify 实例
const vuetify = createVuetify({
  components,
  directives,
})

createApp(App)
  .use(store)
  .use(router)
  .use(vuetify)
  .mount('#app')