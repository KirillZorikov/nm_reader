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
  margin: 30px auto 30px;
  min-height: 300px;
  width: 100%;
  max-width: 1112px;
  box-sizing: border-box;
}

body {
    padding: 0;
    margin: 0;
    background: #f2f3f4;
}
</style>
