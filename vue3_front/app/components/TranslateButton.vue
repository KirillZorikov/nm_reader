<template>
	<button
		type="button"
		class="button-top dropdown-toggle"
		id="dropdownMenuButton1"
		data-bs-toggle="dropdown"
	>
		<Icon icon="mdi:google-translate" width="20" height="20" />
	</button>
	<div
		class="dropdown-menu translate p-0"
		aria-labelledby="dropdownMenuButton1"
		@click="translate_dropdown_click"
	>
		<!-- <Select
			:now_val="current_src"
			:options="service_list_to_obj[current_service].languages"
			:option_value_key="'code'"
            :option_view_key="'name'"
		/>
		<Select
			:now_val="current_dst"
			:options="service_list_to_obj[current_service].languages"
			:option_value_key="'code'"
            :option_view_key="'name'"
		/> -->

		<div
			class="btn-close-container rounded-circle p-2 d-flex justify-content-center align-content-center"
			@click="dropdown_close"
		>
			<button
				type="button"
				class="btn-close shadow-none p-0"
				aria-label="Close"
			></button>
		</div>
		<div
			class="btn-menu-container rounded-circle d-flex justify-content-center align-content-center"
		>
			<button
				type="button"
				class="btn shadow-none p-0 dropdown-toggle"
				data-bs-toggle="dropdown"
				id="dropdown-menu"
			>
				<Icon
					icon="carbon:overflow-menu-vertical"
					width="20"
					height="20"
				/>
			</button>
			<ul class="dropdown-menu" aria-labelledby="dropdown-menu">
				<li>
					<a class="dropdown-item" @click="choose_another_lang"
						>Сhoose another language</a
					>
				</li>
				<li>
					<a class="dropdown-item" @click="try_again">Re-translate</a>
				</li>
			</ul>
		</div>
		<template v-if="translating_error">
			<h3 class="fs-3 ms-3 mt-3">Failed to translate</h3>
			<button
				type="button"
				class="btn mt-2 ms-3 mb-3 retry-button py-1 px-3 shadow-none"
				@click="try_again"
			>
				Try again
			</button>
		</template>
		<template v-else>
			<div
				class="ms-3 mt-2 d-flex justify-content-start lang-button-conteiner"
			>
				<button
					@click="change_text_lang(src)"
					type="button"
					class="btn lang-button shadow-none rounded-0"
					:class="current_text_lang == src ? 'selected' : ''"
				>
					{{ src_lang }}
				</button>
				<button
					@click="change_text_lang(dst)"
					type="button"
					class="btn lang-button shadow-none rounded-0"
					:class="current_text_lang == dst ? 'selected' : ''"
				>
					<div
						v-if="translating"
						class="spinner-border"
						role="status"
					></div>
					<template v-else>
						{{ dst_lang }}
					</template>
				</button>
			</div>
			<div class="form-check mt-3 mb-4 ms-3">
				<input
					class="form-check-input shadow-none"
					type="checkbox"
					id="auto_translate_check"
					v-model="translate_settings.auto_translate"
				/>
				<label class="form-check-label" for="auto_translate_check">
					Automatically translate
				</label>
			</div>
		</template>
		<div class="dropdown-bottom py-3 px-3 border-top">
			<Select
				class="ml-5"
				:now_val="service"
				:options="translate_services"
				:option_value_key="'slug'"
				:option_view_key="'name'"
				@value_changed="change_service"
			/>
		</div>
	</div>
</template>

<script>
import { Icon } from "@iconify/vue";
import { Dropdown } from "bootstrap";
import Select from "./Select.vue";
import { default as VariousServices } from "../services/various.services";

