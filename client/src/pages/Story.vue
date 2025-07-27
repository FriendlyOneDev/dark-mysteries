<template>
  <div v-if="error">something went wrong</div>
  <div v-else class="wrapper">
    <Card 
      :puzzle="content?.puzzle"
      :emoji="content?.emoji"
      :title="content?.title"
    />
  </div>
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
</style>
<script>
  import Card from '../components/Card.vue';

  export default {
    components: { Card },
    data(){
      return {
        content: null, error: false
      }
    },
    async beforeRouteEnter(to, _, next){
      try{
        const story = await (await fetch(`/api/story/${to.params.id}`)).json();
        next(vm => vm.content = story);
      } catch{
        next(vm => vm.error = true);
      }
    },
    async beforeRouteUpdate(to, _){
      try{
        const story = await (await fetch(`/api/story/${to.params.id}`)).json();
        this.content = story;
      } catch{
        this.error = false;
      }
    },
  }
</script>