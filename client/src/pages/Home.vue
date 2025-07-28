<template>
  <Header />
  <div class="center-view wrapper">
    <div v-if="error">Something went wrong</div>
    <template v-else>
      <Story v-for="story in stories" v-bind="story"/>
    </template>
  </div>
</template>
<script>
  import Header from '../components/Header.vue';
  import Story from '../components/StoryLink.vue';

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
  .header{
    margin-bottom: 50px;
  }
  .wrapper{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    align-content: center;

    --limit: 840px;
  }
</style>