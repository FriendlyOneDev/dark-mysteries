<template>
  <router-link :to="{ name: 'story', params: { id: id } }">
    <div class="story">
      <div class="icon-box">
        <span class="emoji-small">{{ emoji }}</span>
      </div>
      <h3 class="title">{{ title }}</h3>
    </div>
  </router-link>
</template>
<script setup>
  const { title, emoji, id } = defineProps(['title', 'emoji', 'id']);
</script>
<style scoped>
  .story{
    display: flex;
    flex-direction: column;

    aspect-ratio: 1 / 1;

    box-sizing: border-box;
    padding: 20px;

    transition: background-color 100ms;
    border: var(--primary-color) dashed 5px;
  }
  .story:hover{
    background-color: var(--primary-color);
  }
  .icon-box{
    display: flex;
    justify-content: center;
    align-items: center;

    flex: 1;
  }
  .title{
    text-align: center;
  }
</style>