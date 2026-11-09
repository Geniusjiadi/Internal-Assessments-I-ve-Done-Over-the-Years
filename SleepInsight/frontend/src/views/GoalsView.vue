<script setup>
import { ref, onMounted } from "vue";
import { api } from "../api";
import GoalProgress from "../components/GoalProgress.vue";

const today = new Date().toISOString().slice(0, 10);
const goals = ref([]);
const editingId = ref(null);
const pendingDeleteId = ref(null);
const error   = ref("");
const message = ref("");

function blankGoal() {
  return {
    goal_type: "minimum_sleep_minutes",
    title: "Sleep at least 7h 30m",
    target_value: 450,
    target_time: "23:45",
    target_nights_per_week: 5,
    start_date: today,
    end_date: "",
    active: true,
    adaptive_enabled: true
  };
}
const form = ref(blankGoal());

async function load() {
  goals.value = await api.get("/api/goals");
}

async function save() {
  error.value = ""; message.value = "";
  const payload = { ...form.value, end_date: form.value.end_date || null };
  try {
    if (editingId.value) {
      await api.put(`/api/goals/${editingId.value}`, payload);
      message.value = "Goal updated.";
    } else {
      await api.post("/api/goals", payload);
      message.value = "Goal created.";
    }
    editingId.value = null;
    form.value = blankGoal();
    await load();
  } catch (err) { error.value = err.message; }
}

function edit(goal) {
  editingId.value = goal.id;
  form.value = {
    goal_type: goal.goal_type, title: goal.title,
    target_value: goal.target_value ?? 450,
    target_time: goal.target_time || "23:45",
    target_nights_per_week: goal.target_nights_per_week,
    start_date: goal.start_date, end_date: goal.end_date || "",
    active: goal.active, adaptive_enabled: goal.adaptive_enabled
  };
  pendingDeleteId.value = null;
}

function cancelEdit() {
  editingId.value = null;
  form.value = blankGoal();
}

function requestDelete(id) {
  pendingDeleteId.value = id;
}

function cancelDelete() {
  pendingDeleteId.value = null;
}

async function confirmDelete(id) {
  await api.del(`/api/goals/${id}`);
  pendingDeleteId.value = null;
  if (editingId.value === id) cancelEdit();
  await load();
}

onMounted(load);
</script>

<template>
  <section>
    <div class="page-header">
      <div class="page-header-row">
        <div>
          <div class="t-label" style="margin-bottom: 6px;">Measurable targets</div>
          <h1 class="t-page">Goals</h1>
        </div>
      </div>
    </div>

    <div v-if="message" class="alert success">{{ message }}</div>
    <div v-if="error"   class="alert error">{{ error }}</div>

    <div class="goals-layout">
      <!-- Form — no card wrapper -->
      <div class="goals-form-col">
        <div class="goals-form-head">
          <h2 class="t-section">{{ editingId ? "Edit goal" : "New goal" }}</h2>
          <button v-if="editingId" class="ghost sm" @click="cancelEdit">Cancel</button>
        </div>

        <form class="goals-form form-card" @submit.prevent="save">
          <label>Goal type
            <select v-model="form.goal_type">
              <option value="minimum_sleep_minutes">Minimum sleep duration</option>
              <option value="bedtime_before">Bedtime before</option>
              <option value="prebed_screen_max">Maximum pre-bed screen time</option>
              <option value="max_sleep_latency">Maximum sleep latency</option>
            </select>
          </label>

          <label>Title<input v-model="form.title" required /></label>

          <label v-if="form.goal_type === 'bedtime_before'">
            Target time<input type="time" v-model="form.target_time" required />
          </label>
          <label v-else>
            Target value (minutes)<input type="number" min="0" v-model.number="form.target_value" required />
          </label>

          <label>Target nights per week
            <input type="number" min="1" max="7" v-model.number="form.target_nights_per_week" required />
          </label>

          <div class="form-row-2">
            <label>Start date<input type="date" lang="en" v-model="form.start_date" required /></label>
            <label>End date <span class="t-caption">(optional)</span><input type="date" lang="en" v-model="form.end_date" /></label>
          </div>

          <label class="checkbox-label">
            <input type="checkbox" v-model="form.adaptive_enabled" />
            Enable adaptive target suggestions
          </label>

          <button type="submit">{{ editingId ? "Update goal" : "Create goal" }}</button>
        </form>
      </div>

      <!-- Active goals list -->
      <div class="goals-list-col">
        <h2 class="t-section" style="margin-bottom: var(--sp-2);">Current goals</h2>

        <div v-if="!goals.length" class="empty-state" style="padding: var(--sp-6) 0; text-align: left;">
          <div class="empty-state-title">No goals yet</div>
          <p class="empty-state-body" style="margin-left: 0;">
            Create a goal to track your sleep habits against a measurable target.
          </p>
        </div>

        <div v-else class="goals-list">
          <div v-for="goal in goals" :key="goal.id" class="goal-entry">
            <GoalProgress :goal="goal" />

            <div class="goal-actions">
              <!-- Inline delete confirm -->
              <template v-if="pendingDeleteId === goal.id">
                <span class="t-caption" style="color: var(--danger);">Delete this goal?</span>
                <button class="danger sm" @click="confirmDelete(goal.id)">Yes, delete</button>
                <button class="ghost sm"  @click="cancelDelete">Cancel</button>
              </template>
              <template v-else>
                <button class="secondary sm" @click="edit(goal)">Edit</button>
                <button class="ghost sm"     @click="requestDelete(goal.id)">Delete</button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.goals-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-8);
  align-items: start;
}

.goals-form-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--sp-3);
  margin-bottom: var(--sp-5);
}

.goals-form {
  display: grid;
  gap: var(--sp-4);
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-3);
}

.goals-list {
  display: grid;
  gap: 0;
}

.goal-entry {
  border-bottom: 1px solid var(--border);
  padding-bottom: var(--sp-3);
  margin-bottom: var(--sp-1);
}
.goal-entry:last-child { border-bottom: none; }

.goal-actions {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-2) 0 var(--sp-3);
}

@media (max-width: 860px) {
  .goals-layout {
    grid-template-columns: 1fr;
    gap: var(--sp-7);
  }
  .form-row-2 { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 480px) {
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>
