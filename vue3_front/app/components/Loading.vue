<template>
  <span>
    <strong v-if="message">{{ message }}</strong>
    <strong v-else>Loading... </strong>
    <span class="spinner-border ml-4" role="status" aria-hidden="true"></span>
  </span>
</template>

<script>
export default {
  name: "Loading",
  props: ["message"],
}
</script>