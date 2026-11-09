<script setup>
import AppNav from "./components/AppNav.vue";
</script>

<template>
  <div class="app-shell">
    <AppNav />
    <main class="page-shell">
      <router-view />
    </main>
  </div>
</template>
