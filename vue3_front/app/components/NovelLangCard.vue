<template>
  <div class="m-card">
    <h2 class="lang">
      <img class="flag" :src="lang['flag']" alt="" />
      {{ lang["name"] }}
    </h2>

    <div class="post-content">
      <div class="box-container">
        <template v-for="service in list" :key="service">
          <NovelServiceBox :service="service" :lang_code="lang['code']" />
        </template>
        <div class="clear"></div>
      </div>
    </div>

  </div>
</template>

<script>
import NovelServiceBox from "./NovelServiceBox.vue";

export default {
  name: "NovelLangCard",
  components: { NovelServiceBox },
  props: ["list", "lang"],
};
</script>

<style>
.m-card {
  position: relative;
  -webkit-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12),
    0 1px 2px rgba(0, 0, 0, 0.24);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
  border-radius: 3px;
  width: 100%;
  color: rgba(0, 0, 0, 0.8);
  background-color: #fff;
  padding: 16px;
  box-sizing: border-box;
  margin: 24px 0;
}

.lang {
  margin: 0 0 10px;
  border-bottom: 1px solid #dfdfdf;
  padding-bottom: 5px;
}

.flag {
  max-height: 20px;
  display: inline;
}

.post-content {
  color: #333;
  font-size: 16px;
  line-height: 26px;
  clear: both;
  position: relative;
}

.clear {
  clear: both;
}
</style>