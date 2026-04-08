<script setup lang="ts">

import { ref, watch } from 'vue';
import BookSearch from './BookSearch.vue';
import GenreSelect from './GenreSelect.vue';
import type { BookLite } from './types';
import { useRecommender } from '@/composables/recommender';
import BookDetail from './BookDetail.vue';

import { Button } from '@/components/ui/button'
import { RotateCcw, Search, X } from 'lucide-vue-next';

import { toast } from 'vue-sonner'
import BookCarousel from './BookCarousel.vue';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import { Spinner } from '@/components/ui/spinner'


const selectedBook = ref<BookLite | null>(null);
const selectedGenre = ref<number | null>(null);
const selectedBookRec = ref<number>(0);

const {bookResults, loading, error, fetchRecs} = useRecommender();

const genreValue = ref('');

watch([selectedBook, selectedGenre], () => {
  // reset on change
  bookResults.value = [];
  error.value = null;
})

const searchNum = ref(0);

async function handleSearch() {
  if (!selectedBook.value || selectedGenre.value == null) {
    // check if selectedBook / selectedGenre is null
    error.value = "Recent liked book and genre must be provided.";
    toast.warning(error.value);
    return;
  }

  searchNum.value++;

  if (selectedGenre.value == 39) {
    // handle im feeling lucky
    await fetchRecs(selectedBook.value.bookid, null);
  } else {
    await fetchRecs(selectedBook.value.bookid, selectedGenre.value);
  }

  if (error.value) {
    toast.error(error.value)
  } else if (bookResults.value.length == 0) {
    toast.message("No recommendations found")
  }
}

const open = ref(false);

function handleBookClick(bookid: number) {
  selectedBookRec.value = bookid; 
  open.value = true;
}

function handleClearSearch() {
  bookResults.value = [];
  error.value = null;
  selectedBook.value = null;
  selectedGenre.value = null;
  genreValue.value = '';
}

</script>

<template>
  <div class="flex flex-col items-center p-4">
    <h1 class="text-6xl font-bold text-center p-6 mt-16 md:mt-32">
      Find your next book
    </h1>

    <form name="recommender" class="flex flex-col md:flex-row gap-4 mb-6" @submit.prevent="handleSearch">
      <BookSearch
        v-model="selectedBook"
        class="flex-1 p-4"
        :prompt="'Enter recently liked book'"/>
      <GenreSelect
        v-model:selected-genre="selectedGenre"
        v-model:value="genreValue"
        class="flex-1 p-4"/>
      <div class="flex gap-2">
        <Button class="rounded-full" type="submit" variant="outline" size="icon" v-if="bookResults.length !== 0">
          <RotateCcw />
        </Button>
        <Button
          class="rounded-full"
          type="submit"
          variant="outline"
          size="icon"
          v-else-if="selectedBook && selectedGenre !== null">
          <Spinner v-if="loading" />
          <Search v-else />
        </Button>
        <Button
          class="rounded-full"
          variant="outline"
          size="icon"
          disabled
          v-else>
          <Search />
        </Button>
        <Button
          class="rounded-full"
          variant="outline"
          size="icon"
          type="button"
          v-if="selectedBook || selectedGenre !== null"
          @click="handleClearSearch">
          <X />
        </Button>
        <Button
          class="rounded-full"
          variant="outline"
          size="icon"
          v-else
          disabled>
          <X />
        </Button>
      </div>
      
    </form>
    <div class="h-95 md:h-120">
      <Card v-if="bookResults.length !== 0" class="pl-10 pr-10 shadow-xl">
        <CardContent>
          <CardHeader class="font-semibold px-0 pb-2">Recommendations</CardHeader>
          <BookCarousel
            :key="searchNum"
            :books="bookResults"
            @selected-book="(bookid : number) => {handleBookClick(bookid)}"/>
        </CardContent>
      </Card>
      
    </div>
  </div>

  <Dialog v-model:open="open">
    <DialogContent class="p-15 min-w-sm md:min-w-2xl h-auto">
      <BookDetail :bookid="selectedBookRec"></BookDetail>
    </DialogContent>
  </Dialog>

  
</template>