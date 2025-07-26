<template>
  <div class="wrapper">
    <div v-if="error">something went wrong</div>
    <template v-else>
      <h1>{{ content?.title }}</h1>
      <span class="icon-big">{{ content?.emoji }}</span>
      <div class="description">{{ content?.puzzle }}</div>
      <div class="bottom">
        <button class="btn-dashed">reveal solution</button>
        <button class="btn-dashed">play with AI</button>
      </div>
    </template>
  </div>
</template>
<style scoped>
  .wrapper{
    width: 75%;
    max-width: 540px;
    margin: auto;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    gap: 30px;
  }
  .description{
    text-align: center;
  }
  .bottom{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    width: 100%;
  }
</style>
<script>
  export default {
    data(){
      return {
        content: null, error: false
      }
    },
    mounted(){
      console.log('hello world');
    },
    async beforeRouteEnter(to, _, next) {
      console.log('before')
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