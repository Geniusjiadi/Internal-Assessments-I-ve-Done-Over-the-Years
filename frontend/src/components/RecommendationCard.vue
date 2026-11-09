<script setup>
import { ref } from "vue";

const props = defineProps({ recommendation: Object, rank: Number });
const open = ref(false);

function confidenceClass(c) {
  if (!c) return "";
  if (c === "high")     return "success";
  if (c === "moderate") return "accent";
  if (c === "low")      return "warning";
  return "";
}

function rankLabel(r) {
  if (r === 1) return "Top priority";
  if (r === 2) return "Worth considering";
  return "When you're ready";
}
</script>

<template>
  <article v-if="recommendation" class="rec-card">
    <div class="rec-header">
      <div class="rec-meta">
        <span class="t-label">{{ rank ? rankLabel(rank) : "Recommendation" }}</span>
        <span class="badge" :class="confidenceClass(recommendation.confidence)">
          {{ recommendation.confidence }} confidence
        </span>
      </div>
      <h3 class="rec-title">{{ recommendation.title }}</h3>
    </div>

    <p class="rec-action">{{ recommendation.action }}</p>

    <button
      class="ghost rec-toggle"
      :aria-expanded="open"
      @click="open = !open"
    >
      {{ open ? "Hide explanation" : "Why am I seeing this?" }}
      <svg
        class="rec-toggle-icon"
        :class="{ open }"
        width="12" height="12" viewBox="0 0 12 12" fill="none"
        aria-hidden="true"
      >
        <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <div v-if="open" class="rec-reason">
      <p class="t-secondary">{{ recommendation.reason }}</p>
    </div>
  </article>
</template>

<style scoped>
.rec-card {
  padding: var(--sp-5) 0;
  border-bottom: 1px solid var(--border);
}
.rec-card:last-child { border-bottom: none; }

.rec-header { margin-bottom: var(--sp-3); }

.rec-meta {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  margin-bottom: var(--sp-2);
}

.rec-title {
  font-size: var(--text-md);
  font-weight: 600;
  letter-spacing: -0.01em;
  line-height: 1.3;
  color: var(--text-primary);
  margin: 0;
}

.rec-action {
  font-size: var(--text-base);
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 var(--sp-3);
}

.rec-toggle {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-1);
  padding: 0;
  font-size: var(--text-xs);
  font-weight: 500;
  color: var(--text-muted);
  background: none;
  border: none;
  cursor: pointer;
  transition: color var(--dur-fast) var(--ease);
}
.rec-toggle:hover { color: var(--text-primary); background: none; }
.rec-toggle:active { transform: none; }

.rec-toggle-icon {
  transition: transform var(--dur-fast) var(--ease);
}
.rec-toggle-icon.open { transform: rotate(180deg); }

.rec-reason {
  margin-top: var(--sp-3);
  padding: var(--sp-3) var(--sp-4);
  background: var(--gray-1);
  border-radius: var(--r-md);
  animation: fadeDown var(--dur-normal) var(--ease-out);
}

@keyframes fadeDown {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
