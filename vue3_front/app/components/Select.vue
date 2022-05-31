<template>
	<select class="form-select shadow-none py-0" v-model="value">
		<template v-for="option in options" :key="option">
			<option
				:value="get_option(option, option_value_key)"
				:selected="get_option(option, option_value_key) === value"
			>
				{{ get_option(option, option_view_key) }}
			</option>
		</template>
	</select>
</template>

<script>
export default {
	name: "Select",
	props: [
		"options",
		"now_val",
		"name",
        "option_value_key",
        "option_view_key",
	],
	emits: ["value_changed"],
	data() {
		return {
			value: this.now_val,
		};
	},
    methods: {
        get_option(option, key) {
            return key? option[key]: option;
        }
    },
	watch: {
		value(new_val) {
			this.$emit("value_changed", new_val);
		},
		now_val(new_) {
			if (this.value !== new_) {
				this.value = new_;
			}
		},
	},
};
</script>
