// Fetch data from Flask API
fetch('/temperature')
  .then((response) => response.json())
  .then((data) => {
    const temperatureElement = document.getElementById('temperature')
    temperatureElement.textContent = `Temperature: ${data.temperature}°C`
  })

fetch('/humidity')
  .then((response) => response.json())
  .then((data) => {
    const humidityElement = document.getElementById('humidity')
    humidityElement.textContent = `Humidity: ${data.humidity}%`
  })
