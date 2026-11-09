<template>
  <header class="topbar">
    <RouterLink to="/" class="brand">SleepInsight</RouterLink>
    <nav class="nav-links" aria-label="Main navigation">
      <RouterLink to="/">Dashboard</RouterLink>
      <RouterLink to="/trends">Trends</RouterLink>
      <RouterLink to="/insights">Insights</RouterLink>
      <RouterLink to="/recommendations">Recommendations</RouterLink>
      <RouterLink to="/goals">Goals</RouterLink>
    </nav>
    <RouterLink to="/entry" class="nav-cta">Log today</RouterLink>
  </header>
</template>
