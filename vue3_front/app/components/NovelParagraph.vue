<template>
	<p class="paragraph" @click="change_show_buttons">
		{{ paragraph }}
		<span
			v-if="show_buttons"
			class="d-flex justify-content-start w-100"
			:style="`margin-left: ${text_indent}`"
		>
			<Icon class="replace" icon="tabler:replace" @click="set_show_src_data(!show_src_data)" />
			<Icon class="edit ms-1" icon="bi:pencil-square" />
			<Icon class="close ms-3" icon="gg:close-r" @click="set_show_buttons(false)" />
		</span>
	</p>
</template>

<script>
import { Icon } from "@iconify/vue";

export default {
	name: "NovelParagraph",
	props: ["p_data", "lang", "service", "is_dst_lang"],
	components: { Icon },
	data() {
		return {
			show_buttons: false,
      show_src_data: false,
			text_indent: "0px",
		};
	},
	mounted() {
		this.text_indent = getComputedStyle(this.$el)["text-indent"];
	},
	computed: {
		paragraph() {
			let paragraph = this.p_data.original;
			if (!this.is_dst_lang || this.show_src_data) {
				return paragraph;
			}
			if (this.lang in this.p_data.translated[this.service]) {
				paragraph = this.p_data.translated[this.service][this.lang];
			}
			return paragraph;
		},
	},
	methods: {
		change_show_buttons(event) {
			if (event.path[0].tagName === "P") {
				this.show_buttons = !this.show_buttons;
			}
		},
    set_show_buttons(val) {
      this.show_buttons = val;
    },
    set_show_src_data(val) {
      this.show_src_data = val;
    }
	},
};
</script>

<style scoped>
p {
	cursor: pointer;
	width: fit-content;
}
p span {
	cursor: default;
}
p svg {
	cursor: pointer;
}
svg.close:hover {
  color: rgb(255, 0, 0);
}
svg.edit:hover {
  color: rgba(167, 194, 14, 0.814);
}
svg.replace:hover {
  color: rgb(35, 131, 8);
}
svg:active {
  border-radius: 10%;
  background-color: rgba(0, 64, 255, 0.059);
}
</style>
