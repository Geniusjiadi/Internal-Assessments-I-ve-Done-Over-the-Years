<script setup>
import { ref, onMounted, watch } from "vue";
import { api } from "../api";
import TrendChart from "../components/TrendChart.vue";

const days   = ref(30);
const series = ref([]);
const error  = ref("");

async function load() {
  try {
    error.value = "";
    const data = await api.get(`/api/analytics/trends?days=${days.value}`);
    series.value = data.series;
  } catch (err) { error.value = err.message; }
}
watch(days, load);
onMounted(load);
</script>

<template>
  <section>
    <div class="page-header">
      <div class="page-header-row">
        <div>
          <div class="t-label" style="margin-bottom: 6px;">Historical data</div>
          <h1 class="t-page">Trends</h1>
        </div>
        <div class="segmented">
          <button
            v-for="option in [7, 30, 90]"
            :key="option"
            :class="{ active: days === option }"
            @click="days = option"
          >{{ option }}d</button>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert error">{{ error }}</div>

    <div v-else class="trends-stack">
      <div class="trend-block">
        <div class="trend-block-head">
          <h2 class="t-section">Sleep duration</h2>
          <span class="t-caption">minutes</span>
        </div>
        <TrendChart :series="series" metric="duration_minutes" title="Sleep duration (min)" />
      </div>

      <div class="divider"></div>

      <div class="trend-block">
        <div class="trend-block-head">
          <h2 class="t-section">Sleep quality</h2>
          <span class="t-caption">1–5 scale</span>
        </div>
        <TrendChart :series="series" metric="quality" title="Perceived quality" />
      </div>

      <div class="divider"></div>

      <div class="trend-block">
        <div class="trend-block-head">
          <h2 class="t-section">Sleep score</h2>
          <span class="t-caption">0–100 weighted composite</span>
        </div>
        <TrendChart :series="series" metric="sleep_score" title="Sleep score" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.trends-stack {
  display: grid;
  gap: 0;
}

.trend-block {
  padding: var(--sp-5) 0;
}

.trend-block-head {
  display: flex;
  align-items: baseline;
  gap: var(--sp-3);
  margin-bottom: var(--sp-4);
}

@media (max-width: 560px) {
  .trend-block { padding: var(--sp-4) 0; }
}
</style>
