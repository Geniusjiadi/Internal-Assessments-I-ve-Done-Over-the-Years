<script setup>
import { ref, onMounted } from "vue";
import { api } from "../api";
import RecommendationCard from "../components/RecommendationCard.vue";

const recommendations = ref([]);
const error = ref("");

onMounted(async () => {
  try { recommendations.value = await api.get("/api/recommendations"); }
  catch (err) { error.value = err.message; }
});
</script>

<template>
  <section>
    <div class="page-header">
      <div class="page-header-row">
        <div>
          <div class="t-label" style="margin-bottom: 6px;">Rule-based decision support</div>
          <h1 class="t-page">Recommendations</h1>
          <p class="page-subtitle">
            Ranked by severity, evidence strength, confidence, and goal relevance.
            Not medical advice.
          </p>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert error">{{ error }}</div>

    <div v-if="recommendations.length">
      <RecommendationCard
        v-for="(item, i) in recommendations"
        :key="item.rule_id"
        :recommendation="item"
        :rank="i + 1"
      />
    </div>

    <div v-else-if="!error" class="empty-state" style="padding: var(--sp-7) 0; text-align: left;">
      <div class="empty-state-title">Nothing to flag right now</div>
      <p class="empty-state-body" style="margin-left: 0;">
        Recommendations appear when patterns in your data cross a meaningful threshold.
        Log a couple more weeks of sleep and lifestyle data to see results.
      </p>
    </div>
  </section>
</template>
