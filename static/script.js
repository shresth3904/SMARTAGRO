let mercury = document.getElementById("mercury");
let tempValue = document.getElementById("tempValue");

function setTemperature(t) {
  mercury.style.height = `${t}%`;
  tempValue.textContent = `${t}°C`;
}

window.onload = setTemperature(current_temp);

const targetLevel = current_water_lvl;
const waterElement = document.getElementById("waterLevel");
const valueElement = document.getElementById("levelValue");

function updateWaterLevel() {
  waterElement.style.height = `${targetLevel}%`;
  valueElement.textContent = `${targetLevel}%`;
}

const targetMoisture = current_moisture;

const fillElement = document.getElementById("moistureFill");
const moistureValue = document.getElementById("moistureValue");

function updateMoistureLevel() {
  fillElement.style.height = `${targetMoisture}%`;
  moistureValue.textContent = `${targetMoisture}%`;
  fillElement.classList.add("filled");
}

const targetHumidity = 78;

const fillElement_humidity = document.getElementById("humidityFill");
const valueElement_humidity = document.getElementById("humidityValue");

function updateHumidityLevel() {
  fillElement_humidity.style.height = `${targetHumidity}%`;
  valueElement_humidity.textContent = `${targetHumidity}%`;
  fillElement_humidity.classList.add("filled");
}

window.onload = function () {
  updateMoistureLevel();
  updateWaterLevel();
  updateHumidityLevel();
};
