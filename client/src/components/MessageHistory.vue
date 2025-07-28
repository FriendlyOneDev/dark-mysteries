<template>
  <div class="history">
    <div :class="['message', type ? 'question' : 'answer']" v-for="{text, type} in messages">
      <div class="bubble"> {{ text }} </div>
    </div>
  </div>
</template>
<style scoped>
  .bubble{
    display: inline-block;
    background-color: var(--primary-color);
    padding: 10px;

    min-width: 30%;
    max-width: 50%;

    text-align: initial;
    border-radius: 3px;
  }
  .message{
    margin-bottom: 10px;
  }
  .message.question{
    text-align: right;
  }
  .message.answer{
    text-align: left;
  }
  .history{
    overflow-x: scroll;
    padding-right: 20px;
  }
</style>
<script setup>
  const { messages } = defineProps(['messages']);
</script>