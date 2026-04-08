<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth';
import { computed, onMounted } from 'vue';
import router from './router';

import 'vue-sonner/style.css'
import { Toaster } from '@/components/ui/sonner'

import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
  NavigationMenuViewport,
} from '@/components/ui/navigation-menu'

import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'

import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import { BookSearch, BookSearchIcon, CircleUserRound, Menu, Router } from 'lucide-vue-next';
import ModeToggle from './components/ModeToggle.vue';
import LoginView from './components/LoginView.vue';
import { ref } from 'vue';
import SignupView from './components/SignupView.vue';


const authStore = useAuthStore();

const openSignin = ref(false);
const openSignup = ref(false);
const openDialog = ref(false);

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await authStore.fetchUser();
  }
})

async function logout() {
  await authStore.logout(router);
}
</script>

<template>
  <body class="flex flex-col min-h-screen">
  <nav class="sticky top-0 z-50 backdrop-blur-sm flex items-center p-4">
    <NavigationMenu>
      <NavigationMenuLink>
        <RouterLink to="/" class="text-lg font-bold flex gap-1 items-center">
          <BookSearch />
          BookRank
        </RouterLink>
      </NavigationMenuLink>
    </NavigationMenu>

    <NavigationMenu class="ml-auto">
      <NavigationMenuList class="hidden md:flex">
        <NavigationMenuItem>
          <NavigationMenuLink>
            <RouterLink to="/">Home</RouterLink>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuLink>
            <RouterLink to="/about">About</RouterLink>
          </NavigationMenuLink>
        </NavigationMenuItem>

        
        <NavigationMenuItem>
          <NavigationMenuTrigger><CircleUserRound /></NavigationMenuTrigger>
          <NavigationMenuContent v-if="!authStore.isAuthenticated">
            <ul class="grid w-50 gap-4">
              <li>
                <NavigationMenuLink as-child>
                  <a @click="openSignin = true; openDialog = true">
                    Sign In
                  </a>
                </NavigationMenuLink>
                <NavigationMenuLink as-child>
                  <a @click="openSignup = true; openDialog = true; openSignin = false">
                    Sign Up
                  </a>
                </NavigationMenuLink>
              </li>
            </ul>
          </NavigationMenuContent>
          <NavigationMenuContent v-else>
            <ul class="grid w-50 gap-4">
              <li>
                <NavigationMenuLink>
                  <RouterLink to="/user">{{ authStore.user?.username }}</RouterLink>
                </NavigationMenuLink>
                <NavigationMenuLink @click="logout">
                  <a>Sign Out</a>
                </NavigationMenuLink>
              </li>
            </ul>
          </NavigationMenuContent>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <ModeToggle />
        </NavigationMenuItem>

      </NavigationMenuList>

      <NavigationMenuList class="md:hidden">
        <NavigationMenuItem>
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button variant="ghost">
                <Menu></Menu>
              </Button>
            </DropdownMenuTrigger>

            <DropdownMenuContent align="end">
              <DropdownMenuGroup>
                <DropdownMenuItem>
                  <RouterLink to="/">Home</RouterLink>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <RouterLink to="/about">About</RouterLink>
                </DropdownMenuItem>
              </DropdownMenuGroup>

              <DropdownMenuSeparator>
              </DropdownMenuSeparator>

              <DropdownMenuGroup v-if="!authStore.isAuthenticated">
                <DropdownMenuLabel>Account</DropdownMenuLabel>
                <DropdownMenuItem
                   @click="openSignin = true; openDialog = true; openSignup = false">
                  Sign In
                </DropdownMenuItem>
                <DropdownMenuItem
                  @click="openSignup = true; openDialog = true; openSignin = false">
                  Sign Up
                </DropdownMenuItem>
              </DropdownMenuGroup>
              <DropdownMenuGroup v-else>
                <DropdownMenuLabel>Account</DropdownMenuLabel>
                <DropdownMenuItem>
                  <RouterLink to="/user">{{ authStore.user?.username }}</RouterLink>
                </DropdownMenuItem>
                <DropdownMenuItem @click="logout">
                  Sign Out
                </DropdownMenuItem>
              </DropdownMenuGroup>
            </DropdownMenuContent>
          </DropdownMenu>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <ModeToggle />
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  </nav>

  <RouterView class="grow"/>
  <Dialog v-model:open="openDialog">
    <LoginView
      v-if="openSignin"
      v-model:dialog="openDialog"
      v-model:signin="openSignin" />
    <SignupView
      v-else
      v-model:dialog="openDialog"
      v-model:signin="openSignin"
      v-model:signup="openSignup" />
  </Dialog>
  

  <Toaster position="top-center"/>

  <footer class="mt-20 p-10 pb-30 border-t bg-secondary">
    <div class="flex flex-col md:flex-row gap-10">
      <div class="flex-1">
        <div class="text-lg font-bold flex items-center gap-1">
          <BookSearch></BookSearch>
          BookRank
        </div>
        <div>
          Ultimate book recommendation website
        </div>
      </div>

      <div class="flex-2 grid">
        <span class="font-semibold mb-2">Sitemap</span>
        <RouterLink to="/">
          Home
        </RouterLink>
        <RouterLink to="/about" >
          About
        </RouterLink>
        <RouterLink to="/user" >
          Account
        </RouterLink>
        
      </div>
    </div>
  </footer>
  </body>
</template>

<style scoped>

</style>
