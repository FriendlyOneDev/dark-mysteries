<template>
  <Curtain v-bind="status">
    <div class="wrapper">
      <Flip :flipped="flipped">
        <template #front>
          <Card
            :puzzle="data.puzzle" :emoji="data.emoji" :title="data.title"
          >
            <div class="footer">
              <button @click="flipped = !flipped" class="btn-dashed">reveal solution</button>
              <router-link :to="{ name: 'chat', params: { id: $route.params.id } }" class="btn-dashed">
                play with AI
              </router-link>
            </div>
          </Card>
        </template>
        <template #back>
          <Card
            :puzzle="data.solution" :emoji="data.emoji" :title="data.title"
          >
            <div class="footer">
              <button @click="flipped = !flipped" class="btn-dashed">back to puzzle</button>
            </div>
          </Card>
        </template>
      </Flip>
      
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
    display: flex;
    gap: 10px;
  }
  .footer > *{
    flex: auto;
  }
</style>
<script setup>
  import { useFetcher } from '../loader.js';

  import Card from '../components/Card.vue';
  import Curtain from '../components/Curtain.vue';
  import Flip from '../components/Flip.vue';

  import { ref } from 'vue';

  const flipped = ref(false);
  const { status, data } = useFetcher((route) => fetch(`/api/story/${route.params.id}`));
</script>