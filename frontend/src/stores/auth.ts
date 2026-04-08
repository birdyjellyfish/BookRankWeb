import type { User } from "@/components/types";
import { defineStore } from "pinia";
import { getCommentRange } from "typescript";
import { ref } from "vue";
import type { Router } from "vue-router";

// adapted from Tom Dekan Vue auth tutorial

const url = import.meta.env.VITE_API_URL

export const useAuthStore = defineStore('auth', () => {
  const storedState = localStorage.getItem('authState');

  const user = ref<User | null>(storedState ? JSON.parse(storedState).user : null);
  const isAuthenticated = ref(storedState ? JSON.parse(storedState).isAuthenticated : false);

  async function setCSRFToken(): Promise<void> {
    await fetch(`${url}/set-csrf-token/`, {
      method: 'GET',
      credentials: 'include',
    })
  }

  async function login(
    username: string,
    password: string,
    router: Router | null = null
  ): Promise<void> {
    const response = await fetch(`${url}/users/login/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      credentials: 'include',
      body: JSON.stringify({
        username,
        password
      })
    })

    const data = await response.json();

    if (data.success) {
      fetchUser();
      isAuthenticated.value = true;
      saveState();

      // route to home page if router is supplied
      if (router) {
        await router.push({
          name: 'home',
        })
      }
    } else {
      user.value = null;
      isAuthenticated.value = false;

      saveState();
    }
  }

  async function logout(router: Router | null = null): Promise<void> {
    try {
      const response = await fetch(`${url}/users/logout/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include',
      })

      if (response.ok) {
        user.value = null;
        isAuthenticated.value = false;
        saveState();
        if (router) {
          await router.push({
            name: "home",
          })
        }
      }
    } catch (error) {
      console.error('Logout failed', error);
    }
  }

  // help populate user store
  async function fetchUser(): Promise<void> {
    try {
      const response = await fetch(`${url}/users/`, {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
      })

      if (response.ok) {
        const data = await response.json();
        user.value = data;
        isAuthenticated.value = true;
      } else {
        user.value = null;
        isAuthenticated.value = false;
      }
    } catch (error) {
      console.error('Failed to fetch user', error);
      user.value = null;
      isAuthenticated.value = null;
    }
    saveState();
  }

  function saveState() {
    // save user info and isAuthenticated in localStorage
    localStorage.setItem(
      'authState',
      JSON.stringify({
        user: user.value,
        isAuthenticated: isAuthenticated.value,
      })
    )
  }

  return {
    user,
    isAuthenticated,
    setCSRFToken,
    login,
    logout,
    fetchUser,
    saveState,
  }
})

export function getCSRFToken() {
  /*
    We get the CSRF token from the cookie to include in our requests.
    This is necessary for CSRF protection in Django.
     */
  const name = 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  if (cookieValue === null) {
    throw 'Missing CSRF cookie.'
  }
  return cookieValue
}