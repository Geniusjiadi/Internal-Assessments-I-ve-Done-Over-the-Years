<script setup>
import { ref, onMounted } from "vue";
import { api } from "../api";
import StatCard from "../components/StatCard.vue";

const data  = ref(null);
const error = ref("");

onMounted(async () => {
  try { data.value = await api.get("/api/analytics/insights"); }
  catch (err) { error.value = err.message; }
});

function rhoDisplay(rho) {
  if (rho == null) return "—";
  return (rho >= 0 ? "+" : "") + rho;
}

function strengthClass(s) {
  if (!s) return "";
  if (s.includes("strong")) return "c-accent";
  if (s.includes("moderate")) return "c-secondary";
  return "c-muted";
}

function confidenceBadgeClass(c) {
  if (c === "high")     return "success";
  if (c === "moderate") return "accent";
  if (c === "low")      return "warning";
  return "";
}
</script>

<template>
  <section>
    <div class="page-header">
      <div class="page-header-row">
        <div>
          <div class="t-label" style="margin-bottom: 6px;">Pattern analysis</div>
          <h1 class="t-page">Insights</h1>
          <p class="page-subtitle">Associations are descriptive — they do not prove causation.</p>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert error">{{ error }}</div>
    <div v-else-if="!data" class="empty-state"><div class="empty-state-title">Loading…</div></div>

    <template v-else>
      <!-- Metrics strip — no cards, inline data -->
      <div class="insights-strip">
        <StatCard
          label="Regularity score"
          :value="data.regularity.regularity_score ?? '—'"
          :detail="`Bedtime SD: ${data.regularity.bedtime_sd ?? '—'} min`"
          size="md"
        />
        <div class="strip-divider"></div>
        <StatCard
          label="Social jet lag"
          :value="data.weekday_weekend.social_jetlag_minutes != null
            ? `${data.weekday_weekend.social_jetlag_minutes} min`
            : '—'"
          detail="Weekday vs. weekend midpoint shift"
          size="md"
        />
        <div class="strip-divider"></div>
        <StatCard
          label="Records analysed"
          :value="data.record_count"
          detail="Total nights logged"
          size="md"
        />
      </div>

      <div class="divider"></div>

      <!-- Factor associations — primary table -->
      <div class="insights-section">
        <h2 class="t-section" style="margin-bottom: var(--sp-4);">Factor associations</h2>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Relationship</th>
                <th>Spearman ρ</th>
                <th>n</th>
                <th>Strength</th>
                <th>Confidence</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in data.correlations" :key="item.label">
                <td class="td-primary">{{ item.label }}</td>
                <td class="td-mono" :class="item.rho != null ? 'td-primary' : 'c-muted'">
                  {{ rhoDisplay(item.rho) }}
                </td>
                <td class="td-mono c-secondary">{{ item.sample_size }}</td>
                <td :class="strengthClass(item.strength)">{{ item.strength || "—" }}</td>
                <td>
                  <span class="badge" :class="confidenceBadgeClass(item.confidence)">
                    {{ item.confidence }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="divider"></div>

      <!-- Detected patterns -->
      <div class="insights-section">
        <h2 class="t-section" style="margin-bottom: var(--sp-2);">Detected patterns</h2>
        <p class="t-caption" style="margin-bottom: var(--sp-5);">
          Rules fire when behaviour crosses a defined threshold.
        </p>

        <div v-if="!data.patterns.length" class="empty-state" style="padding: var(--sp-5) 0; text-align: left;">
          <div class="empty-state-title">No patterns detected</div>
          <p class="empty-state-body" style="margin-left: 0;">
            None of the pattern thresholds have been crossed yet. Keep logging to build up a fuller picture.
          </p>
        </div>

        <div v-else class="pattern-list">
          <div v-for="pattern in data.patterns" :key="pattern.rule_id" class="pattern-item">
            <div class="pattern-head">
              <span class="pattern-title">{{ pattern.title }}</span>
              <span class="badge" :class="confidenceBadgeClass(pattern.confidence)">
                {{ pattern.confidence }}
              </span>
            </div>
            <p class="t-secondary">{{ pattern.reason }}</p>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped>
/* Inline metrics strip */
.insights-strip {
  display: flex;
  gap: var(--sp-7);
  align-items: start;
  margin-bottom: var(--sp-6);
}

.strip-divider {
  width: 1px;
  background: var(--border);
  align-self: stretch;
  flex-shrink: 0;
}

.insights-section {
  margin-bottom: var(--sp-2);
}

/* Pattern list */
.pattern-list {
  display: grid;
  gap: 0;
}

.pattern-item {
  padding: var(--sp-4) 0;
  border-bottom: 1px solid var(--border);
}
.pattern-item:last-child { border-bottom: none; }

.pattern-head {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  margin-bottom: var(--sp-2);
}

.pattern-title {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
}

@media (max-width: 680px) {
  .insights-strip {
    flex-direction: column;
    gap: var(--sp-5);
  }
  .strip-divider {
    width: 100%;
    height: 1px;
    align-self: auto;
  }
}
</style>
