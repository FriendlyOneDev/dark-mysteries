<template>
  <Curtain v-bind="status">
    <Header />
    <div class="center-view wrapper">
      <Story v-for="story in data" v-bind="story"/>
    </div>
  </Curtain>
</template>
<script setup>
  import Curtain from '../components/Curtain.vue';
  import Header from '../components/Header.vue';
  import Story from '../components/StoryLink.vue';

  import { useFetcher } from '../loader';
  
  const { status, data } = useFetcher(() => fetch('/api/all_stories'));
</script>
<style scoped>
  .header{
    margin-bottom: 50px;
  }
  .wrapper{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    align-content: center;
    padding: 10px;

    --limit: 840px;
  }
</style>