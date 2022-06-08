import { store } from "../modules/store";

class ChapterData {
	constructor(data) {
		if (typeof data === "string") {
			console.log(data);
			data = JSON.parse(data);
		}
		this.data = data;
		this.init_original_text(data);
		this.init_translated_text();
	}
	init_original_text(data) {
		let original_text = {
			text: [],
			author_note: [],
			title: "",
			chapter_name: "",
		};
		original_text.title =
			"title" in data ? data.title : data.title_link.text;
		original_text.chapter_name = data.name;
		original_text.text = data.text
			.split("\n")
			.filter((n) => n)
			.map((x) => x.trim());
		original_text.author_note = data.author_note
			? data.author_note
					.split("\n")
					.filter((n) => n)
					.map((x) => x.trim())
			: [];
		this.original_text = original_text;
	}
	init_translated_text() {
		let translated_text = {};
		store.state.translate_services.forEach((service) => {
			translated_text[service["slug"]] = {};
		});
		this.translated_text = translated_text;
	}

	get next() {
		return this.data.next;
	}
	get prev() {
		return this.data.prev;
	}
	get current() {
		return this.data.current;
	}
	get info() {
		return this.data.request_info;
	}
	get text_data() {
		let text_data = {};
		this.original_text.text
			.concat(
				this.original_text.author_note,
				[this.original_text.title],
				[this.original_text.chapter_name]
			)
			.forEach((val) => {
				text_data[val] = "";
			});
		return text_data;
	}

	prepopulate_translated_text(trans_service, lang_code) {
		if (lang_code in this.translated_text[trans_service]) {
			return;
		}
		this.translated_text[trans_service][lang_code] = { ...this.text_data };
	}
	is_translated(trans_service, lang_code) {
		if (!(lang_code in this.translated_text[trans_service])) {
			return false;
		}
		let untran_len = Object.entries(
			this.translated_text[trans_service][lang_code]
		).filter(([key, value]) => value === "").length;
		let all_len = Object.keys(this.text_data).length;
		return (untran_len / all_len) * 100 < 2;
	}
	get_untran_text(trans_service, lang_code) {
		return Object.entries(this.translated_text[trans_service][lang_code])
			.filter(([key, value]) => value === "")
			.map((x) => x[0]);
	}
	get_title(is_src_lang, trans_service, lang_code) {
		let title = this.original_text.title;
		if (is_src_lang) {
			return title;
		}
		if (this.translated_text[trans_service][lang_code][title]) {
			title = this.translated_text[trans_service][lang_code][title];
		}
		return title;
	}
	get_chapter_name(is_src_lang, trans_service, lang_code) {
		return this.prepare_paragraph(this.original_text.chapter_name);
		// let chapter_name = { original: this.original_text.chapter_name };
		// if (lang_code in this.translated_text[trans_service]) {
		// 	chapter_name.translated =
		// 		this.translated_text[trans_service][lang_code][chapter_name];
		// }
		// return chapter_name;

		// let chapter_name = this.original_text.chapter_name;
		// if (is_src_lang) {
		// 	return chapter_name;
		// }
		// if (this.translated_text[trans_service][lang_code][chapter_name]) {
		// 	chapter_name =
		// 		this.translated_text[trans_service][lang_code][chapter_name];
		// }
		// return chapter_name;
	}
	get_text(is_src_lang, trans_service, lang_code) {
		let text = [];
		this.original_text.text.forEach((val) => {
			text.push(this.prepare_paragraph(val));
		});
		return text;

		// let text = this.original_text.text;
		// if (is_src_lang) {
		// 	return text;
		// }
		// text = Array.from(
		// 	{ length: text.length },
		// 	(_, i) =>
		// 		this.translated_text[trans_service][lang_code][text[i]] ||
		// 		text[i]
		// );
		// return text;
	}
	get_author_note(is_src_lang, trans_service, lang_code) {
		let author_note = this.original_text.author_note;
		if (is_src_lang) {
			return author_note;
		}
		author_note = Array.from(
			{ length: author_note.length },
			(_, i) =>
				this.translated_text[trans_service][lang_code][
					author_note[i]
				] || author_note[i]
		);
		return author_note;
	}

	prepare_paragraph(paragraph) {
		let prepared_paragraph = { original: paragraph, translated: {} };
		store.state.translate_services.forEach((service) => {
			prepared_paragraph.translated[service["slug"]] = {};
			let entries = Object.entries(this.translated_text[service.slug]);
			for (const [lang_code, obj_trans] of entries) {
				if (obj_trans[paragraph]) {
					prepared_paragraph.translated[service["slug"]][lang_code] =
						obj_trans[paragraph];
				}
			}
		});
		return prepared_paragraph;
	}
}

export default class Chapter {
	constructor({ novel_id, chapter_id, service_name, lang_code, data }) {
		this.novel_id = novel_id;
		this.chapter_id = chapter_id;
		this.service_name = service_name;
		this.lang_code = lang_code;
		this.data = new ChapterData(data);
		if ("info" in this.data && this.data.info.length) {
			this.init_from_data();
		}
	}
	init_from_data() {
		this.novel_id = this.data.info.novel_id;
		this.chapter_id = this.data.info.chapter_id;
		this.service_name = this.data.info.service_name;
		this.lang_code = this.data.info.lang_code;
	}
}
