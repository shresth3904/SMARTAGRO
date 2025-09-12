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

let prev_pump_id = 0;
let pump_req_count = 0;
let pumpConnectionStatus = 'fetching...';
async function fetchPumpStatus() {
  const response = await fetch('/pump_status');
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }
  const data = await response.json();
  if (pump_req_count > 0){
    if (data[0] != prev_pump_id){
      pumpConnectionStatus = 'connected';
      document.getElementById('pump_status_value').textContent = 'Connected';
      document.getElementById('pump_status_value').className = 'connected';
    }
    else {
      pumpConnectionStatus = 'Disconnected'
      document.getElementById('pump_status_value').textContent = 'Disconnected';
      document.getElementById('pump_status_value').className = 'disconnected';
    }
  }
  prev_pump_id = data[0];
  pump_req_count++;
  return data[1];
}

const intervalId_pump = setInterval(fetchPumpStatus, 2000);

let prev_id = 0;
let connectionStatus = 'connected';
let connection_req_count = 0;
async function fetchData() {
    try {
      const response = await fetch('/fetch_parameters');
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
          if (lastDataPoint[0] != prev_id){
            connectionStatus = 'connected';
          }
          else connectionStatus = 'Disconnected'
          prev_id = lastDataPoint[0];
          setTemperature(lastDataPoint[2]);
          updateWaterLevel(lastDataPoint[4]);
          updateMoistureLevel(lastDataPoint[1]);
          updateHumidityLevel(lastDataPoint[3]);
    }
    } catch (error) {
      console.error('Error fetching data:', error);
    }

  if (connectionStatus == 'Disconnected'){
    document.getElementById('connection_status_value1').textContent = 'Disconnected';
    document.getElementById('connection_status_value1').className = 'disconnected';
    document.getElementById('connection_status_value2').textContent = 'Disconnected';
    document.getElementById('connection_status_value2').className = 'disconnected';
    document.getElementById('connection_status_value3').textContent = 'Disconnected';
    document.getElementById('connection_status_value3').className = 'disconnected';
  }
  else if (connectionStatus == 'connected'){
    if (connection_req_count > 1){
    document.getElementById('connection_status_value1').textContent = 'Connected';
    document.getElementById('connection_status_value1').className = 'connected';
    document.getElementById('connection_status_value2').textContent = 'Connected';
    document.getElementById('connection_status_value2').className = 'connected';
    document.getElementById('connection_status_value3').textContent = 'Connected';
    document.getElementById('connection_status_value3').className = 'connected';
  }
  }
  connection_req_count++;
}
  
const intervalId = setInterval(fetchData, 2000);
  
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
    document.getElementById('tank_info').innerHTML = `Current volume: ${(level)/100} liter<br>Total Capacity: 01 liter`
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


function change_opr_mode(mode) {
  fetch('/set_mode', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ mode: mode }),
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === 'success') {
          console.log('Mode changed to:', data.mode);
          const pumpButton = document.getElementById('pump_btn');
          const auto = document.getElementById('auto');
          const manual = document.getElementById('manual');
          
          current_mode = data.mode; 
          if (current_mode === 'AUTO') {
              pumpButton.classList.remove('pump_btn');
              pumpButton.classList.add('pump_btn_disabled');
              pumpButton.disabled = true;

              auto.classList.add('selected_opr');
              auto.classList.remove('opr_btn');
              manual.classList.add('opr_btn');
              manual.classList.remove('selected_opr');
          } else { 
              pumpButton.classList.add('pump_btn');
              pumpButton.classList.remove('pump_btn_disabled');
              pumpButton.disabled = false;

              auto.classList.remove('selected_opr');
              auto.classList.add('opr_btn');
              manual.classList.remove('opr_btn');
              manual.classList.add('selected_opr');
          }
      }
  })
  .catch(error => console.error('Error setting mode:', error));
}

function toggle_switch() {
  const pumpButton = document.getElementById('pump_btn');
  
  if (pumpButton.disabled) {
      return;
  }

  const isTurningOn = pumpButton.textContent.trim() === 'TURN PUMP ON';
  const command = isTurningOn ? 1 : 0;

  fetch('/toggle_pump', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ command: command }),
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === 'success') {
          console.log('Pump command sent:', data.command);
         
          if (isTurningOn) {
            pumpButton.textContent = 'TURN PUMP OFF';
            pumpButton.className = 'pump_btn_off'; 
        } else {
            pumpButton.textContent = 'TURN PUMP ON';
            pumpButton.className = 'pump_btn';
        }
      }
  })
  .catch(error => console.error('Error toggling pump:', error));
}

