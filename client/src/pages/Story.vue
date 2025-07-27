<template>
  <Curtain :status="status">
    <div class="wrapper">
      <Flip :isFlipped="isFlipped">
       <slot name="front" v-if="!isFlipped">
          <Card 
          :puzzle="data.puzzle"
          :emoji="data.emoji"
          :title="data.title"
        >
          <div class="footer">
            <button class="btn-dashed" @click="flipCard">reveal solution</button>
            <router-link :to="{ name: 'chat', params: { id: route.params.id } }" class="btn-dashed">
              play with AI
            </router-link>
          </div>
        </Card>
        </slot>
        <slot name="back" v-else>
                    <Card 
            :puzzle="data.solution"
            :emoji="data.emoji"
            :title="Solution"
          >
            <div class="footer">
              <button class="btn-dashed" @click="flipCard">go back</button>
            </div>
          </Card>
        </slot>
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
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
</style>
<script setup>
  import { ref } from 'vue';

  import { useRoute } from 'vue-router';

  import Card from '../components/Card.vue';
  import Curtain from '../components/Curtain.vue';
  import useLoader from '../loader.js';
  import Flip from '../components/Flip.vue';

  const route = useRoute();
  const isFlipped = ref(false);

  const { status, data } = useLoader(() => route.params.id, async (id) => {
    return (await fetch(`/api/story/${id}`)).json();
  });

  const flipCard = () => {
    isFlipped.value = !isFlipped.value;
  }
</script>