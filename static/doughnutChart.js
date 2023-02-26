new Chart(document.getElementById("MyDoughnutChart"), {
  type: 'doughnut',
  data: {
    labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
    datasets: [
      {
        label: "Companies",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
        data: [45,77,252,58,156]
      }
    ]
  },
  options: {
    title: {
      display: true,
      text: 'Company Locations'
    }
  }
});
