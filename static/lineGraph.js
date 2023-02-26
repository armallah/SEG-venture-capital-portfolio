var xValues = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

new Chart("myLineGraph", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      data: [860,1140,1060,1060,1070,1110,1330,2210,7830,2478,3020,3492],
      borderColor: "red",
      fill: false,
      label: "Hospitality"
    },{
      data: [1600,1700,1700,1900,2000,2700,4000,5000,6000,7000,7500,7650],
      borderColor: "green",
      fill: false,
      label: "Tech"
    },{
      data: [300,700,2000,5000,6000,4000,2000,1000,200,100,325,300],
      borderColor: "blue",
      fill: false,
      label: "Manufacturing"
    }]
  },
  options: {
    legend: {display: true}
  }
});
