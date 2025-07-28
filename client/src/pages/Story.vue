<template>
  <Curtain v-bind="status">
    <div class="full-height">
      <Header />
      <div class="center-view wrapper">
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
    </div>
  </Curtain>
</template>
<style scoped>
  .wrapper{
    --limit: 540px;

    display: flex;
    align-content: stretch;
    justify-content: stretch;

    flex: 1;
    box-sizing: border-box;
  }
  .footer{
    display: flex;
    align-content: center;
    gap: 10px;
  }
  .footer > *{
    flex: 1;
  }
</style>
<script setup>
  import { useFetcher } from '../loader.js';

  import Header from '../components/Header.vue';
  import Card from '../components/Card.vue';
  import Curtain from '../components/Curtain.vue';
  import Flip from '../components/Flip.vue';

  import { ref } from 'vue';

  const flipped = ref(false);
  const { status, data } = useFetcher((route) => fetch(`/api/story/${route.params.id}`));
</script>