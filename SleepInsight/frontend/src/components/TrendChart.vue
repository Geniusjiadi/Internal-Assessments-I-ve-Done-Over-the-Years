<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
  series: { type: Array, default: () => [] },
  metric: { type: String, default: "duration_minutes" },
  title: { type: String, default: "Trend" }
});

const canvas = ref(null);
let chart = null;

function render() {
  if (!canvas.value) return;
  if (chart) chart.destroy();

  const labels = props.series.map((item) => item.date);
  const values = props.series.map((item) => item[props.metric]);

  chart = new Chart(canvas.value, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: props.title,
        data: values,
        tension: 0.3,
        borderColor: "#1f5261",
        borderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 4,
        pointHoverBackgroundColor: "#1f5261",
        fill: true,
        backgroundColor: (ctx) => {
          const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, ctx.chart.height);
          gradient.addColorStop(0, "rgba(31, 82, 97, 0.12)");
          gradient.addColorStop(1, "rgba(31, 82, 97, 0)");
          return gradient;
        }
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#1e2e2f",
          titleColor: "#a0acad",
          bodyColor: "#f7f8f8",
          titleFont: { family: "Inter", size: 11, weight: "500" },
          bodyFont: { family: "Inter", size: 13, weight: "600" },
          padding: 10,
          cornerRadius: 8,
          displayColors: false
        }
      },
      scales: {
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: {
            color: "#a0acad",
            font: { family: "Inter", size: 11 },
            maxRotation: 0,
            maxTicksLimit: 8
          }
        },
        y: {
          beginAtZero: false,
          grid: {
            color: "#e4e8e8",
            drawBorder: false
          },
          border: { display: false, dash: [4, 4] },
          ticks: {
            color: "#a0acad",
            font: { family: "Inter", size: 11 },
            maxTicksLimit: 5
          }
        }
      }
    }
  });
}

onMounted(render);
watch(() => [props.series, props.metric], render, { deep: true });
onBeforeUnmount(() => chart?.destroy());
</script>

<template>
  <div class="chart-wrap">
    <canvas ref="canvas" :aria-label="title" role="img"></canvas>
  </div>
</template>
