import { TranslateService } from "../services/translate.services";
import { Dropdown, Collapse, Offcanvas } from "bootstrap";

function splitArrayIntoChunks(array, parts) {
	let result = [];
	for (let i = parts; i > 0; i--) {
		result.push(array.splice(0, Math.ceil(array.length / i)));
	}
	return result;
}

class VariousServices {
	get_list_available_fonts() {
		const fontCheck = new Set(
			[
				// Web Safe Fonts
				"Arial",
				"Arial Black",
				"Verdana",
				"Tahoma",
				"Trebuchet MS",
				"Impact",
				"Times New Roman",
				"Didot",
				"Georgia",
				"American Typewriter",
				"Andalé Mono",
				"Courier",
				"Lucida Console",
				"Monaco",
				"Bradley Hand",
				"Brush Script MT",
				"Luminari",
				"Comic Sans MS",
				// Windows 10
				"Arial",
				"Arial Black",
				"Bahnschrift",
				"Calibri",
				"Cambria",
				"Cambria Math",
				"Candara",
				"Comic Sans MS",
				"Consolas",
				"Constantia",
				"Corbel",
				"Courier New",
				"Ebrima",
				"Franklin Gothic Medium",
				"Gabriola",
				"Gadugi",
				"Georgia",
				"HoloLens MDL2 Assets",
				"Impact",
				"Ink Free",
				"Javanese Text",
				"Leelawadee UI",
				"Lucida Console",
				"Lucida Sans Unicode",
				"Malgun Gothic",
				"Marlett",
				"Microsoft Himalaya",
				"Microsoft JhengHei",
				"Microsoft New Tai Lue",
				"Microsoft PhagsPa",
				"Microsoft Sans Serif",
				"Microsoft Tai Le",
				"Microsoft YaHei",
				"Microsoft Yi Baiti",
				"MingLiU-ExtB",
				"Mongolian Baiti",
				"MS Gothic",
				"MV Boli",
				"Myanmar Text",
				"Nirmala UI",
				"Palatino Linotype",
				"Segoe MDL2 Assets",
				"Segoe Print",
				"Segoe Script",
				"Segoe UI",
				"Segoe UI Historic",
				"Segoe UI Emoji",
				"Segoe UI Symbol",
				"SimSun",
				"Sitka",
				"Sylfaen",
				"Symbol",
				"Tahoma",
				"Times New Roman",
				"Trebuchet MS",
				"Verdana",
				"Webdings",
				"Wingdings",
				"Yu Gothic",
				// macOS
				"American Typewriter",
				"Andale Mono",
				"Arial",
				"Arial Black",
				"Arial Narrow",
				"Arial Rounded MT Bold",
				"Arial Unicode MS",
				"Avenir",
				"Avenir Next",
				"Avenir Next Condensed",
				"Baskerville",
				"Big Caslon",
				"Bodoni 72",
				"Bodoni 72 Oldstyle",
				"Bodoni 72 Smallcaps",
				"Bradley Hand",
				"Brush Script MT",
				"Chalkboard",
				"Chalkboard SE",
				"Chalkduster",
				"Charter",
				"Cochin",
				"Comic Sans MS",
				"Copperplate",
				"Courier",
				"Courier New",
				"Didot",
				"DIN Alternate",
				"DIN Condensed",
				"Futura",
				"Geneva",
				"Georgia",
				"Gill Sans",
				"Helvetica",
				"Helvetica Neue",
				"Herculanum",
				"Hoefler Text",
				"Impact",
				"Lucida Grande",
				"Luminari",
				"Marker Felt",
				"Menlo",
				"Microsoft Sans Serif",
				"Monaco",
				"Noteworthy",
				"Optima",
				"Palatino",
				"Papyrus",
				"Phosphate",
				"Rockwell",
				"Savoye LET",
				"SignPainter",
				"Skia",
				"Snell Roundhand",
				"Tahoma",
				"Times",
				"Times New Roman",
				"Trattatello",
				"Trebuchet MS",
				"Verdana",
				"Zapfino",
				// Linux
				"Liberation Mono",
				"Bitstream Charter",
				"URW Palladio L",
				"Ubuntu",
				"Ubuntu Mono",
				"Noto Mono",
				"Caladea",
				"Cantarell",
				"Montserrat",
				"Noto Serif",
				"Noto Color Emoji",
				// Android
				"monospace",
				"normal",
				"notoserif",
				"Roboto",
				"sans-serif",
				"sans-serif-light",
				"sans-serif-thin",
				"sans-serif-condensed",
				"sans-serif-medium",
				"serif",
			].sort()
		);

		return (async () => {
			await document.fonts.ready;

			const fontAvailable = new Set();

			for (const font of fontCheck.values()) {
				if (document.fonts.check(`12px "${font}"`)) {
					fontAvailable.add(font);
				}
			}
			return [...fontAvailable.values()];
		})();
	}

	async translateArray({
		service,
		paragraphs,
		dst,
		src = "auto",
		parts = 4,
		obj_to_fill = {},
		skip_init = false,
	}) {
		console.log(parts);
		if (!paragraphs.length) {
			return;
		}
		if (!skip_init && !service.endsWith("_api")) {
			await TranslateService.initPages(service);
			await new Promise((resolve) => setTimeout(resolve, 1000));
		}
		let chunks = splitArrayIntoChunks([...paragraphs], parts);
		let promises = [];
		chunks.forEach((chunk, index) => {
			let promise = TranslateService.getTranslate(
				{
					paragraphs: chunk,
					dst: dst,
					src: src,
				},
				service
			);
			if (obj_to_fill) {
				promise.then((resp) => {
					chunk.forEach((p, i) => {
						obj_to_fill[p] = resp.data[p];
					});
				});
			}
			promises.push(promise);
		});

		return Promise.all(promises);
	}

	get_lang_by_code(code) {
		const languageNames = new Intl.DisplayNames(["en"], {
			type: "language",
		});
		return languageNames.of(code);
	}

	dropdown_close({ selector }) {
		let dropdown_elm = document.querySelector(selector);
		let dropdown = new Dropdown(dropdown_elm);
		dropdown.hide();
	}

	dropdown_action(selector, action) {
		let dropdown_elm = document.querySelector(selector);
		let current_open = dropdown_elm.classList.contains("show");
		if (
			(current_open && action === "hide") ||
			(!current_open && action === "show")
		) {
			let dropdown = new Dropdown(dropdown_elm);
			dropdown[action]();
		}
	}

	collapse_action(selector, action) {
		let collapse_elm = document.querySelector(selector);
		let current_open = collapse_elm.classList.contains("show");
		if (
			(current_open && action === "hide") ||
			(!current_open && action === "show")
		) {
			let collapse = new Collapse(collapse_elm);
			console.log(collapse);
			collapse[action]();
		}
	}

	offcanvas_action(selector, action) {
		let offcanvas_elm = document.querySelector(selector);
		let current_open = offcanvas_elm.classList.contains("show");
		if (
			(current_open && action === "hide") ||
			(!current_open && action === "show")
		) {
			let offcanvas = new Offcanvas(offcanvas_elm);
			offcanvas[action]();
		}
	}
}

export default new VariousServices();
