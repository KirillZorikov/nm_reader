import { createRouter, createWebHistory } from 'vue-router'
import { TranslateService } from "../services/translate.services"
import {store} from '../modules/store'
import { default as VariousServices } from "../services/various.services"

// Views
import Home from "./../views/Home.vue"
import Section from "./../views/Section.vue"
import NovelService from "./../views/NovelService.vue"
import NovelChapter from "./../views/NovelChapter.vue"

// Routes
const routes = [

	{ path: '/', name: 'Home', component: Home },
	{ path: '/section', component: Section },
	{ path: '/novel/:lang_code/:service_name', name: 'NovelService', component: NovelService, props: true },
	{ path: '/novel/:lang_code/:service_name/:novel_id/:chapter_id', name: 'NovelChapter', component: NovelChapter, props: true },
	// not found
	{ path: '/:pathMatch(.*)*', redirect: "/" }
]

// export Router Object
export default () => {

	const router = createRouter({

		routes,

		history: createWebHistory(),

		scrollBehavior(to, from, savedPosition) {

			// Avoid relocating the user when navigating to the same path
			if (to.path == from.path) return

			// transition delay
			const ms = from.name ? 350 : 0

			return new Promise(resolve => { setTimeout(() => { resolve(savedPosition ? savedPosition : { top: 0, left: 0 }) }, ms) })
		}
	})

	router.beforeEach(async (to, from, next) => {
		if (store.state.translate_services.length) {
			return next();
		}
		let fonts = await VariousServices.get_list_available_fonts();
		store.commit('change_available_fonts', fonts);
		let services = await TranslateService.getListTranslateServices();
		store.commit('change_translate_services', services.data);
		return next();
	});

	return router
}
