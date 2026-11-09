<script setup>
import { ref, onMounted } from "vue";
import { api } from "../api";

const today = new Date().toISOString().slice(0, 10);

const sleepForm = ref({
  sleep_date: today, bedtime: "23:30", wake_time: "07:00",
  latency_minutes: 15, awakenings: 0, quality: 4, notes: ""
});
const caffeineForm = ref({ event_date: today, time: "09:00", amount_mg: 80, beverage_type: "Coffee" });
const exerciseForm = ref({ event_date: today, time: "17:30", duration_minutes: 30, intensity: "Moderate" });
const screenForm   = ref({ event_date: today, total_minutes: 300, pre_bed_minutes: 45 });

const sleepRecords = ref([]);
const editingId    = ref(null);
const pendingDeleteId = ref(null);  // inline confirm state
const message      = ref("");
const error        = ref("");
const activeTab    = ref("caffeine"); // "caffeine" | "exercise" | "screen"

async function loadSleep() {
  sleepRecords.value = (await api.get("/api/sleep")).slice().reverse();
}

async function saveSleep() {
  error.value = ""; message.value = "";
  try {
    if (editingId.value) {
      await api.put(`/api/sleep/${editingId.value}`, sleepForm.value);
      message.value = "Sleep record updated.";
    } else {
      await api.post("/api/sleep", sleepForm.value);
      message.value = "Sleep record saved.";
    }
    editingId.value = null;
    sleepForm.value = { sleep_date: today, bedtime: "23:30", wake_time: "07:00", latency_minutes: 15, awakenings: 0, quality: 4, notes: "" };
    await loadSleep();
  } catch (err) { error.value = err.message; }
}

