<template>
	<div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvas">
		<div class="offcanvas-header">
			<h6 class="offcanvas-title d-none d-sm-block">Chapter Settings</h6>
			<button
				type="button"
				class="btn-close text-reset"
				data-bs-dismiss="offcanvas"
				aria-label="Close"
			></button>
		</div>
		<div class="offcanvas-body px-0">
			<ul
				class="nav nav-pills flex-column mb-sm-auto mb-0 align-items-start"
				id="menu"
			>
				<li class="w-100">
					<button
						class="btn btn-toggle align-items-center shadow-none style-collapse"
						data-bs-toggle="collapse"
						data-bs-target="#style-collapse"
						aria-expanded="true"
					>
						Style
					</button>
					<div
						class="collapse show text-secondary"
						id="style-collapse"
						style=""
					>
						<ul
							class="btn-toggle-nav list-unstyled fw-normal pb-1 small"
						>
							<BackgroundPickListItem
								:background_options="options.theme"
								:background_now="style.theme"
								:style_name="'theme'"
								@style_changed="styleChange"
							/>
							<RangeListItem
								:label_text="'Text block width'"
								:measure="'%'"
								:name="'text_block_width'"
								:val="style.text_block_width"
								:min="30"
								:max="100"
								:step="1"
								@val_changed="styleChange"
							/>
							<RangeListItem
								:label_text="'Container background opacity'"
								:measure="'%'"
								:name="'container_background_opacity'"
								:val="style.container_background_opacity"
								:min="0"
								:max="100"
								:step="1"
								@val_changed="styleChange"
							/>
							<SelectListItem
								:label_text="'Font Family'"
								:options="options.font_family"
								:name="'font_family'"
								:val="style.font_family"
								:is_font_options="true"
								@val_changed="styleChange"
							/>
							<NumberListItem
								:label_text="'Font Size'"
								:max="40"
								:min="5"
								:measure="'px'"
								:name="'font_size'"
								:val="style.font_size"
								@val_changed="styleChange"
							/>
							<SelectListItem
								:label_text="'Font Weight'"
								:options="options.font_weight"
								:name="'font_weight'"
								:val="style.font_weight"
								@val_changed="styleChange"
							/>
							<RangeListItem
								:label_text="'Text Indent'"
								:measure="'px'"
								:name="'text_indent'"
								:val="style.text_indent"
								:min="0"
								:max="80"
								:step="1"
								@val_changed="styleChange"
							/>
							<RangeListItem
								:label_text="'Line Height'"
								:measure="'%'"
								:name="'line_height'"
								:val="style.line_height"
								:min="100"
								:max="500"
								:step="5"
								@val_changed="styleChange"
							/>
							<RangeListItem
								:label_text="'Letter Spacing'"
								:measure="'px'"
								:name="'letter_spacing'"
								:val="style.letter_spacing"
								:min="-10"
								:max="15"
								:step="0.1"
								@val_changed="styleChange"
							/>
							<RangeListItem
								:label_text="'Word Spacing'"
								:measure="'px'"
								:name="'word_spacing'"
								:val="style.word_spacing"
								:min="-10"
								:max="15"
								:step="0.1"
								@val_changed="styleChange"
							/>
						</ul>
					</div>
				</li>
				<li class="w-100">
					<button
						class="btn btn-toggle align-items-center shadow-none translate-collapse"
						data-bs-toggle="collapse"
						data-bs-target="#translate-collapse"
						aria-expanded="true"
					>
						Translate
					</button>
					<div
						class="collapse show text-secondary"
						id="translate-collapse"
						style=""
					>
						<ul
							class="btn-toggle-nav list-unstyled fw-normal pb-1 small"
						>
							<SelectListItem
								:label_text="'Translate Service'"
								:options="translate_services"
								:name="'service_slug'"
								:val="service"
								@val_changed="translate_settings_change"
								:option_value_key="'slug'"
								:option_view_key="'name'"
							/>
							<SelectListItem
								:label_text="'Source Language'"
								:options="services_obj[service].languages"
								:name="'src_code'"
								:val="src"
								@val_changed="translate_settings_change"
								:option_value_key="'code'"
								:option_view_key="'name'"
							/>
							<SelectListItem
								:label_text="'Destination Language'"
								:options="services_obj[service].languages"
								:name="'dst_code'"
								:val="dst"
								@val_changed="dst_change"
								:option_value_key="'code'"
								:option_view_key="'name'"
							/>
							<NumberListItem
								:label_text="'Max Pages'"
								:max="8"
								:min="0"
								:measure="''"
								:name="'max_pages'"
								:val="services_obj[service].max_pages"
								@val_changed="max_pages_change"
							/>
							<RangeListItem
								:label_text="'Timeout'"
								:measure="''"
								:name="'timeout'"
								:val="services_obj[service].timeout"
								:min="5"
								:max="60"
								:step="1"
								@val_changed="timeout_change"
							/>
						</ul>
					</div>
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
import RangeListItem from "./sidebar_list_items/RangeListItem.vue";
import BackgroundPickListItem from "./sidebar_list_items/BackgroundPickListItem.vue";
import NumberListItem from "./sidebar_list_items/NumberListItem.vue";
import SelectListItem from "./sidebar_list_items/SelectListItem.vue";
import { default as VariousServices } from "../services/various.services";
import { ParserServices } from "../services/parser.services";

