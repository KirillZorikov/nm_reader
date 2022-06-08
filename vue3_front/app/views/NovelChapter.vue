<template>
	<div class="novel-chapter-conteiner m-auto">
		<SideBarChapter :open_collapses="open_settings_collapses" />
		<div class="top text-center">
			<a href="" class="title"
				><h1 class="novel-title" v-if="title">
					{{ title }}
				</h1></a
			>
			<div>
				<div class="d-flex justify-content-center">
					<div>
						<NovelParagraph
							:is_dst_lang="is_destination_lang"
							:lang="current_text_lang"
							:p_data="chapter_name"
							:service="service"
						/>
					</div>
				</div>
				<!-- <span class="chapter-name mb-4 d-block" v-if="chapter_name">
					{{ chapter_name }}
				</span> -->
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
					<template v-for="(p, index) in text" :key="index">
						<!-- {{ p }} -->
						<NovelParagraph
							:is_dst_lang="is_destination_lang"
							:lang="current_text_lang"
							:p_data="p"
							:service="service"
						/>
						<!-- <button
							class="btn p-0 border-0 text-replace shadow-none"
						>
							<Icon icon="ri:translate" />
						</button> -->
					</template>
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
import NovelParagraph from "../components/NovelParagraph.vue";
import SideBarChapter from "../components/SideBarChapter.vue";
import Loading from "../components/Loading.vue";
import TranslateButton from "../components/TranslateButton.vue";

import { NovelService } from "../services/novel.service";
import { TranslateService } from "../services/translate.services";
import { default as VariousServices } from "../services/various.services";
import Chapter from "../models/novel.chapter";

import { Icon } from "@iconify/vue";
import googleTranslate from "@iconify-icons/mdi/google-translate";
import settingsLine from "@iconify-icons/clarity/settings-line";
import listUnordered from "@iconify-icons/codicon/list-unordered";

export default {
	name: "NovelChapter",

	SELECTORS: {
		settings: "#offcanvas",
	},

	components: {
		Loading,
		SideBarChapter,
		Icon,
		TranslateButton,
		NovelParagraph,
	},
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
			current_chapter: "",
			response_data: "",
			open_settings_collapses: ["style"],
			loading: false,
			translating: false,
			translating_error: false,
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
			if (this.current_chapter) {
				return this.current_chapter.data.is_translated(
					this.service,
					this.dst
				);
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
			if (this.current_chapter) {
				return this.current_chapter.data.next;
			}
		},
		prev_link() {
			if (this.current_chapter) {
				return this.current_chapter.data.next;
			}
		},
		title() {
			let title = "";
			console.log(this.is_source_lang, this.current_text_lang);
			if (this.current_chapter) {
				title = this.current_chapter.data.get_title(
					this.is_source_lang,
					this.service,
					this.dst
				);
			}
			return title;
		},
		chapter_name() {
			let chapter_name = "";
			if (this.current_chapter) {
				chapter_name = this.current_chapter.data.get_chapter_name(
					this.is_source_lang,
					this.service,
					this.dst
				);
			}
			return chapter_name;
		},
		text() {
			let text = [];
			if (this.current_chapter) {
				text = this.current_chapter.data.get_text(
					this.is_source_lang,
					this.service,
					this.dst
				);
			}
			return text;
		},
		author_note() {
			let author_note = [];
			if (this.current_chapter) {
				author_note = this.current_chapter.data.get_author_note(
					this.is_source_lang,
					this.service,
					this.dst
				);
			}
			return author_note;
		},
	},
	created() {
		if (this.data) {
			this.create_chapter(this.data);
			this.response_data = this.current_chapter.data.data;
			this.send_data_to_translate();
		} else {
			this.loadChapter();
		}
	},
	methods: {
		loadChapter() {
			this.loading = true;
			NovelService.getChapter(
				this.lang_code,
				this.service_name,
				this.novel_id,
				this.chapter_id
			).then((response) => {
				this.loading = false;
				this.create_chapter(response.data);
				this.response_data = response.data;
				this.send_data_to_translate();
			});
		},
		loadChapterFromUrl(url) {
			this.loading = true;
			NovelService.getDataFromLink(url).then((response) => {
				this.create_chapter(response.data);
				this.response_data = response.data;
				this.loading = false;
				this.send_data_to_translate();
			});
		},
		create_chapter(data) {
			this.current_chapter = new Chapter({ data: data });
			this.current_chapter.data.prepopulate_translated_text(
				this.service,
				this.dst
			);
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
			this.translateChapter();
		},
		clickNavigation(type) {
			if (type === "next" && this.next_link) {
				this.loadChapterFromUrl(this.next_link);
			} else if (type === "prev" && this.prev_link) {
				this.loadChapterFromUrl(this.prev_link);
			}
		},
		send_data_to_translate() {
			if (this.auto_translate || this.is_destination_lang) {
				this.translateChapter();
			}
		},
		translateChapter() {
			this.translating = true;
			let kwargs = {
				service: this.service,
				dst: this.dst,
				src: this.src,
				parts: this.translate_services.find(
					(x) => x.slug === this.service
				).max_pages,
				paragraphs: this.current_chapter.data.get_untran_text(
					this.service,
					this.dst
				),
			};
			VariousServices.translateArray({
				...kwargs,
				obj_to_fill:
					this.current_chapter.data.translated_text[this.service][
						this.dst
					],
			}).then(
				(resp) => {
					this.translating = false;
					console.log(resp);
				},
				(error) => {
					console.log(error);
					this.translating = false;
					this.translating_error = true;
				}
			);
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
		service(new_) {
			this.current_chapter.data.prepopulate_translated_text(
				new_,
				this.dst
			);
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
			this.current_chapter.data.prepopulate_translated_text(
				this.service,
				new_
			);
			if (this.current_text_lang === old) {
				this.current_text_lang = new_;
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
/* .text-wrapper p {
	position: relative;
	width: fit-content;
}
.text-replace {
	position: absolute;
	top: 0px;
	right: -10px;
	width: 1em;
	height: 1em;
	color: lightgrey;
	visibility: hidden;
}
.text-replace:hover {
	color: blue;
	border: 1px solid blue;
}
.text-replace svg {
	vertical-align: 0%;
}
.text-wrapper p:hover .text-replace {
	visibility: visible;
} */
</style>
