import 'core-js/features/global-this';
document.documentElement.appendChild(
	Object.assign(document.createElement('script'), {
		textContent: 'window.globalThis = window',
	})
).remove();
import { createApp } from 'vue'
// feature flags
globalThis.__VUE_OPTIONS_API__ = process.env.NODE_ENV == "development"
globalThis.__VUE_PROD_DEVTOOLS__ = process.env.NODE_ENV == "development"

import App from './views/App.vue'
import router from './modules/router.js'
import store from './modules/store.js'
import './index.css'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

const init = () => {

	// new app instance
	const app = createApp(App)
		.use(store())
		.use(router())

	// mount
	app.mount('#app')
}

init()
