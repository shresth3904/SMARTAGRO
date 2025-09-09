function createLineGraph(elementId, rawData, graphTitle, color1, color2) {
    const labels = rawData.slice(1).map(row => row[0]);
    const values = rawData.slice(1).map(row => row[1]);
  
    const ctx = document.getElementById(elementId).getContext('2d');
    const newChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: rawData[0][1],
          data: values,
          borderColor: 'white',
          backgroundColor: 'white',
          borderWidth: 2,
          tension: 0.4,
          pointBackgroundColor: color1,
          pointRadius: 5
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: graphTitle,
            color: color2,
            font: { size: 20, weight: 'bold' }
          }
        },
        scales: {
          x: {
            grid: { color: "gray" },
            ticks: { color: "rgb(200, 200, 200)" }
          },
          y: {
            grid: { color: "gray" },
            ticks: { color: "rgb(200, 200, 200)" },
            beginAtZero: true,
            title: {
              display: true,
              text: rawData[0][1],
              color: color1,
              font: { size: 14, weight: 'bold' }
            }
          }
        }
      }
    });
  
    return newChart;
}
  
let moistureChart, tempChart, humidityChart, waterLevelChart;
moistureChart = createLineGraph('moisture', rawData, 'Soil Moisture', 'green', 'lightgreen');
tempChart = createLineGraph('temp', temperature, 'Temperature levels', 'orange', 'tomato');
humidityChart = createLineGraph('humidity', humidity, 'Humidity', 'cyan', 'lightcyan');
waterLevelChart = createLineGraph('water_lvl', water_level, 'Water Levels', 'blue', 'lightblue');
  
function convertData(data) {
    const moisture = [['id', 'moisture']];
    const temp = [['id', 'temp']];
    const humidity = [['id', 'humidity']];
    const water_lvl = [['id', 'water_lvl']];
  
    for (let i = data.length - 1; i >= 0; i--) {
        const item = data[i];
        const id = item[0];
        const moistureVal = item[1];
        const tempVal = item[2];
        const humidityVal = item[3];
        const waterLvlVal = item[4];

        moisture.push([id, moistureVal]);
        temp.push([id, tempVal]);
        humidity.push([id, humidityVal]);
        water_lvl.push([id, waterLvlVal]);
      }
  
    return {
      moisture,
      temp,
      humidity,
      water_lvl
    };
}
  
async function fetchData() {
    try {
      const response = await fetch('http://127.0.0.1:5000/fetch_parameters');
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      let converted = convertData(data);
      const moistureLabels = converted.moisture.slice(1).map(row => row[0]);
      const moistureValues = converted.moisture.slice(1).map(row => row[1]);
      const tempValues = converted.temp.slice(1).map(row => row[1]);
      const humidityValues = converted.humidity.slice(1).map(row => row[1]);
      const waterLvlValues = converted.water_lvl.slice(1).map(row => row[1]);
  
      moistureChart.data.labels = moistureLabels;
      moistureChart.data.datasets[0].data = moistureValues;
      moistureChart.update();
      
      tempChart.data.labels = moistureLabels; 
      tempChart.data.datasets[0].data = tempValues;
      tempChart.update();
      
      humidityChart.data.labels = moistureLabels;
      humidityChart.data.datasets[0].data = humidityValues;
      humidityChart.update();
      
      waterLevelChart.data.labels = moistureLabels;
      waterLevelChart.data.datasets[0].data = waterLvlValues;
      waterLevelChart.update();
  
      const lastDataPoint = data[0];
      if (lastDataPoint) {
          setTemperature(lastDataPoint[2]);
          updateWaterLevel(lastDataPoint[4]);
          updateMoistureLevel(lastDataPoint[1]);
          updateHumidityLevel(lastDataPoint[3]);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
}
  
const intervalId = setInterval(fetchData, 500);
  
let mercury = document.getElementById("mercury");
let tempValue = document.getElementById("tempValue");
const waterElement = document.getElementById("waterLevel");
const valueElement = document.getElementById("levelValue");
const fillElement = document.getElementById("moistureFill");
const moistureValue = document.getElementById("moistureValue");
const fillElement_humidity = document.getElementById("humidityFill");
const valueElement_humidity = document.getElementById("humidityValue");

function setTemperature(t) {
    mercury.style.height = `${t}%`;
    tempValue.textContent = `${t}°C`;
}

function updateWaterLevel(level) {
    waterElement.style.height = `${level}%`;
    valueElement.textContent = `${level}%`;
}

function updateMoistureLevel(level) {
    fillElement.style.height = `${level}%`;
    moistureValue.textContent = `${level}%`;
    fillElement.classList.add("filled");
}

function updateHumidityLevel(level) {
    fillElement_humidity.style.height = `${level}%`;
    valueElement_humidity.textContent = `${level}%`;
    fillElement_humidity.classList.add("filled");
}

window.onload = function () {
    updateMoistureLevel(current_moisture);
    updateWaterLevel(current_water_lvl);
    updateHumidityLevel(current_humidity);
    setTemperature(current_temp);
};