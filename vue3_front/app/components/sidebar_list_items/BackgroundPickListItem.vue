<template>
	<li class="d-flex align-items-center justify-content-between px-3 mt-2">
		<label for="customRange2" class="form-label m-0 text-center" style="width: 40%;"
			>Background
		</label>
		<div class="theme-wrapper" style="width: 60%">
			<template v-for="(color, name) in background_options" :key="name">
				<div
					class="rounded-circle border m-2 float-end"
					:class="
						name === background_now ? `chosen-theme ${name}` : name
					"
					style="width: 30px; height: 30px;"
                    :style="`background-color: ${color};`"
					@click="change_background(name)"
				>
					<div
						class="checkmark"
						:class="name"
						v-if="name === background_now"
					></div>
				</div>
			</template>
		</div>
	</li>
</template>

<script>
export default {
	name: "BackgroundPickListItem",
	props: [
		"background_options",
        "background_now",
		"style_name",
	],
	emits: ["style_changed"],
	methods: {
		change_background(theme) {
			let obj = {};
			obj[this.style_name] = theme;
			this.$emit("style_changed", obj);
		},
	},
};
</script>

<style scoped>
.theme-wrapper > .yellow {
	background: #f6edd4
		url("data:image/png;base64,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");
	background-size: 48px 48px;
	border-color: #d9cfb3;
}

.checkmark {
	display: inline-block;
	transform: rotate(45deg);
	height: 15px;
	width: 7px;
	margin-left: 38%;
	margin-top: 15%;
	border-bottom: 3px solid #4c5fe2;
	border-right: 3px solid #4c5fe2;
}
.chosen-theme {
	border: 1px solid #4c5fe2 !important;
}
.checkmark.dark {
	border-bottom: 3px solid #e5e6eb;
	border-right: 3px solid #e5e6eb;
}
.chosen-theme.dark {
	border: 1px solid #e5e6eb !important;
}

.theme-wrapper > .dark {
	background-color: #252528;
}
</style>
