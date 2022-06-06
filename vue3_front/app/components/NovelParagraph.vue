<template>
  <p>{{ paragraph }}</p>
</template>

<script>
export default {
  name: "NovelParagraph",
  props: ["p_data", "lang", "service", "is_dst_lang"],
  computed: {
      paragraph() {
          let paragraph = this.p_data.orig;
          if (this.is_dst_lang) {
              return paragraph;
          };
          if (this.service in this.p_data.translated) {
              paragraph = this.p_data.translated[this.service];
          };
          return paragraph; 
      },
  },
};
</script>

<style>

</style>