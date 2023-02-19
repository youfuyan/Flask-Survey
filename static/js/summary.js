// Get the canvas element
var ctx = document.getElementById("myChart").getContext("2d");

// Get the data from Flask app
var timestamps = {{ timestamps|tojson }};
var counts = {{ counts|tojson }};
console.log(timestamps);
console.log(counts);

// Create the bar chart
var myChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: timestamps,
    datasets: [
      {
        label: "Response Frequency",
        data: counts,
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  },
});
