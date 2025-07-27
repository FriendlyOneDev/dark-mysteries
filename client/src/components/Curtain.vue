<template>
  <div v-if="status == 'error'">Something went wrong</div>
  <template v-else-if="status == 'done'">
    <slot></slot>
  </template>
</template>
<script setup>
  const { status } = defineProps(['status']);
</script>