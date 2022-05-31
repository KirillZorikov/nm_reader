import { createStore } from "vuex";

const translate_chapter_settings = JSON.parse(
	localStorage.getItem("translate_chapter_settings")
);
const initialState = translate_chapter_settings
	? translate_chapter_settings
	: {
			src_code: "auto",
			dst_code: "en",
			service_slug: "deepl",
			auto_translate: false,
			max_connections: 3,
			timeout: 15,
			retry_count: 1,
	  };

export const store = createStore({
	state: {
		translate_services: [],
		available_fonts: [],
		translate_chapter_settings: initialState,
	},
	getters: {
		get_translate_services: (state) => {
			return state.translate_services;
		},
		get_available_fonts: (state) => {
			return state.available_fonts;
		},
	},
	mutations: {
		change_translate_services(state, new_) {
			state.translate_services = new_;
		},
		update_translate_services(state, service, fields) {
			let index = state.translate_services.findIndex(x => x.slug === service);
			let new_obj = {...state.translate_services[index], ...fields};
			state.translate_services[index] = new_obj;
		},
		change_available_fonts(state, new_) {
			state.available_fonts = new_;
		},
		change_translate_chapter_settings(state, new_) {
			let new_obj = {...state.translate_chapter_settings, ...new_}
			state.translate_chapter_settings = new_obj;
		},
	},
});
