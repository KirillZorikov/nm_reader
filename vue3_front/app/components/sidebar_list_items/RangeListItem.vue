<template>
	<li class="d-flex align-items-center justify-content-between px-3 mt-2">
		<label class="form-label m-0 text-center" style="width: 40%">{{
			label_text
		}}</label>
		<div class="input-wrapper w-50 text-center">
			<input
				type="range"
				class="form-range m-0"
				:min="min"
				:max="max"
				:step="step"
				v-model="value"
			/>
			<span class="input-val"> {{ value }}{{ measure }} </span>
		</div>
	</li>
</template>

<script>
export default {
	name: "RangeListItem",
	props: ["label_text", "measure", "name", "val", "min", "max", "step"],
	emits: ["val_changed"],
	data() {
		return {
			value: this.val,
		};
	},
	watch: {
		value(new_val) {
			let obj = {};
			obj[this.name] = new_val;
			this.$emit("val_changed", obj);
		},
		val(new_) {
			if (new_ !== this.value) {
				this.value = new_;
			}
		},
	},
};
</script>
