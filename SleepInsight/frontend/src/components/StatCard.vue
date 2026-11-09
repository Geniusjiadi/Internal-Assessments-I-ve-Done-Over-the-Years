<script setup>
defineProps({
  label: String,
  value: [String, Number],
  detail: String,
  size: {         // "lg" | "md" | "sm"
    type: String,
    default: "md"
  },
  accent: Boolean
});
</script>

<template>
  <div class="stat-item">
    <div class="t-label">{{ label }}</div>
    <div
      class="stat-value"
      :class="[`t-metric-${size}`, accent ? 'c-accent' : '']"
    >{{ value ?? "—" }}</div>
    <div v-if="detail" class="t-caption stat-detail">{{ detail }}</div>
  </div>
</template>

<style scoped>
.stat-item {
  display: grid;
  gap: 4px;
}
.stat-value {
  margin: 2px 0;
}
.stat-detail {
  margin-top: 1px;
}
</style>
