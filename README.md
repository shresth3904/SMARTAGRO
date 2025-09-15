<h1>SMARTAGRO</h1>
<br><br>

<p>
A scalable IoT solution for smart irrigation and sustainable farming in hilly regions, built as part of Smart India Hackathon 2025.
</p>
<br>

<h3>PROJECT SUMMARY</h3>
<p>
SmartAgro is an IoT-enabled precision irrigation and water management system designed for farms in hilly regions. 
It leverages <b>ESP32-based sensor nodes</b> to acquire real-time data from <b>HC-SR04 ultrasonic sensors</b> (tank water level), 
<b>capacitive soil moisture probes</b> (field condition monitoring), and <b>DHT22 digital thermo-hygrometers</b> (ambient temperature and humidity).
<br><br>
Sensor data is serialized into <b>JSON payloads</b> and transmitted via <b>HTTP REST APIs</b> to a cloud backend and a responsive web dashboard. 
Farmers can visualize live data, receive <b>alerts for critical thresholds</b> (low water level, dry soil), and control pump actuation either 
through <b>Auto Mode</b> (closed-loop threshold & ML-driven irrigation logic) or <b>Manual Override</b> (on-demand dashboard toggling).
<br><br>
The system integrates <b>rainwater harvesting management</b> with real-time tank monitoring and employs 
<b>relay-driven pump actuation</b> powered by independent battery sources. 
Edge-level processing on the ESP32 reduces cloud dependency, enabling <b>low-latency decision making</b> and reliable offline performance.
<br><br>
Overall, SmartAgro provides a <b>scalable, modular, and cost-effective IoT solution</b> that empowers farmers with data-driven, efficient, and sustainable irrigation practices.
</p>
<br>

<h3>PROBLEM STATEMENT</h3>
<p>
Implementation of Smart Agriculture for Efficient Cultivation in Hilly Regions
</p>
<br>

<h3>IMPLEMENTATION</h3>
<p>
- Soil moisture and temperature sensors monitor field conditions in real time.<br>
- A crop database determines optimal watering thresholds.<br>
- Automated valve and pump control via ESP32 microcontrollers.<br>
- Rainwater harvesting integrated with water level sensors.<br>
- A web/mobile dashboard provides farmers with live data and control options.<br>
- Alerts and notifications keep farmers informed about critical soil or water levels.<br>
</p>
<br>

<h3>TEAM MEMBERS</h3>
<p>
SHRESTH - 2024UEA6597<br>
PIYUSH LAL - 2024UEA6577<br>
DAKSH GULIA - 2024UEA6584<br>
TANAY AGARWAL - 2024UEA6582<br>
PRATHAM SAGAR - 2024UEA6628<br>
VEDIKA CHOUDHARY -- 2024UEA6609<br>
</p>
