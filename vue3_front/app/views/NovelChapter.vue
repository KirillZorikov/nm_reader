<template>
	<div class="novel-chapter-conteiner m-auto">
		<SideBarChapter :open_collapses="open_settings_collapses" />
		<div class="top text-center">
			<a href="" class="title"
				><h1 class="novel-title" v-if="title">
					{{ title }}
				</h1></a
			>
			<div class="col-lg-6 mx-auto">
				<p class="chapter-name mb-4" v-if="chapter_name">
					{{ chapter_name }}
				</p>
				<div class="d-flex justify-content-center">
					<button
						type="button"
						class="button-top px-4"
						@click="clickNavigation('prev')"
					>
						<i class="fas fa-angle-left fs-6 align-middle"></i> Prev
						Chapter
					</button>
					<button
						type="button"
						class="button-top"
						data-bs-toggle="offcanvas"
						data-bs-target="#offcanvas"
						role="button"
					>
						<Icon
							:icon="icons.settingsLine"
							width="20"
							height="20"
						/>
					</button>

					<TranslateButton
						:translating="translating"
						:loading="loading"
						:lang_code="lang_code"
						:text_lang="current_text_lang"
						:translating_error="translating_error"
						@text_lang_changed="text_lang_change"
						@try_again="try_again"
						@open_settings="open_settings(['translate'])"
					/>

					<button type="button" class="button-top">
						<Icon
							:icon="icons.listUnordered"
							width="20"
							height="20"
						/>
					</button>
					<button
						type="button"
						class="button-top px-4 ml-4"
						@click="clickNavigation('next')"
					>
						Next Chapter
						<i class="fas fa-angle-right fs-6 align-middle"></i>
					</button>
				</div>
				<div class="text-start px-5 d-flex justify-content-center">
					<img src="../images/chapter-start.webp" />
				</div>
			</div>
		</div>

		<div class="text w-100 d-flex justify-content-center">
			<div class="text-wrapper py-4">
				<Loading :message="'Load chapter '" v-if="loading" />
				<template v-if="text.length && !loading">
					<p v-for="(p, index) in text" :key="index">
						{{ p }}
					</p>
				</template>
				<template v-if="author_note.length && !loading">
					<hr class="mx-4" />
					<p v-for="(p, index) in author_note" :key="index">
						{{ p }}
					</p>
				</template>
			</div>
		</div>

		<div class="bottom mx-auto">
			<div
				class="d-flex justify-content-center align-items-center flex-column"
			>
				<div class="text-start">
					<img src="../images/chapter-end.webp" />
				</div>
				<div class="d-flex justify-content-center">
					<button
						type="button"
						class="button-top px-4 ml-0"
						@click="clickNavigation('prev')"
					>
						<i class="fas fa-angle-left fs-6 align-middle"></i> Prev
						Chapter
					</button>
					<button type="button" class="button-top">
						<i class="fas fa-list"></i>
					</button>
					<button
						type="button"
						class="button-top px-4 ml-4 mr-0"
						@click="clickNavigation('next')"
					>
						Next Chapter
						<i class="fas fa-angle-right fs-6 align-middle"></i>
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { NovelService } from "../services/novel.service";
import { TranslateService } from "../services/translate.services";
import { default as VariousServices } from "../services/various.services";
import SideBarChapter from "../components/SideBarChapter.vue";
import Loading from "../components/Loading";
import TranslateButton from "../components/TranslateButton.vue";
import { Icon } from "@iconify/vue";
import googleTranslate from "@iconify-icons/mdi/google-translate";
import settingsLine from "@iconify-icons/clarity/settings-line";
import listUnordered from "@iconify-icons/codicon/list-unordered";

