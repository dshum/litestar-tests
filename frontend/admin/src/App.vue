<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div
      class="h-screen bg-cover bg-no-repeat bg-center bg-[url('/src/assets/bg.jpg')]">
    <div class="container mx-auto">
      <div class="flex h-screen">
        <div class="m-auto flex w-full lg:w-1/2 2xl:w-1/3 justify-center">
          <div class="w-full backdrop-blur-xl bg-white/35 rounded-xl shadow-2xl">
            <div class="text-lg py-2 px-4">
              <form>
                <div class="my-4">
                  <label class="block mb-1">E-mail</label>
                  <div>
                    <input type="email"
                           class="w-full bg-transparent border-b-2 border-slate-500 focus:outline-none focus:shadow-outline focus:border-slate-700 py-2 px-0 placeholder-slate-600"
                           placeholder="Enter your e-mail">
                  </div>
                </div>
                <div class="my-4">
                  <label class="block mb-1">Password</label>
                  <div>
                    <input type="password"
                           class="w-full bg-transparent border-b-2 border-slate-500 focus:outline-none focus:shadow-outline focus:border-slate-700 py-2 px-0 placeholder-slate-600"
                           placeholder="Enter password">
                  </div>
                </div>
                <div class="my-6">
                  <button class="w-full shadow rounded-lg py-2 px-4 bg-sky-700 text-white">Sign In</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
