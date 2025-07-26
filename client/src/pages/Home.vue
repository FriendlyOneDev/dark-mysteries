<template>
  <Header />
  <div class="wrapper">
    <div v-if="error">Something went wrong</div>
    <template v-else>
      <Story v-for="story in stories" v-bind="story"/>
    </template>
  </div>
</template>
<script>
  import Header from '../components/Header.vue';
  import Story from '../components/Story.vue';

  export default {
    components: { Header, Story },

    data(){
      return {
        stories: null, error: false
      }
    },
    async beforeRouteEnter(to, from, next) {
      try{
        const res = await fetch('/api/all_stories');
        const stories = await res.json();

        next(vm => vm.stories = stories)
      } catch{
        next(vm => vm.error = true)
      }
    }
  }
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