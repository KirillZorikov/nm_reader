<template>
	<li class="d-flex align-items-center justify-content-between px-3 mt-2">
		<label for="fontSize" class="form-label m-0 text-center"  style="width: 40%;">{{
			label_text
		}}</label>
		<div class="input-group input-group-sm" style="width: 30%">
			<button class="input-group-text" @click="change_value(-1)">
				–
			</button>
			<input
				type="text font-size"
				class="form-control shadow-none py-0 bg-light"
				aria-label="Sizing example input"
				v-model="value"
				disabled
				style="width: 4ch"
			/>
			<button class="input-group-text" @click="change_value(1)">+</button>
		</div>
	</li>
</template>

<script>
export default {
	name: "NumberListItem",
	props: ["label_text", "measure", "name", "val", "min", "max"],
	emits: ["val_changed"],
	data() {
		return {
			value: "" + this.val,
		};
	},
	methods: {
		change_value(val) {
			let border = this.measure
				? -this.measure.length
				: this.value.length;
			let new_val = parseInt(this.value.slice(0, border)) + val;
			if (this.min <= new_val && new_val <= this.max) {
				this.value = `${new_val}${this.measure}`;
			}
		},
	},
	watch: {
		value(new_val) {
			let obj = {};
			obj[this.name] = new_val;
			this.$emit("val_changed", obj);
		},
		val(new_) {
			console.log(new_)
			if ("" + new_ !== this.value) {
				this.value = "" + new_;
			}
		},
	},
};
</script>
