<script setup>
const count = ref(0)
const flipped = ref(false);
const { data: context } = await useFetch('http://localhost:8000/')
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
                @click="flipped = !flipped">
                <p> {{ flipped }}</p>
                    <p v-if="flipped==false"> {{ JSON.stringify(context.data.words) }}</p>
                    <p v-else> {{ JSON.stringify(context.data.descs) }}</p>
                </button>
            </div>
            <div class="row">
                <h5>{{ count+1 }} of {{ parseInt(context.data.words.length) }}</h5>
            </div>
            <div class="row">
                <div class="col">
                    <a href="#" role="button" class="previous"
                    @click="count--">Previous</a>
                </div>
                <div class="col">
                    <a href="#" role="button" class="next"
                    @click="count++">Next</a>
                </div>
            </div>
        </main>
    </article>
</template>

<style scoped>
.apart {
    display: flex;
    justify-content: space-between;
}

[role=button] {
    display: flex;
    justify-content: center;
    margin: 30px;
}

.card {
    background-color: #6486FF;
    min-height: 300px;
    max-width: 800px;
}

.card-container {
    display: flex;
    justify-content: center;
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