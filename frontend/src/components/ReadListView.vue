<script setup lang="ts">
import { getCSRFToken, useAuthStore } from '@/stores/auth';
import { useFetch } from '@vueuse/core';
import type { BookUser } from './types';
import { onMounted, ref, watch } from 'vue';
import BookDetail from './BookDetail.vue';
import ReadListRecord from './ReadListRecord.vue';
import { useReadlist } from '@/composables/readlistRecord';
import AddRecord from './AddRecord.vue';
import BookCarousel from './BookCarousel.vue';
import Button from './ui/button/Button.vue';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import {
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from '@/components/ui/empty'

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
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip'

import { BookCheck, CircleUserRound, Library } from 'lucide-vue-next';

const authStore = useAuthStore();

watch(() => authStore.isAuthenticated, (isAuth) => {
  fetchRecords(); 
})

const {loading, error, success, data, fetchRecords} = useReadlist();

const selectedRecord = ref<BookUser | null>(null);

const openRecord = ref(false);
const createRecord = ref(false);

function handleBookSelect(bookid: number) {
  selectedRecord.value = data.value.find(record => record.bookid === bookid)!;
  openRecord.value = true;
}

onMounted(() => {
  fetchRecords();
})
</script>

<template>
  <div class="flex flex-col px-6">
    <span class="flex gap-4 items-center">
      <h1 class="text-3xl font-bold">
        My Read List
      </h1>
      <div v-if="authStore.isAuthenticated">
        <Button
          class="h-full"
          variant="outline"
          @click="createRecord = true">
          <BookCheck />
          Add
        </Button>
      </div>
      <div v-else>
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger>
              <Button
                class="h-full"
                variant="outline"
                disabled>
                <BookCheck />
                Add
              </Button>
            </TooltipTrigger>
            <TooltipContent>
              Sign in to add books to your read list.
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
       
      </div>
      
    </span>
    <span>
      Books added here will be excluded from recommendations.
    </span>
    
    <div class="h-95 md:h-120 flex flex-col">
      <Empty 
        v-if="authStore.isAuthenticated && data.length == 0"
        class="border border-dashed mt-4">
        <EmptyHeader>
          <EmptyMedia variant="icon">
            <Library></Library>
          </EmptyMedia>
          <EmptyTitle>
            Read List Empty
          </EmptyTitle>
          <EmptyDescription>
            Add some books to your read list.
          </EmptyDescription>
        </EmptyHeader>
      </Empty>

      <Card  v-else-if="authStore.isAuthenticated" class="mt-4 pl-10 pr-10 shadow-xl mx-auto">
        <CardContent >
          <p v-if="error">{{ error }}</p>
          <p v-else-if="loading">Loading...</p>
          <BookCarousel
            v-else-if="data"
            :books="data"
            @selected-book="(bookid: number) => handleBookSelect(bookid)" />
        </CardContent>
      </Card>

      <Empty v-else class="border border-dashed mt-4">
        <EmptyHeader>
          <EmptyMedia variant="icon">
            <CircleUserRound></CircleUserRound>
          </EmptyMedia>
          <EmptyTitle>
            User not signed in
          </EmptyTitle>
          <EmptyDescription>
            Sign in / sign up to access your read list.
          </EmptyDescription>
        </EmptyHeader>
      </Empty>
      </div>
  </div>
  
  <!-- other than book details, include datefinished and update/delete options-->
  <Dialog
    v-model:open="openRecord">
    <DialogContent v-if="selectedRecord" class="p-4 md:p-15 min-w-sm md:min-w-2xl h-auto">
      <ReadListRecord
        :record="selectedRecord"
        @refresh="fetchRecords"
        @close="openRecord = false"/>
    </DialogContent>
  </Dialog>

  <Dialog
    v-model:open="createRecord">
    <DialogContent class="w-auto">
      <AddRecord
        @refresh="fetchRecords"
        @close="createRecord = false"></AddRecord>
    </DialogContent>
  </Dialog>

</template>