export default {
	name: "NovelChapter",

	SELECTORS: {
		settings: "#offcanvas",
	},

	components: { Loading, SideBarChapter, Icon, TranslateButton },
	props: {
		service_name: String,
		lang_code: String,
		novel_id: String,
		chapter_id: String,
		data: String,
	},
	data() {
		return {
			icons: {
				googleTranslate,
				settingsLine,
				listUnordered,
			},
			open_settings_collapses: ["style"],
			response_data: "",
			loading: false,
			translating: false,
			translating_error: false,
			original_text_data: {
				text: [],
				author_note: [],
				title: "",
				chapter_name: "",
			},
			translated_text_data: {},
			current_text_lang:
				this.$store.state.translate_chapter_settings.src_code,
		};
	},
	computed: {
		translate_chapter_settings() {
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
		translated() {
			if (this.service in this.translated_text_data) {
				return this.translated_text_data[this.service].translated;
			}
		},
		is_source_lang() {
			return (
				this.current_text_lang ===
				this.translate_chapter_settings.src_code
			);
		},
		is_destination_lang() {
			return (
				this.current_text_lang ===
				this.translate_chapter_settings.dst_code
			);
		},
		next_link() {
			let next_link;
			if (this.response_data.next) {
				next_link = this.response_data.next;
			}
			return next_link;
		},
		prev_link() {
			let prev_link;
			if (this.response_data.prev) {
				prev_link = this.response_data.prev;
			}
			return prev_link;
		},
		title() {
			let title = this.original_text_data.title;
			if (
				this.is_source_lang ||
				!(this.service in this.translated_text_data)
			) {
				return title;
			}
			return this.translated_text_data[this.service].title || title;
		},
		chapter_name() {
			let chapter_name = this.original_text_data.chapter_name;
			if (
				this.is_source_lang ||
				!(this.service in this.translated_text_data)
			) {
				return chapter_name;
			}
			return (
				this.translated_text_data[this.service].data[chapter_name] ||
				chapter_name
			);
		},
		text() {
			if (
				this.is_source_lang ||
				!(this.service in this.translated_text_data)
			) {
				return this.original_text_data.text;
			}
			return Array.from(
				{ length: this.original_text_data.text.length },
				(_, i) =>
					this.translated_text_data[this.service].data[
						this.original_text_data.text[i]
					] || this.original_text_data.text[i]
			);
		},
		author_note() {
			if (
				this.is_source_lang ||
				!(this.service in this.translated_text_data)
			) {
				return this.original_text_data.author_note;
			}
			return Array.from(
				{ length: this.original_text_data.author_note.length },
				(_, i) =>
					this.translated_text_data[this.service].data[
						this.original_text_data.author_note[i]
					] || this.original_text_data.author_note[i]
			);
		},
	},
	created() {
		if (this.data) {
			this.response_data = JSON.parse(this.data);
			this.reset_state();
			this.send_data_to_translate();
		} else {
			this.loadChapter();
		}
	},
	methods: {
		loadChapter() {
			this.loading = true;
			this.reset_state();
			NovelService.getChapter(
				this.lang_code,
				this.service_name,
				this.novel_id,
				this.chapter_id
			).then((response) => {
				this.response_data = response.data;
				this.loading = false;
				this.send_data_to_translate();
			});
		},
		loadChapterFromUrl(url) {
			this.loading = true;
			this.reset_state();
			NovelService.getDataFromLink(url).then((response) => {
				this.response_data = response.data;
				this.loading = false;
				this.send_data_to_translate();
			});
		},
		open_settings(collapses) {
			this.open_settings_collapses = collapses;
			VariousServices.offcanvas_action(
				this.$options.SELECTORS.settings,
				"show"
			);
		},
		try_again() {
			this.translating_error = false;
			this.current_text_lang = this.translate_chapter_settings.dst_code;
			this.init_translated_text_data();
			this.translateChapter();
		},
		send_data_to_translate() {
			this.saveText(this.response_data);
			if (this.auto_translate || this.is_destination_lang) {
				this.translateChapter();
			}
		},
		clear_translated_text_data() {
			let current_service_data = this.translated_text_data[this.service];
			this.translated_text_data = {};
			if (typeof current_service_data === "object") {
				this.translated_text_data[this.service] = current_service_data;
			}
		},
		init_translated_text_data() {
			let title = "";
			if (this.service in this.translated_text_data) {
				title = this.translated_text_data[this.service].title;
			}
			this.translated_text_data[this.service] = {
				title: title,
				data: {},
				translated: false,
			};
			this.original_text_data.author_note
				.concat(this.original_text_data.text, [
					this.original_text_data.chapter_name,
				])
				.forEach((e, i) => {
					this.translated_text_data[this.service].data[e] = "";
				});
		},
		saveText(data) {
			this.original_text_data.title =
				"title" in data ? data.title : data.title_link.text;
			this.original_text_data.chapter_name = data.name;
			this.original_text_data.text = data.text
				.split("\n")
				.filter((n) => n)
				.map((x) => x.trim());
			this.original_text_data.author_note = data.author_note
				? data.author_note
						.split("\n")
						.filter((n) => n)
						.map((x) => x.trim())
				: [];
			this.init_translated_text_data();
		},
		reset_state() {
			this.original_text_data = {
				text: [],
				author_note: [],
				title: this.original_text_data.title,
				chapter_name: "",
			};
			this.clear_translated_text_data();
			this.init_translated_text_data();
			this.translating_error = false;
			if (this.auto_translate) {
				this.current_text_lang =
					this.translate_chapter_settings.dst_code;
			} else {
				this.current_text_lang =
					this.translate_chapter_settings.src_code;
			}
		},
		clickNavigation(type) {
			if (type === "next" && this.next_link) {
				this.loadChapterFromUrl(this.next_link);
			} else if (type === "prev" && this.prev_link) {
				this.loadChapterFromUrl(this.prev_link);
			}
		},
		translateChapter() {
			this.translating = true;
			let kwargs = {
				service: this.service,
				dst: this.dst,
				src: this.src,
				parts: this.translate_services.find((x) => x.slug === this.service)
					.max_pages,
				paragraphs: Object.keys(
					this.translated_text_data[this.service].data
				),
			};
			VariousServices.translateArray({
				...kwargs,
				obj_to_fill: this.translated_text_data[this.service].data,
			}).then(
				(resp) => {
					this.translated_text_data[this.service].translated = true;
					this.translating = false;
					console.log(resp);
				},
				(error) => {
					console.log(error);
					this.translating = false;
					this.translating_error = true;
				}
			);
			if (!this.translated_text_data[this.service].title) {
				VariousServices.translateArray({
					...kwargs,
					paragraphs: [this.original_text_data.title],
					parts: 1,
					skip_init: true,
				}).then((resp) => {
					this.translated_text_data[this.service].title =
						resp[0].data[this.original_text_data.title];
					console.log(this.translated_text_data[this.service].title);
				});
			}
		},
		text_lang_change(new_) {
			this.current_text_lang = new_;
		},
	},
	watch: {
		response_data(new_) {
			if (new_) {
				let url = `${window.location.pathname}`;
				url = `${url.split("/").slice(0, -1).join("/")}/${
					new_.request_info.chapter_id
				}`;
				this.$router.push(url);
			}
		},
		current_text_lang(new_) {
			if (
				!this.translated &&
				!this.translating &&
				!this.loading &&
				this.is_destination_lang
			) {
				this.translateChapter();
			}
		},
		auto_translate(new_) {
			console.log(this.is_source_lang);
		},
		service(new_) {
			if (!this.translated) {
				this.init_translated_text_data();
			}
			if (
				!this.translated &&
				!this.translating &&
				!this.loading &&
				this.is_destination_lang
			) {
				this.translateChapter();
			}
		},
		src(new_, old) {
			if (this.current_text_lang === old) {
				this.current_text_lang = new_;
			}
		},
		dst(new_, old) {
			if (this.current_text_lang === old) {
				this.current_text_lang = new_;
				this.clear_translated_text_data();
				this.init_translated_text_data();
				this.translateChapter();
			}
		},
	},
};
</script>

<style scoped>
.m-card.search {
	min-height: 50vh;
	margin-top: 100px;
}
.chapter-name {
	color: #555;
	font-size: 18px;
}
.title {
	display: inline-block;
	font-size: 24px;
	font-weight: 700;
	text-transform: uppercase;
	text-shadow: 0 0 1px #c2c2c2;
	text-align: center;
	color: #3974a9;
	text-decoration: none;
}
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
.text-start img {
	margin: 15px 0 19px;
	max-width: 200px;
}
.text {
	min-height: 50vh;
	font-size: 17px;
	text-indent: 20px;
	line-height: 150%;
	letter-spacing: 0;
	word-spacing: 0;
}
.novel-chapter-conteiner {
	font-family: "Times New Roman";
	background-color: rgba(255, 255, 255, 30%);
}
.text-wrapper {
	border-top: 1px solid #dcdcdc;
	border-bottom: 1px solid #dcdcdc;
	width: 90%;
}
</style>
