<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue';
import { CircleQuestionMark } from 'lucide-vue-next';
</script>

<template>
  <div class="h-full flex flex-col items-center justify-center gap-4">
    <h1 class="flex items-center">
      <div class="text-8xl font-semibold">4</div>
      <div><CircleQuestionMark :size="64" /></div>
      <div class="text-8xl font-semibold">4</div>
    </h1>

    <div class="flex flex-col items-center">
      <h1 class="font-semibold text-2xl">
      Page Not Found
      </h1>
      <h2>
        We couldn't find what you were looking for.
      </h2>
    </div>
    <div>
      <Button variant="secondary">
        <RouterLink to="/">Back to Home</RouterLink>
      </Button>
    </div>
  </div>
</template>