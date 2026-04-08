<script setup lang="ts">
import ReadListView from '@/components/ReadListView.vue';
import RecommendView from '@/components/RecommendView.vue';
import { ref } from 'vue';



// function bookSelected(book: Book | null) {
//   console.log(book)
// }

// function genreSelected(genreid: number | null) {
//   console.log(`Genre Selected: ${genreid}`)
// }
</script>

<template>
  <RecommendView></RecommendView>
  <ReadListView></ReadListView>
</template>

<style scoped>

</style>