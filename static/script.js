google.charts.load('current', {packages:['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable(data);

        var options = { title: 'Moisture lvl' };
        var chart = new google.visualization.LineChart(document.getElementById('moisture'));
        chart.draw(data, options);
      }