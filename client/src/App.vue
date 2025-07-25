<template>
  <Header />
  <div class="wrapper">
    <Story v-for="story in stories" v-bind="story"/>
  </div>
</template>
<script setup>
  import Header from './Header.vue';
  import Story from './Story.vue';

  const stories = ([
    {emoji: '👑', title: 'The accident', text: 'A car driver causes an accident when he crashes into a bike, as he was making an unexpected turn at a crossroad. When the policemen arrive, another man gets arrested. The one who was driving is carried home.'},
    {emoji: '👑', title: 'The accident', text: 'A car driver causes an accident when he crashes into a bike, as he was making an unexpected turn at a crossroad. When the policemen arrive, another man gets arrested. The one who was driving is carried home.'},
    {emoji: '👑', title: 'The accident', text: 'A car driver causes an accident when he crashes into a bike, as he was making an unexpected turn at a crossroad. When the policemen arrive, another man gets arrested. The one who was driving is carried home.'},
    {emoji: '👑', title: 'The accident', text: 'A car driver causes an accident when he crashes into a bike, as he was making an unexpected turn at a crossroad. When the policemen arrive, another man gets arrested. The one who was driving is carried home.'},
    {emoji: '👑', title: 'The accident', text: 'A car driver causes an accident when he crashes into a bike, as he was making an unexpected turn at a crossroad. When the policemen arrive, another man gets arrested. The one who was driving is carried home.'}
  ])
</script>
<style scoped>
  .wrapper{
    width: 75%;
    margin: auto;

    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
</style>