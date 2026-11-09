<script setup>
import { ref, onMounted } from "vue";
import { api } from "../api";
import StatCard from "../components/StatCard.vue";
import RecommendationCard from "../components/RecommendationCard.vue";
import GoalProgress from "../components/GoalProgress.vue";

const data = ref(null);
const error = ref("");

function hours(minutes) {
  if (minutes == null) return "—";
  const h = Math.floor(minutes / 60);
  const m = Math.round(minutes % 60);
  return m > 0 ? `${h}h ${m}m` : `${h}h`;
}

async function load() {
  try {
    data.value = await api.get("/api/dashboard");
  } catch (err) {
    error.value = err.message;
  }
}
onMounted(load);
</script>

<template>
  <section>
    <!-- Header -->
    <div class="page-header">
      <div class="page-header-row">
        <div>
          <div class="t-label" style="margin-bottom: 6px;">Overview</div>
          <h1 class="t-page">Dashboard</h1>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert error">{{ error }}</div>

    <div v-else-if="!data" class="empty-state">
      <div class="empty-state-title">Loading…</div>
    </div>

    <template v-else>
      <!-- Primary metric row -->
      <div class="dash-metrics">
        <div class="dash-primary">
          <StatCard
            label="Sleep score"
            :value="data.sleep_score?.score ?? '—'"
            detail="Weighted composite 0–100"
            size="lg"
            accent
          />
        </div>
        <div class="dash-secondary">
          <StatCard
            label="Last night"
            :value="hours(data.latest?.duration_minutes)"
            :detail="data.latest?.sleep_date || 'No record yet'"
          />
          <StatCard
            label="Regularity"
            :value="data.regularity?.regularity_score ?? '—'"
            detail="Bedtime consistency 0–100"
          />
          <StatCard
            label="Tracked nights"
            :value="data.record_count"
            detail="Stored locally"
          />
        </div>
      </div>

      <div class="divider"></div>

      <!-- Content panels -->
      <div class="dash-panels">
        <!-- Recommendation -->
        <div class="dash-panel">
          <div class="dash-panel-head">
            <h2 class="t-section">Top recommendation</h2>
          </div>
          <div v-if="data.top_recommendation">
            <RecommendationCard :recommendation="data.top_recommendation" :rank="1" />
          </div>
          <div v-else class="empty-state" style="padding: var(--sp-6) 0;">
            <div class="empty-state-title">Nothing to flag yet</div>
            <p class="empty-state-body">Log a couple of weeks of sleep to start seeing personalised patterns.</p>
          </div>
        </div>

        <!-- Goals -->
        <div class="dash-panel">
          <div class="dash-panel-head">
            <h2 class="t-section">Goals</h2>
          </div>
          <div v-if="data.goals && data.goals.length">
            <GoalProgress v-for="goal in data.goals" :key="goal.id" :goal="goal" />
          </div>
          <div v-else class="empty-state" style="padding: var(--sp-6) 0;">
            <div class="empty-state-title">No active goals</div>
            <p class="empty-state-body">
              <RouterLink to="/goals" style="color: var(--accent);">Set a sleep goal</RouterLink>
              to start tracking your progress.
            </p>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped>
/* Primary metric + secondary row */
.dash-metrics {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: var(--sp-8);
  align-items: start;
  margin-bottom: var(--sp-6);
}

.dash-primary {
  padding-right: var(--sp-8);
  border-right: 1px solid var(--border);
}

.dash-secondary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-6);
  align-items: start;
}

/* Two-column content panels */
.dash-panels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-8);
  align-items: start;
}

.dash-panel-head {
  margin-bottom: var(--sp-2);
}

@media (max-width: 860px) {
  .dash-metrics {
    grid-template-columns: 1fr;
    gap: var(--sp-6);
  }
  .dash-primary {
    padding-right: 0;
    border-right: none;
    border-bottom: 1px solid var(--border);
    padding-bottom: var(--sp-5);
  }
  .dash-secondary {
    grid-template-columns: repeat(3, 1fr);
  }
  .dash-panels {
    grid-template-columns: 1fr;
    gap: var(--sp-6);
  }
}

@media (max-width: 560px) {
  .dash-secondary {
    grid-template-columns: 1fr 1fr;
    gap: var(--sp-5);
  }
}
</style>
