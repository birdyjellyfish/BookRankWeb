<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue';

</script>

<template>
  <div class="flex flex-col px-6 space-y-4 max-w-250">
    
    <div>
      <h1 class="text-lg font-bold">Overview</h1>
      Inspired by Google's PageRank search ranking algorithm, 
      BookRank is a book recommendation system that makes use of graphs to recommend books.
    </div>

    <div>
      <h1 class="text-lg font-bold">How it works</h1>
      Based on the last book read that the user liked (we call this book A), 
      we find the neighbouring books of book A (books read by other users who also read A). For each neighbour, we calculate its combined score, 
      and select the top kth books. We can filter for the genre that user wants to read next as well.
    </div>

    <div>
      <h1 class="text-lg font-bold">Acknowledgements</h1>
      <ul class="list-disc list-inside">
        <li>
          <Button class="p-0" variant="link">
            <a href="https://github.com/zygmuntz/goodbooks-10k">
              zygmuntz/goodbooks-10k
            </a>
          </Button>
        </li>
        <li>
          <Button class="p-0" variant="link">
            <a href="https://github.com/malcolmosh/goodbooks-10k-extended">
            malcomosh/goodbooks-10k-extended
            </a>
          </Button>
        </li>
        <li>
          <Button class="p-0" variant="link">
            <a href="https://openlibrary.org/dev/docs/api/covers">
              Open Library Covers API
            </a>
          </Button>  
        </li>
      </ul>
    </div>
    
  </div>
</template>
