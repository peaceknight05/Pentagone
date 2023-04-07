<script setup>
const count = ref(0)
const flipped = ref(false);
const { data: context } = await useFetch('http://localhost:8000/');
</script>

<template>
    <article data-theme="dark">
        <main class="container">
            <div class="row">
                <div class="flex-container">
                    <div class="pentagone">
                        <img class="logo" src="/img/logo.png"/>
                        <h2>Pentagone</h2>
                    </div>
                    <div>
                        <h2>Biology</h2>
                    </div>
                </div>
            </div>
            <div class="row card-container">

                <button class="card"
                @click="flipped = !flipped" >
                    <div v-if="flipped==false"><h3>{{ context.data.words[count] }}</h3></div>
                    <div v-else>
                        <h3>{{ context.data.descs[count] }}</h3>

                        <div class="card-buttons">
                            <button @click.prevent="console.log('rember button clicked')">I rember</button>
                            <button>I forgor</button>
                        </div>
                    </div>
                </button>
            </div>
            <div class="row">
                <h5>{{ count+1 }} of {{ parseInt(context.data.words.length) }}</h5>
            </div>
            <div class="row button-container">
                <div class="col">
                    <button class="previous" 
                    @click="count !== 0 ? count-- : count = context.data.words.length - 1">Previous</button>
                </div>
                <div class="col">
                    <button class="next"
                    @click="count < context.data.words.length - 1 ? count++ : count = 0">Next</button>
                </div>
            </div>
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
    background-color: #6486FF;
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

.pentagone{
    display: flex;
}

.flex-container {
    display: flex;
    justify-content: space-between;
}

</style>