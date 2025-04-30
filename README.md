Live Weather Data Dashboard
A real-time interactive dashboard built with Python, Streamlit, and the OpenWeatherMap API that visualizes weather conditions across 50+ major cities around the world. This project integrates data fetching, cleaning, and advanced visualizations into a clean and informative web app.

 Features
 Real-time weather data using OpenWeatherMap API

 Key metrics: Temperature, Feels Like, Humidity, Pressure, Wind Speed, Cloudiness, and more

 Sunrise, Sunset, and Daylight Duration calculation

 Visualizations: bar plots, line charts, histograms, pie charts, jointplots, boxplots

 Covers major global cities for a comparative overview

 Built with Streamlit for fast deployment and interactive viewing

Project Structure
graphql
Copy
Edit
weather-dashboard/
│
├── weather_dashboard.py      # Main Streamlit app
├── api_key.txt               # Your OpenWeatherMap API key (excluded from repo)
├── README.md                 # Project description and setup
🔧 How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/weather-data-dashboard.git
cd weather-data-dashboard
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Add your API key:

Create a file named api_key.txt in the project root

Paste your OpenWeatherMap API key inside (no quotes)

Launch the app:

bash
Copy
Edit
streamlit run weather_dashboard.py
📷 Screenshots
(Add screenshots of your Streamlit app here for better visualization.)

Requirements
Python 3.7+

Streamlit

Requests

Pandas

Seaborn

Matplotlib

 API Used
OpenWeatherMap Current Weather API

Learning Outcome
Working with real-time APIs

Building Streamlit apps for data presentation

Performing EDA and visualizations

Converting raw JSON data into insightful visuals

Contributing
Pull requests and improvements are welcome!

📜 License
This project is licensed under the MIT License.

