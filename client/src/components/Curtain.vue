<template>
  <div v-if="!done">Loading...</div>
  <template v-else>
    <div v-if="error">
      Something went wrong..
    </div>
    <slot v-else></slot>
  </template>
</template>
<script setup>
  const { done, error } = defineProps(['done', 'error']);
</script>