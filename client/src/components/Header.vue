<template>
  <header class="header">
    <h1 class="title">DarkMysteries</h1>
    <ul class="links">
      <li>How to Play</li>
    </ul>
  </header>
</template>
<style scoped>
  .header{
    display: flex;
    padding: 0 30px;
    padding-top: 20px;
    align-items: center;
  }
  .title{
    flex: 1;
  }
  .links{
    flex-basis: auto;
    flex-shrink: 0;
    min-width: 20%;
  }
  .links{
    display: flex;
    justify-content: center;
    gap: 25px;
  }

  @media (max-width: 540px){
    .title{
      font-size: larger;
    }
  }
</style>