<template>
  <Header />
  <main class="container">
    <router-view />
  </main>
</template>

<script>
import Header from "../components/Header.vue"

export default {
  name: "App",
  components: { Header },
};
</script>

<style>
main.container {
  margin: 0 auto 0;
  padding: 30px 0;
  min-height: 300px;
  width: 100%;
  max-width: 1222px;
  box-sizing: border-box;
}

body {
    padding: 0;
    margin: 0;
    background: #f2f3f4;
}
</style>
