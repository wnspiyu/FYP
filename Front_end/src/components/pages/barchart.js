// import React from 'react';
// import { Bar } from 'react-chartjs-2';
// import Chart from 'chart.js/auto';

// Chart.register({
//     id: 'category',
//     afterBuildTicks: function(chart) {
//         chart.ticks = chart.data.labels;
//         return;
//     }
// });

// const data = {
//     labels: ['A', 'B', 'C', 'D', 'E'],
//     datasets: [
//         {
//             label: 'My Data',
//             data: [1, 2, 3, 4, 5],
//             backgroundColor: 'rgba(255, 99, 132, 0.2)',
//             borderColor: 'rgba(255, 99, 132, 1)',
//             borderWidth: 1,
//         },
//     ],
// };

// const options = {
//     scales: {
//         y: {
//             beginAtZero: true,
//         },
//         x: {
//             type: 'category', // use the registered "category" scale here
//             display: true,
//             title: {
//                 display: true,
//                 text: 'My Categories',
//             },
//         },
//     },
// };

// export default function MyChart(){
//     return(
//         <div className="chart-container">
//         <h2>My Chart</h2>
//         <Bar data={data} options={options} canvasClassName="chart-canvas" />
//     </div>
//     );
// }

import React from "react";
import { Bar } from "react-chartjs-2";

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