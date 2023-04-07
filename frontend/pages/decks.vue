<script setup>
const { data: decks } = await useFetch("http://localhost:8000/decks");
watch(
  () => decks.value,
  () => {}
);
</script>

<template>
  <article data-theme="dark">
    <main class="container">
      <div class="row">
        <div class="flex-container">
          <div class="pentagone">
            <img class="logo" src="/img/logo.png" />
            <h2><NuxtLink to="/decks">Pentagone</NuxtLink></h2>
          </div>
          <div>
            <h2>Your Decks</h2>
          </div>
        </div>
      </div>
      <div id="decks-container" v-for="deck in decks.data">
        <article>
          <h1>{{ deck.name }}</h1>
          <p>{{ deck.words.length }} terms</p>

          <NuxtLink :to="'/?deck=' + deck.name.toLowerCase()"
            ><button>Review now</button></NuxtLink
          >
        </article>
      </div>
    </main>
  </article>
</template>

<style scoped>
#decks-container > article {
  border: 2px solid #11191f;
  align-items: start;
}

#decks-container > article > * {
  margin: 0;
}

#decks-container > article button {
  margin-top: 1em;
}

.button-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 30px;
}

.button-container > div {
  flex: 1;
}

.card {
  background-color: #6486ff;
  min-height: 300px;
  max-width: 800px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-buttons > button {
  width: auto !important;
}

/* p {
  padding-right: 25px;
  padding-left: 25px;
  text-align: center;
} */

.logo {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.pentagone {
  display: flex;
}

.flex-container {
  display: flex;
  justify-content: space-between;
}
</style>
