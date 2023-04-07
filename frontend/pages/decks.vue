<script setup>
const index = '0'

const { data: decks } = await useFetch('http://localhost:8000/decks');

</script>

<template>
    <article data-theme="dark">
        <main class="container">
            <div class="row">
                <div class="flex-container">
                    <div class="pentagone">
                        <img class="logo" src="/img/logo.png"/>
                        <h2><a href="/pages/decks.vue" >Pentagone</a></h2>
                    </div>
                    <div>
                        <h2>Your Decks</h2>
                    </div>
                </div>
            </div>
            <div class="row button-container">
                <a role="button" href="/pages/index.vue" class="row">
                    <h1>{{ decks.data[0].name }}</h1>
                </a>
                <a role="button" href="/pages/index.vue" class="row">
                    <h1>{{ decks.data[1].name }}</h1>
                </a>
                <a role="button" href="/pages/index.vue" class="row">
                    <h1>{{ decks.data[2].name }}</h1>
                </a>
            </div>
        </main>
    </article>
</template>

<style scoped>
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
    background-color: #6486FF;
    min-height: 300px;
    max-width: 800px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.card-buttons > button {
    width: auto !important
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

.pentagone{
    display: flex;
}

.flex-container {
    display: flex;
    justify-content: space-between;
}

</style>