export default {
	name: "SideBarChapter",

	COLLAPSES: {
		style: "#style-collapse",
		translate: "#translate-collapse",
	},
	SELECTORS: {
		translate_dropdown: ".button-top.dropdown-toggle",
		sidebar_offcanvas: "#offcanvas",
		close_button: "#offcanvas .btn-close",
	},

	props: ["open_collapses"],
	components: {
		RangeListItem,
		BackgroundPickListItem,
		NumberListItem,
		SelectListItem,
	},
	data() {
		return {
			style: {
				text_block_width: 90,
				font_family: "Times New Roman",
				font_size: "17px",
				font_weight: "normal",
				text_indent: 20,
				theme: "light",
				line_height: 150,
				letter_spacing: 0,
				word_spacing: 0,
				container_background_opacity: 30,
			},
			options: {
				font_family: this.$store.state.available_fonts,
				theme: {
					// "dark": "#000",
					yellow: "rgb(248, 241, 217)",
					tea: "rgba(20,70,50,0.1)",
					mint: "#e6fae4",
					sky: "#e0ffff",
					light_grey: "#eeeeee",
					laurel: "#e1eced",
					linen: "rgb(239, 234, 231)",
					light: "#f8f9fa",
				},
				font_weight: ["normal", "bolder", "lighter"],
			},
		};
	},
	computed: {
		translate_settings() {
			return this.$store.state.translate_chapter_settings;
		},
		translate_services() {
			return this.$store.state.translate_services;
		},
		src() {
			return this.$store.state.translate_chapter_settings.src_code;
		},
		dst() {
			return this.$store.state.translate_chapter_settings.dst_code;
		},
		service() {
			return this.$store.state.translate_chapter_settings.service_slug;
		},
		auto_translate() {
			return this.$store.state.translate_chapter_settings.auto_translate;
		},
		max_connections() {
			return this.$store.state.translate_chapter_settings.max_connections;
		},
		services_obj() {
			let obj = {};
			this.translate_services.forEach((element, index) => {
				obj[element.slug] = element;
			});
			return obj;
		},
	},
	mounted() {
		this.handle_collapses();
	},
	methods: {
		handle_collapses() {
			let entries = Object.entries(this.$options.COLLAPSES);
			for (const [collapse, selector] of entries) {
				console.log(this.open_collapses.includes(collapse));
				if (this.open_collapses.includes(collapse)) {
					VariousServices.collapse_action(selector, "show");
				} else {
					VariousServices.collapse_action(selector, "hide");
				}
			}
		},
		max_pages_change(val) {
			console.log(val);
			if (this.services_obj[this.service].max_pages !== val.max_pages) {
				ParserServices.set_max_pages(this.service, val.max_pages);
				this.$store.commit('update_translate_services', this.service, val);
			}
		},
		timeout_change(val) {
			if (this.services_obj[this.service].timeout !== val.timeout) {
				ParserServices.set_timeout(this.service, val.timeout);
				this.$store.commit('update_translate_services', this.service, val);
			}
		},
		changeFontSize(val) {
			let min_fs = 5;
			let max_fs = 40;
			let new_val = parseInt(this.style.font_size.slice(0, -2)) + val;
			if (min_fs <= new_val && new_val <= max_fs) {
				this.style.font_size = `${new_val}px`;
			}
		},
		changeTheme(val) {
			this.style.theme = val;
		},
		styleChange(obj) {
			let key = Object.keys(obj)[0];
			this.style[key] = obj[key];
		},
		translate_settings_change(obj) {
			console.log(obj);
			this.$store.commit("change_translate_chapter_settings", obj);
			console.log(this.translate_settings);
		},
		dst_change(obj) {
			this.translate_settings_change(obj);
			document
				.querySelector(this.$options.SELECTORS.close_button)
				.click();
			VariousServices.dropdown_action(
				this.$options.SELECTORS.translate_dropdown,
				"show"
			);
		},
	},
	watch: {
		"style.font_size": function (new_val) {
			document.querySelector(".text").style.fontSize = new_val;
		},
		"style.line_height": function (new_val) {
			document.querySelector(".text").style[
				"line-height"
			] = `${new_val}%`;
		},
		"style.container_background_opacity": function (new_val) {
			document.querySelector("main.container").style[
				"background-color"
			] = `rgba(255,255,255,${new_val}%)`;
		},
		"style.letter_spacing": function (new_val) {
			document.querySelector(".text").style[
				"letter-spacing"
			] = `${new_val}px`;
		},
		"style.word_spacing": function (new_val) {
			document.querySelector(".text").style[
				"word-spacing"
			] = `${new_val}px`;
		},
		"style.font_family": function (new_val) {
			document.querySelector(
				".novel-chapter-conteiner"
			).style.fontFamily = new_val;
		},
		"style.font_weight": function (new_val) {
			document.querySelector(".novel-chapter-conteiner").style[
				"font-weight"
			] = new_val;
		},
		"style.text_block_width": function (new_val) {
			document.querySelector(".text-wrapper").style.width = `${new_val}%`;
		},
		"style.text_indent": function (new_val) {
			document.querySelector(".text").style[
				"text-indent"
			] = `${new_val}px`;
		},
		"style.theme": function (new_val) {
			let color = this.options.theme[new_val];
			document.querySelector("body").style["background-color"] = color;
			document.querySelector("#offcanvas").style["background-color"] =
				color;
		},
		open_collapses(new_) {
			this.handle_collapses();
		},
	},
};
</script>

