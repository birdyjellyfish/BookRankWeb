<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue';
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';

import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSet,
} from '@/components/ui/field'
import { Input } from '@/components/ui/input'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import FieldError from '@/components/ui/field/FieldError.vue';
import Spinner from './ui/spinner/Spinner.vue';
import { Check } from 'lucide-vue-next';

const authStore = useAuthStore();
const username = ref<string>("");
const password = ref<string>("");
const error = ref<string>("");
const success = ref<string>("");
const loading = ref(false);

async function login() {
  loading.value = true;
  await authStore.login(username.value, password.value);
  if (!authStore.isAuthenticated) {
    error.value = "Incorrect login credentials."
  } else {
    success.value = "Successfully logged in."
    setTimeout(() => {
      openSignin.value = false;
      openDialog.value = false;
    }, 500)
  }

  loading.value = false;
}

function resetError() {
  error.value = ""
}

const openSignin = defineModel<boolean>("signin");
const openDialog = defineModel<boolean>("dialog");

</script>

<template>
  <DialogContent class="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Sign In</DialogTitle>
      <DialogDescription class="min-h-10">
        <FieldError>
          {{ error }}
        </FieldError>
        <div>
          {{ success }}
        </div>
      </DialogDescription>
    </DialogHeader>
    <div class="flex items-center justify-center">
      <form class="w-full max-w-md" @submit.prevent="login">
        <FieldSet>
          <FieldGroup>
            <Field>
              <FieldLabel for="username">
                Username
              </FieldLabel>
              <Input
                v-model="username"
                id="username"
                type="text"
                required
                placeholder="Enter username..."
                @update:model-value="resetError" />
            </Field>
            
            <Field>
              <FieldLabel for="password">
                Password
              </FieldLabel>
              <Input
                v-model="password"
                id="password"
                type="password"
                placeholder="Enter password..."
                required
                @update:model-value="resetError" />
            </Field>

            <Field>
              <Button disabled v-if="success"><Check /></Button>
              <Button type="submit" v-else-if="!loading">Sign In</Button>
              <Button disabled v-else-if="loading"><Spinner /></Button>
            </Field>
          </FieldGroup>
        </FieldSet>
      </form>
    </div>
  </DialogContent>
</template> 