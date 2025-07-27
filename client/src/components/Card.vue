<template>
  <div class="card">
    <h1 class="title">{{ title }}</h1>
    <div class="main">
      <span class="icon-big">{{ emoji }}</span>
      <div class="description">{{ puzzle }}</div>
    </div>
    <div class="footer">
      <button class="btn-dashed">reveal solution</button>
      <button class="btn-dashed">play with ai</button>
    </div>
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
  .icon-big{
    align-self: center;
  }

  .title, .description{
    text-align: center;
  }
  .title{
    text-align: center;
    justify-content: flex-start;
  }
  .footer{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
</style>