import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "./views/DashboardView.vue";
import EntryView from "./views/EntryView.vue";
import TrendsView from "./views/TrendsView.vue";
import InsightsView from "./views/InsightsView.vue";
import RecommendationsView from "./views/RecommendationsView.vue";
import GoalsView from "./views/GoalsView.vue";

const routes = [
  { path: "/", component: DashboardView, name: "dashboard" },
  { path: "/entry", component: EntryView, name: "entry" },
  { path: "/trends", component: TrendsView, name: "trends" },
  { path: "/insights", component: InsightsView, name: "insights" },
  { path: "/recommendations", component: RecommendationsView, name: "recommendations" },
  { path: "/goals", component: GoalsView, name: "goals" }
];

export default createRouter({
  history: createWebHistory(),
  routes
});
