<template>
  <article class="post" v-if="novel_services">
    <template v-for="(list, lang_code) in novel_services" :key="lang_code">
      <NovelLangCard :lang="getLangByCode(lang_code)" :list="list" />
    </template>
  </article>
</template>

<script>
import { NovelService } from "../services/novel.service";
import NovelLangCard from "../components/NovelLangCard.vue";

export default {
  name: "Home",
  components: { NovelLangCard },
  data() {
    return {
      loading: false,
      languages: [],
      novel_services: {},
    };
  },
  created() {
    this.loadData();
  },
  methods: {
    getLangByCode(code) {
      return this.languages.find((x) => x.code == code);
    },
    loadData() {
      this.loading = true;
      this.loadLanguages();
      this.loadListNovelServices();
      this.loading = false;
    },
    loadLanguages() {
      NovelService.getListLanguages().then((response) => {
        this.languages = response.data;
      });
    },
    loadListNovelServices() {
      NovelService.getListNovelsServices().then((response) => {
        this.novel_services = response.data;
        console.log(this.novel_services);
      });
    },
  },
};
</script>

<style>
article.post {
  position: relative;
  margin: 0 auto;
}

article {
  width: 100%;
  max-width: 900px;
  margin-right: 18px;
}
.loading_message {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
    font-size: x-large;
}
</style>
