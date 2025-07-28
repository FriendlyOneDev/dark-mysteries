<template>
  <div class="card">
    <h1 class="title">{{ title }}</h1>
    <div class="main">
      <span class="emoji-big">{{ emoji }}</span>
      <div class="description">{{ puzzle }}</div>
    </div>
    <slot>
      <div />
    </slot>
  </div>
</template>
<script setup>
  const { title, emoji, puzzle, solution } = defineProps([
    'title', 'emoji', 'puzzle', 'solution'
  ]);
</script>
<style scoped>
  .card{
    display: flex;
    flex-direction: column;

    justify-content: space-evenly;
    padding: 20px;
  }

  .main{
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .emoji-big{
    align-self: center;
  }

  .title, .description{
    text-align: center;
  }
  .title{
    text-align: center;
    justify-content: flex-start;
  }
</style>