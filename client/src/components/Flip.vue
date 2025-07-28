<template>
  <slot name="front" v-if="!flipped"></slot>
  <slot name="back" v-else></slot>
</template>
<script setup>
  const { flipped } = defineProps(['flipped']);
</script>