<style scoped>
.dropdown-toggle {
	outline: 0;
}

.nav-flush .nav-link {
	border-radius: 0;
}

.btn-toggle {
	display: inline-flex;
	align-items: center;
	padding: 0.25rem 0.5rem;
	font-weight: 600;
	color: rgba(0, 0, 0, 0.65);
	background-color: transparent;
	border: 0;
}
.btn-toggle:hover,
.btn-toggle:focus {
	color: rgba(0, 0, 0, 0.85);
	/* background-color: #d2f4ea; */
}

.btn-toggle::before {
	margin-right: 5px;
	width: 1.25em;
	line-height: 0;
	content: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='rgba%280,0,0,.5%29' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 14l6-6-6-6'/%3e%3c/svg%3e");
	transition: transform 0.35s ease;
	transform-origin: 0.5em 50%;
}

.btn-toggle[aria-expanded="true"] {
	color: rgba(0, 0, 0, 0.85);
}
.btn-toggle[aria-expanded="true"]::before {
	transform: rotate(90deg);
}

.btn-toggle-nav a {
	display: inline-flex;
	padding: 0.1875rem 0.4rem;
	margin-top: 0.125rem;
	margin-left: 1.25rem;
	text-decoration: none;
}
.btn-toggle-nav a:hover,
.btn-toggle-nav a:focus {
	background-color: #d2edf4;
}

.scrollarea {
	overflow-y: auto;
}

.fw-semibold {
	font-weight: 600;
}
.lh-tight {
	line-height: 1.25;
}
</style>
