<script setup lang="ts">
import { onMounted, ref } from 'vue';
import type { Genre } from './types';

import { Sparkle } from 'lucide-vue-next';
import { toast } from 'vue-sonner';

import { CheckIcon, ChevronsUpDownIcon } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { cn } from '@/lib/utils';


const selectedGenre = defineModel<number | null>('selected-genre');
const genres = ref<Genre[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const url = import.meta.env.VITE_API_URL;

const fetchGenres = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch(`${url}/genres`)

    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    
    genres.value = await response.json();

  } catch (err) {
    error.value = `fetchGenres: ${(err as Error).message}`;
    toast.error(error.value);
  } finally {
    loading.value = false;
  }
}

const open = ref(false);
const value = defineModel<string>('value');

function selectGenre(genreName: string, genreId: number) {
  // if already selected, deselect, else select
  if (value.value === genreName) {
    // deselect
    value.value = '';
    selectedGenre.value = null;
  } else {
    value.value = genreName;
    selectedGenre.value = genreId;
  }
  open.value = false;
}

onMounted(async () => {
  await fetchGenres();

  // re arrange genres so that I'm feeling lucky is at the top
  genres.value.unshift(genres.value.pop()!);
});
</script>

<template>
  <Popover v-model:open="open">
    <PopoverTrigger as-child>
      <!-- <Sparkle></Sparkle> -->
      <Button
        variant="outline"
        role="combobox"
        :aria-expanded="open"
        :class="cn('w-100 md:w-50 justify-between font-normal', selectedGenre === null && 'text-muted-foreground')"
      >
        <Sparkle></Sparkle>
        <span v-if="value" class="font-semibold">{{ value }}</span>
        <span v-else>Select a genre</span>
        <ChevronsUpDownIcon class="ml-2 h-4 w-4 shrink-0" />
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-100 md:w-50 p-0">
      <Command>
        <CommandInput placeholder="Search genres..." />
        <CommandList>
          <CommandEmpty>No genre found.</CommandEmpty>
          <CommandGroup>
            <CommandItem
              v-for="genre in genres"
              :key="genre.genreid"
              :value="genre.name"
              @select="selectGenre(genre.name, genre.genreid)"
            >
              <CheckIcon
                  :class="cn(
                    'mr-2 h-4 w-4',
                    value === genre.name ? 'opacity-100' : 'opacity-0',
                  )"
                />
              {{ genre.name }}
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template>
