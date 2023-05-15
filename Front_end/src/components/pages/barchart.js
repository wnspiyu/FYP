import React from "react";
import { Bar } from "react-chartjs-2";
import Chart from 'chart.js/auto';

Chart.register({
    id: 'category',
    afterBuildTicks: function(chart) {
        chart.ticks = chart.data.labels;
        return;
    }
});

const data = {
  labels: ["January", "February", "March", "April", "May", "June", "July"],
  datasets: [
    {
      label: "Sales",
      data: [12, 19, 3, 5, 2, 3, 15],
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 1,
    },
  ],
};

const options = {
  scales: {
    yAxes: [
      {
        ticks: {
          beginAtZero: true,
        },
      },
    ],
  },
};

const BarChart = () => {
  return (
    <div>
      <h2>Bar Chart</h2>
      <Bar data={data} options={options} />
    </div>
  );
};

export default BarChart;