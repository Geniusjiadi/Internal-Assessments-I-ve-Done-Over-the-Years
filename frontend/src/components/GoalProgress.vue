<script setup>
defineProps({ goal: Object });
</script>

<template>
  <div v-if="goal" class="goal-item">
    <div class="row-between goal-top">
      <span class="goal-title">{{ goal.title }}</span>
      <span class="t-metric-sm goal-pct">{{ goal.progress?.completion_percent ?? 0 }}%</span>
    </div>

    <div class="progress-track" :aria-label="`Goal progress: ${goal.progress?.completion_percent ?? 0}%`" role="progressbar"
         :aria-valuenow="Math.min(100, goal.progress?.completion_percent || 0)"
         aria-valuemin="0" aria-valuemax="100">
      <div
        class="progress-fill"
        :style="{ width: `${Math.min(100, goal.progress?.completion_percent || 0)}%` }"
      ></div>
    </div>

    <div class="goal-meta">
      <span class="t-caption">
        {{ goal.progress?.met_nights ?? 0 }} / {{ goal.progress?.target_nights ?? 0 }} target nights
      </span>
      <span v-if="goal.adaptive_suggestion?.suggested_target != null" class="t-caption goal-adaptive">
        Next target: {{ goal.adaptive_suggestion.suggested_target }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.goal-item {
  padding: var(--sp-4) 0;
  border-bottom: 1px solid var(--border);
}
.goal-item:last-child { border-bottom: none; }

.goal-top { margin-bottom: var(--sp-3); align-items: baseline; }

.goal-title {
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.4;
}

.goal-pct {
  color: var(--accent);
  flex-shrink: 0;
}

.progress-track { margin-bottom: var(--sp-2); }

.goal-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--sp-3);
}

.goal-adaptive {
  color: var(--accent-muted);
  font-weight: 500;
}
</style>
