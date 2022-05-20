<template>
  <article class="post" v-if="novel_services">
    <div class="m-card search">
       
      <SearchNovel :service_name="service_name" :lang_code="lang_code" @search_completed="searchCompleted"/>
      <p>{{ novel_list }}</p>
    </div>
  </article>
</template>

<script>
import SearchNovel from "../components/SearchNovel.vue";

export default {
  name: "NovelService",
  components: { SearchNovel },
  props: ["service_name", "lang_code"],
  data() {
    return {
      loading: false,
      novel_list: [],
      novel_services: {},
    };
  },
  methods: {
      searchCompleted(novel_list){
          this.novel_list = novel_list;
      }
  }
};
</script>

<style scoped>
.m-card.search {
    min-height: 50vh;
    margin-top: 100px;
}
</style>
