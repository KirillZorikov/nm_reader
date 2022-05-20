<template>
  <div class="box">
    <router-link :to="{name: 'NovelService', params: {service_name: service.slug, lang_code: lang_code}}">
      <img class="novel-service-img" :src="service.logo" alt="" />
    </router-link>
    <router-link :to="{name: 'NovelService', params: {service_name: service.slug, lang_code: lang_code}}">
      {{ service.slug }}
    </router-link>
  </div>
</template>

<script>
export default {
  name: "NovelServiceBox",
  props: ["service", "lang_code"],
};
</script>

<style scoped>
.box {
  padding: 10px;
  width: calc(25% - 8px);
  height: 100px;
  box-sizing: border-box;
  text-align: center;
  display: block;
  float: left;
  border: 1px solid #eaeaea;
  margin: 4px;
  -webkit-box-shadow: 0px 0px 8px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 0px 0px 8px 0px rgba(0, 0, 0, 0.1);
  box-shadow: 0px 0px 8px 0px rgba(0, 0, 0, 0.1);
  position: relative;
}

.novel-service-img {
  height: 50px;
  display: block;
  margin: 0 auto 8px;
  max-width: 120px;
  overflow: hidden;
}

a.list-title {
  max-height: 40px;
  display: block;
  overflow: hidden;
  color: #333;
  font-size: 14px;
  font-weight: 700;
}
</style>