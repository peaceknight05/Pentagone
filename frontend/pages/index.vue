<script setup>
const flipped = ref(false);
const displayData = ref(null);
const finished = ref(false);
watch(
  () => displayData.value,
  () => {}
);

const route = useRoute();
const router = useRouter();
const deck = route.query.deck;

const startReview = async () => {
  const { data, error } = await useFetch(
    "http://localhost:8000/start_review/",
    {
      method: "POST",
      body: {
        deck_name: deck,
      },
    }
  );
  displayData.value = data.value;
  if (error.value !== null) {
    alert(
      "An error has occurred while fetching the data: " +
        error.value.message +
        ". We'll redirect you back to your decks."
    );
    router.push("decks");
  }
};

const updateReview = async (state) => {
  const { data, error } = await useFetch("http://localhost:8000/review/", {
    method: "POST",
    body: {
      ...displayData.value.data,
      attempt: state,
    },
  });
  setTimeout(() => {
    displayData.value = data.value;
  }, 1500);
  if (displayData.value.message !== undefined) {
    finished.value = true;
    // Recreate nextReview in a more readable format, including the time.
    const nextReview = new Date(
      displayData.value.data.nextReview * 1000
    ).toLocaleString();
    alert(
      `You have finished the review! Your learning model has been tuned for your next review on ${nextReview}. We'll redirect you back to your decks.`
    );
    displayData.value = null;
    router.push("decks");
  }
  if (error.value !== null) {
    alert(
      "An error has occurred while fetching the data: " +
        error.value.message +
        ". We'll redirect you back to your decks."
    );
    router.push("decks");
  } else {
    displayData.value = data.value;
  }
};

if (deck !== undefined) {
  await startReview();
}
</script>

<template>
  <article data-theme="dark">
    <main class="container">
      <div class="row">
        <div class="flex-container">
          <div class="pentagone">
            <img class="logo" src="/img/logo.png" />
            <h2><a href="/decks">Pentagone</a></h2>
          </div>
          <div>
            <h2 v-if="deck !== undefined">{{ displayData.data.name }}</h2>
          </div>
        </div>
      </div>
      <div class="row card-container" v-if="deck !== undefined">
        <button class="card" @click="flipped = !flipped">
          <div v-if="flipped == false">
            <h3>{{ displayData.data.nextWord }}</h3>
          </div>
          <div v-else>
            <h3>{{ displayData.data.nextDefinition }}</h3>

            <div class="card-buttons">
              <button @click.prevent="updateReview('right')">I got it</button>
              <button @click.prevent="updateReview('wrong')">
                Need more time
              </button>
            </div>
          </div>
        </button>
      </div>
      <div class="row card-container" v-else>
        <h1 style="text-align: center">Welcome to Pentagone!</h1>
        <p>
          Click on the link above to see all the decks you have and can go
          through.
        </p>
      </div>
      <!-- <div class="row">
        <h5>{{ count + 1 }} of {{ parseInt(context.data.words.length) }}</h5>
      </div>
      <div class="row button-container">
        <div class="col">
          <button
            class="previous"
            @click="
              count !== 0 ? count-- : (count = context.data.words.length - 1)
            "
          >
            Previous
          </button>
        </div>
        <div class="col">
          <button
            class="next"
            @click="
              count < context.data.words.length - 1 ? count++ : (count = 0)
            "
          >
            Next
          </button>
        </div>
      </div> -->
    </main>
  </article>
</template>

<style scoped>
.button-container {
  display: flex;
  flex-direction: row;
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

.card-container {
  display: flex;
  justify-content: center;
}

.card-buttons {
  display: flex;
  gap: 30px;
}

.card-buttons > button {
  width: auto !important;
}

p {
  padding-right: 25px;
  padding-left: 25px;
  text-align: center;
}

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
