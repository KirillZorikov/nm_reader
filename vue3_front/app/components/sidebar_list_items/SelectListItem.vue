<template>
	<li class="d-flex align-items-center justify-content-between px-3 mt-2">
		<label class="form-label m-0 text-center" style="width: 40%;">{{
			label_text
		}}</label>
		<select class="form-select w-50 shadow-none py-0" v-model="value">
			<template v-for="option in options" :key="option">
				<option
					:value="get_option(option, option_value_key)"
					:selected="option === value"
					:style="is_font_options ? `font-family: ${option};` : ''"
				>
					{{ get_option(option, option_view_key) }}
				</option>
			</template>
		</select>
	</li>
</template>

<script>
export default {
	name: "SelectListItem",
	props: [
		"label_text",
		"name",
		"val",
		"options",
		"is_font_options",
        "option_value_key",
        "option_view_key",
	],
	emits: ["val_changed"],
	data() {
		return {
			value: this.val,
		};
	},
	methods: {
		get_option(option, key) {
            return key? option[key]: option;
        }
	},
	watch: {
		value(new_val) {
			let obj = {};
			obj[this.name] = new_val;
			this.$emit("val_changed", obj);
		},
	},
};
</script>
