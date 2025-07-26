<template>
  <div class="story">
    <div class="icon-box">
      <span class="icon">{{ emoji }}</span>
    </div>
    <h3 class="title">{{ title }}</h3>
  </div>
</template>
<script setup>
  const { title, emoji } = defineProps(['title', 'emoji']);
</script>
<style scoped>
  .story{
    display: flex;
    flex-direction: column;

    width: 200px;
    height: 200px;

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
  .icon{
    font-size: 64px;
    font-family: 'Noto Emoji';
    user-select: none;
    color: red;
  }
  .title{
    text-align: center;
  }
</style>