function editSleep(record) {
  editingId.value = record.id;
  sleepForm.value = {
    sleep_date: record.sleep_date, bedtime: record.bedtime,
    wake_time: record.wake_time, latency_minutes: record.latency_minutes,
    awakenings: record.awakenings, quality: record.quality,
    notes: record.notes || ""
  };
  pendingDeleteId.value = null;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function cancelEdit() {
  editingId.value = null;
  sleepForm.value = { sleep_date: today, bedtime: "23:30", wake_time: "07:00", latency_minutes: 15, awakenings: 0, quality: 4, notes: "" };
}

function requestDelete(id) {
  pendingDeleteId.value = id;
}

function cancelDelete() {
  pendingDeleteId.value = null;
}

async function confirmDelete(id) {
  await api.del(`/api/sleep/${id}`);
  pendingDeleteId.value = null;
  if (editingId.value === id) cancelEdit();
  await loadSleep();
}

async function submitLifestyle(path, form, success) {
  error.value = ""; message.value = "";
  try {
    await api.post(path, form.value);
    message.value = success;
  } catch (err) { error.value = err.message; }
}

function hours(minutes) {
  if (minutes == null) return "—";
  return `${Math.floor(minutes / 60)}h ${minutes % 60}m`;
}

onMounted(loadSleep);
</script>

<template>
  <section>
    <div class="page-header">
      <div class="page-header-row">
        <div>
          <div class="t-label" style="margin-bottom: 6px;">Data collection</div>
          <h1 class="t-page">Daily Entry</h1>
        </div>
      </div>
    </div>

    <div v-if="message" class="alert success">{{ message }}</div>
    <div v-if="error"   class="alert error">{{ error }}</div>

    <!-- Primary: Sleep form -->
    <div class="entry-layout">
      <div class="entry-main">
        <div class="entry-form-head">
          <h2 class="t-section">{{ editingId ? "Edit sleep record" : "Sleep record" }}</h2>
          <button v-if="editingId" class="ghost sm" @click="cancelEdit">Cancel edit</button>
        </div>

        <form class="sleep-form" @submit.prevent="saveSleep">
          <div class="form-row-2">
            <label class="field">
              <span>Date</span>
              <input type="date" lang="en" v-model="sleepForm.sleep_date" required />
            </label>
          </div>

          <div class="form-row-2">
            <label class="field">
              <span>Bedtime</span>
              <input type="time" v-model="sleepForm.bedtime" required />
            </label>
            <label class="field">
              <span>Wake time</span>
              <input type="time" v-model="sleepForm.wake_time" required />
            </label>
          </div>

          <div class="form-row-2">
            <label class="field">
              <span>Sleep latency (min)</span>
              <input type="number" min="0" max="360" v-model.number="sleepForm.latency_minutes" required />
            </label>
            <label class="field">
              <span>Awakenings</span>
              <input type="number" min="0" v-model.number="sleepForm.awakenings" required />
            </label>
          </div>

          <label class="field">
            <span>Perceived quality (1–5)</span>
            <input type="number" min="1" max="5" v-model.number="sleepForm.quality" required />
          </label>

          <label class="field">
            <span>Notes <span class="t-caption">(optional)</span></span>
            <textarea v-model="sleepForm.notes" rows="3" placeholder="Anything worth noting…"></textarea>
          </label>

          <div class="row" style="margin-top: var(--sp-2);">
            <button type="submit">{{ editingId ? "Update record" : "Save record" }}</button>
          </div>
        </form>
      </div>

      <!-- Secondary: Lifestyle inputs -->
      <div class="entry-side">
        <h2 class="t-section" style="margin-bottom: var(--sp-4);">Lifestyle factors</h2>

        <!-- Tabs -->
        <div class="lifestyle-tabs" role="tablist">
          <button
            v-for="tab in ['caffeine', 'exercise', 'screen']"
            :key="tab"
            role="tab"
            :aria-selected="activeTab === tab"
            :class="{ active: activeTab === tab }"
            class="lifestyle-tab"
            @click="activeTab = tab"
          >{{ tab.charAt(0).toUpperCase() + tab.slice(1) }}</button>
        </div>

        <!-- Caffeine -->
        <form
          v-show="activeTab === 'caffeine'"
          class="lifestyle-form form-card"
          @submit.prevent="submitLifestyle('/api/caffeine', caffeineForm, 'Caffeine event saved.')"
        >
          <label>Date<input type="date" lang="en" v-model="caffeineForm.event_date" required /></label>
          <label>Time<input type="time" v-model="caffeineForm.time" required /></label>
          <label>Amount (mg)<input type="number" min="0" step="1" v-model.number="caffeineForm.amount_mg" required /></label>
          <label>Beverage<input v-model="caffeineForm.beverage_type" /></label>
          <button type="submit">Save caffeine</button>
        </form>

        <!-- Exercise -->
        <form
          v-show="activeTab === 'exercise'"
          class="lifestyle-form form-card"
          @submit.prevent="submitLifestyle('/api/exercise', exerciseForm, 'Exercise session saved.')"
        >
          <label>Date<input type="date" lang="en" v-model="exerciseForm.event_date" required /></label>
          <label>Time<input type="time" v-model="exerciseForm.time" required /></label>
          <label>Duration (min)<input type="number" min="0" v-model.number="exerciseForm.duration_minutes" required /></label>
          <label>Intensity
            <select v-model="exerciseForm.intensity">
              <option>Low</option>
              <option>Moderate</option>
              <option>High</option>
            </select>
          </label>
          <button type="submit">Save exercise</button>
        </form>

        <!-- Screen -->
        <form
          v-show="activeTab === 'screen'"
          class="lifestyle-form form-card"
          @submit.prevent="submitLifestyle('/api/screen', screenForm, 'Screen record saved.')"
        >
          <label>Date<input type="date" lang="en" v-model="screenForm.event_date" required /></label>
          <label>Total screen time (min)<input type="number" min="0" v-model.number="screenForm.total_minutes" required /></label>
          <label>Pre-bed screen time (min)<input type="number" min="0" v-model.number="screenForm.pre_bed_minutes" required /></label>
          <button type="submit">Save screen record</button>
        </form>
      </div>
    </div>

    <!-- Sleep history table -->
    <div class="divider"></div>

    <div class="row-between" style="margin-bottom: var(--sp-4); align-items: baseline;">
      <h2 class="t-section">Recent sleep records</h2>
      <span class="t-caption">Showing last 15</span>
    </div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Bedtime</th>
            <th>Wake</th>
            <th>Duration</th>
            <th>Quality</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in sleepRecords.slice(0, 15)" :key="record.id">
            <td class="td-primary td-mono">{{ record.sleep_date }}</td>
            <td class="td-mono">{{ record.bedtime }}</td>
            <td class="td-mono">{{ record.wake_time }}</td>
            <td class="td-mono">{{ hours(record.duration_minutes) }}</td>
            <td>{{ record.quality }}/5</td>
            <td>
              <!-- Inline delete confirmation -->
              <template v-if="pendingDeleteId === record.id">
                <div class="row" style="gap: var(--sp-2);">
                  <span class="t-caption" style="color: var(--danger);">Delete?</span>
                  <button class="danger sm" @click="confirmDelete(record.id)">Yes</button>
                  <button class="ghost sm"  @click="cancelDelete">No</button>
                </div>
              </template>
              <template v-else>
                <div class="row" style="gap: var(--sp-2);">
                  <button class="secondary sm" @click="editSleep(record)">Edit</button>
                  <button class="ghost sm"     @click="requestDelete(record.id)">Delete</button>
                </div>
              </template>
            </td>
          </tr>
          <tr v-if="!sleepRecords.length">
            <td colspan="6">
              <div class="empty-state" style="padding: var(--sp-6) 0;">
                <div class="empty-state-title">No records yet</div>
                <p class="empty-state-body">Save your first sleep record above to start tracking.</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
/* Two-column entry layout */
.entry-layout {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: var(--sp-8);
  align-items: start;
}

.entry-form-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--sp-3);
  margin-bottom: var(--sp-5);
}

.sleep-form {
  display: grid;
  gap: var(--sp-4);
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-3);
}

.field {
  display: grid;
  gap: 5px;
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-secondary);
}

/* Lifestyle side */
.entry-side {}

.lifestyle-tabs {
  display: flex;
  gap: 2px;
  background: var(--gray-2);
  border-radius: var(--r-md);
  padding: 3px;
  margin-bottom: var(--sp-4);
}

.lifestyle-tab {
  flex: 1;
  background: transparent;
  color: var(--text-secondary);
  padding: 6px var(--sp-3);
  font-size: var(--text-sm);
  border-radius: 4px;
  transition: background var(--dur-fast) var(--ease),
              color var(--dur-fast) var(--ease);
}

.lifestyle-tab:hover:not(.active) {
  background: var(--gray-3);
  color: var(--text-primary);
  transform: none;
}

.lifestyle-tab.active {
  background: var(--gray-0);
  color: var(--text-primary);
  font-weight: 600;
  box-shadow: var(--shadow-1);
}

.lifestyle-form {
  display: grid;
  gap: var(--sp-3);
}

/* Responsive */
@media (max-width: 860px) {
  .entry-layout {
    grid-template-columns: 1fr;
    gap: var(--sp-6);
  }
  .form-row-2 { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 480px) {
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>
