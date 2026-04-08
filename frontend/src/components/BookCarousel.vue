<script setup lang="ts">
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel'

import { Skeleton } from '@/components/ui/skeleton'

import type { BookLite, BookUser } from './types';
import { ref } from 'vue';


const { books } = defineProps<{
  books: BookLite[] | BookUser[];
}>()

const imgLoaded = ref<Record<number, boolean>>({});

</script>

<template>
      <Carousel 
        class="w-80 md:w-150 lg:w-200"
        :opts="{
          slidesToScroll: 3,
          align: 'start'
        }"
      >
        <CarouselContent class="-ml-7 p-2">
          <CarouselItem 
            v-for="book in books"
            :key="book.bookid"
            class="basis-1/3 md:basis-1/4 lg:basis-1/5 flex flex-col pl-7"
            @click="$emit('selectedBook', book.bookid)">
            <div class="w-full aspect-2/3 hover:scale-105">
              <Skeleton class="w-full h-full rounded" v-if="!imgLoaded[book.bookid]"/>
              <img 
                :src="`https://covers.openlibrary.org/b/id/${book.coverid}-M.jpg?default=false`"
                class="w-full h-full rounded object-cover"
                v-show="imgLoaded[book.bookid]"
                @load="imgLoaded[book.bookid] = true"
                @error="imgLoaded[book.bookid] = false">
            </div>
            <div class="line-clamp-3 md:line-clamp-none">{{ book.title }}</div>
            <div class="line-clamp-2 text-muted-foreground">{{ book.authors }}</div>
          </CarouselItem>
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
  
</template>