export default {
	name: "TranslateButton",
	components: { Icon, Select },
	props: [
		"translating",
		"loading",
		"lang_code",
		"text_lang",
		"translating_error",
	],
	emits: ["text_lang_changed", "try_again", 'open_settings'],
	computed: {
		services_obj() {
			let obj = {};
			this.translate_services.forEach((element, index) => {
				obj[element.slug] = element;
			});
			return obj;
		},
		dst_lang() {
			return VariousServices.get_lang_by_code(this.dst);
		},
		src_lang() {
			return this.src === "auto"
				? this.main_lang
				: VariousServices.get_lang_by_code(this.src);
		},
		current_text_lang() {
			return this.text_lang;
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
	},
	data() {
		return {
			translate_settings: {
				// current_src:
				// 	this.$store.state.translate_chapter_settings.src_code,
				// current_dst:
				// 	this.$store.state.translate_chapter_settings.dst_code,
				auto_translate:
					this.$store.state.translate_chapter_settings.auto_translate,
				// service:
				// 	this.$store.state.translate_chapter_settings.service_slug,
				text_lang: this.text_lang,
			},
			translate_services: this.$store.state.translate_services,
			main_lang: VariousServices.get_lang_by_code(this.lang_code),
		};
	},
	created() {
		this.first_word_bold(".dropdown-bottom option");
	},
	methods: {
		change_service(new_) {
			this.$store.commit("change_translate_chapter_settings", {
				service_slug: new_,
			});
		},
		try_again() {
			this.$emit("try_again");
		},
		change_text_lang(val) {
			console.log(val);
			this.translate_settings.text_lang = val;
			this.$emit("text_lang_changed", val);
		},
		dropdown_close({ selector }) {
			VariousServices.dropdown_close({
				selector: selector || ".button-top.dropdown-toggle",
			});
		},
		choose_another_lang() {
			// this.dropdown_close({
			// 	selector: ".btn-menu-container > .dropdown-toggle",
			// });
			this.$emit("open_settings");
		},
		translate_dropdown_click(event) {
			event.stopPropagation();
			if (!event.delegateTarget) {
				this.dropdown_close({
					selector: ".btn-menu-container > .dropdown-toggle",
				});
			}
		},
		async first_word_bold(selector) {
			let paragraphs = [];
			while (!paragraphs.length) {
				await new Promise((resolve) => setTimeout(resolve, 100));
				paragraphs = document.querySelectorAll(selector);
			}
			[...paragraphs].forEach((element, i) => {
				let first, other;
				[first, ...other] = element.textContent.split(" ");
				element.innerHTML = `<b>${
					element.textContent.split(" ")[0]
				}</b> ${other.join(" ")}`;
			});
		},
	},
	watch: {
		loading(new_) {
			if (new_) {
				return;
			}
			setTimeout(function () {
				let dropdown_toggle = document.querySelector(
					".button-top.dropdown-toggle"
				);
				let dropdown = new Dropdown(dropdown_toggle);
				dropdown.show();
			}, 500);
		},
		"translate_settings.auto_translate": function (new_) {
			this.$store.commit("change_translate_chapter_settings", {
				auto_translate: new_,
			});
		},
		// "translate_settings.service": function (new_) {
		// 	this.$store.commit("change_translate_chapter_settings", {
		// 		service_slug: new_,
		// 	});
		// },
	},
};
</script>

<style scoped>
.button-top {
	overflow: hidden;
	display: block;
	padding: 0 12px;
	line-height: 32px;
	font-size: 14px;
	color: #fff;
	background-color: #14425d;
	border: 1px solid #14425d;
	margin: 0 3px;
}
.button-top.dropdown-toggle::after {
	display: none;
}
.button-top.dropdown-toggle::after,
.btn-menu-container > .dropdown-toggle::after {
	display: none;
}
.form-select {
	width: fit-content;
	max-width: 45%;
}
.dropdown-menu.translate {
	min-width: 400px;
	left: calc(100vw - 115%) !important;
}
@media (max-width: 500px) {
	.dropdown-menu.translate {
		width: 100%;
		min-width: 100%;
		left: auto !important;
	}
}
.lang-button {
	min-width: 60px;
	padding-top: 0.15rem;
	padding-bottom: 0.15rem;
	text-transform: lowercase;
}
.lang-button.selected {
	outline: 2px solid #2d6df7;
	color: #2d6df7;
	transition: opacity 0.2s cubic-bezier(0.2, 0.6, 0.1, 1.2),
		color 0.2s cubic-bezier(0.2, 0.6, 0.1, 1.2);
}
.lang-button-conteiner {
	width: fit-content;
	border-bottom: 1px solid #828485;
}
.dropdown-bottom {
	background-color: #f1f1f2;
}
.dropdown-bottom .form-select {
	background-color: #f1f1f2;
	color: #828485;
}
.btn-close-container,
.btn-menu-container {
	position: absolute;
	right: 7px;
	top: 7px;
	width: 29px;
	height: 29px;
}
.btn-menu-container {
	right: 35px;
	top: 6px;
}
.dropdown-menu .btn-close {
	width: 13px;
	height: 13px;
}
.btn-close-container:hover,
.btn-menu-container:hover {
	background-color: rgba(206, 201, 201, 0.6);
}
.spinner-border {
	font-size: 0.5rem;
	width: 1rem;
	height: 1rem;
}
.retry-button {
	border: 1px solid #c9c9ca;
	background-color: #fff;
	color: #2d6df7;
}
.retry-button:hover {
	border: 1px solid #2d6df7;
	color: #2d6df7;
	animation: background_change 2s;
}
@keyframes background_change {
	from {
		background-color: #fff;
	}
	to {
		background-color: #2d6df718;
	}
}
</style>
