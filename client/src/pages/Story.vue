<template>
  <Curtain v-bind="status">
    <div class="wrapper">
      <Card 
        :puzzle="data.puzzle" :emoji="data.emoji" :title="data.title"
      >
        <div class="footer">
          <button class="btn-dashed">revel solution</button>
          <router-link :to="{ name: 'chat', params: { id: $route.params.id } }" class="btn-dashed">
            play with AI
          </router-link>
        </div>
      </Card>
    </div>
  </Curtain>
</template>
<style scoped>
  .wrapper{
    max-width: 540px;
    width: 75%;
    height: 100vh;
    margin: auto;

    display: flex;
    align-content: stretch;
    justify-content: stretch;
    padding: 30px 0;

    box-sizing: border-box;
  }
  .footer{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
</style>
<script setup>
  import { useFetcher } from '../loader.js';

  import Card from '../components/Card.vue';
  import Curtain from '../components/Curtain.vue';
  import { watch } from 'vue';

  const { status, data } = useFetcher((route) => fetch(`/api/story/${route.params.id}`));
</script>