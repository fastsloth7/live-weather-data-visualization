import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st



base_url = "https://api.openweathermap.org/data/2.5/weather?"

def get_weather_data(city_name, api_key):
    url = f"{base_url}q={city_name.capitalize()}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_info = response.json()
        return weather_info
    else:
        print(f"Error: {response.status_code} - {response.text}")


def collect_weather_data(city_names, api_key):
    weather_list = []

    for city in city_names:
        weather_data = get_weather_data(city, api_key)
        
        if weather_data:
            city_weather = {
                "City": weather_data['name'],
                "Temperature (°C)": weather_data['main']['temp'],
                "Feels Like (°C)": weather_data['main']['feels_like'],
                "Humidity (%)": weather_data['main']['humidity'],
                "Pressure (hPa)": weather_data['main']['pressure'],
                "Wind Speed (m/s)": weather_data['wind']['speed'],
                "Weather": weather_data['weather'][0]['description'],
                "Visibility (m)": weather_data.get('visibility', 0),
                "Sunrise (UTC)": pd.to_datetime(weather_data['sys']['sunrise'], unit='s'),
                "Sunset (UTC)": pd.to_datetime(weather_data['sys']['sunset'], unit='s'),
                "Timezone": weather_data['timezone'],
                "Cloudiness (%)": weather_data['clouds']['all'],
            }
            weather_list.append(city_weather)
    weather_df = pd.DataFrame(weather_list)
    
    return weather_df
    
def data_preprocessing(df):
    

    print(df.isnull().sum())
    df.rename(columns = {"Temperature (°C)": "Temperature", 
                     "Feels Like (°C)": "Feels Like", 
                     "Humidity (%)": "Humidity", 
                     "Pressure (hPa)": "Pressure", 
                     "Wind Speed (m/s)": "Wind Speed",
                     "Visibility (m)": "Visibility (km)"}, 
                     inplace = True)
    
    df["Visibility (km)"] = df["Visibility (km)"].apply(lambda x: x / 1000)  # Convert to km
    df["Wind Speed"] = df["Wind Speed"].apply(lambda x: x * 3.6) 
    columns_to_round = ["Temperature", "Feels Like", "Wind Speed"]
    df[columns_to_round] = df[columns_to_round].round(0).astype(int)
    df["Weather"] = df["Weather"].str.capitalize()
    df["City"] = df["City"].str.capitalize()
    df["Daylight Duration (hrs)"] = (df["Sunset (UTC)"] - df["Sunrise (UTC)"]).dt.total_seconds() / 3600
    
    return df

def plot_weather_data(df):
    
    sns.set_theme(style = "whitegrid")


    #Bar plot by Temperature By City
    st.subheader("Temperature by City")
    fig, ax = plt.subplots(figsize = (10, 6))
    sns.barplot(x = "City", y = "Temperature", data = df, palette = "coolwarm", ax = ax)

    plt.title("Temperature by City")
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 45, ha = "right", fontsize = 10)
    plt.xlabel("City")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    st.pyplot(fig)

    #line plot by WindSpeed By City
    st.subheader("Wind Speed by City")
    fig, ax = plt.subplots(figsize = (10, 6))
    sns.lineplot(x = "City", y = "Wind Speed", data = df, marker = "o", 
                 color = "red", markersize = 10, ax = ax)
    plt.title("Wind Speed by City")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    plt.xlabel("City")
    plt.ylabel("Wind Speed (km/h)")
    plt.tight_layout()
    st.pyplot(fig)

    #pie chart by Weather Condition 
    st.subheader("Weather Condition Distribution")
    fig, ax = plt.subplots(figsize = (10, 6))
    weather_counts = df["Weather"].value_counts()
    weather_counts.plot.pie(autopct = "%1.1f%%", startangle = 90, ax = ax, pctdistance = 0.8,
                            colors = sns.color_palette("pastel"), legend = False)
    plt.title("Weather Condition Distribution")
    plt.ylabel("")  
    
    st.pyplot(fig)
    
    #histogram by Humidity Distribution
    st.subheader("Humidity Distribution")
    fig, ax = plt.subplots(figsize = (10, 6))
    sns.histplot(df["Humidity"], bins = 10, kde = True, color = "blue", ax = ax)
    plt.title("Humidity Distribution")
    plt.xlabel("Humidity (%)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    st.pyplot(fig)  

    #jointplot by visibility and Temperature
    st.subheader("Visibility vs Temperature")
    g = sns.jointplot(x = "Visibility (km)", y = "Temperature", data = df, kind = "hex", color =  "#4CB391")
    g.fig.set_size_inches(10, 8)
    g.ax_joint.set_xlabel("Visibility (km)")
    g.ax_joint.set_ylabel("Temperature (°C)")
    plt.tight_layout()
    st.pyplot(g.fig)
    

    #Boxplot by Feels Like and humidity
    st.subheader("Feels Like vs Humidity")
    fig, ax = plt.subplots(figsize = (10, 5))
    sns.boxplot(x = "Feels Like", y = "Humidity", data = df, palette = "Set2", ax = ax)
    plt.title("Feels Like vs Humidity")
    plt.xlabel("Feels Like (°C)")
    plt.ylabel("Humidity (%)")
    plt.tight_layout()
    st.pyplot(fig)

    
if __name__ == "__main__":
    st.title("Live Weather Data Dashboard")

    city_names = ["Delhi", "New York", "Tokyo", "Paris", "London", "Beijing", "Moscow", "Berlin", "Dubai", "Mumbai",
    "Los Angeles", "Chicago", "Toronto", "São Paulo", "Buenos Aires", "Cairo", "Istanbul", "Bangkok", "Seoul", "Jakarta",
    "Sydney", "Melbourne", "Mexico City", "Madrid", "Rome", "Lagos", "Nairobi", "Cape Town", "Karachi", "Lima",
    "Singapore", "Hong Kong", "Barcelona", "Vienna", "Budapest", "Warsaw", "Prague", "Dublin", "Brussels", "Amsterdam",
    "Zurich", "Geneva", "Stockholm", "Oslo", "Helsinki", "Copenhagen", "Doha", "Riyadh", "Tehran", "Kuala Lumpur"]

    try:
        api_key = open("api_key.txt").read().strip()
    except FileNotFoundError:
        st.error("API key file not found. Please check the path and try again.")
        st.stop()

    st.info("Fetching real-time weather data...")
    df_before_processing = collect_weather_data(city_names, api_key)

    if not df_before_processing.empty:
        df = data_preprocessing(df_before_processing)
        st.success("Weather data loaded successfully!")
        st.dataframe(df)
        plot_weather_data(df)
    else:
        st.warning("No data available. Please check your API key and city names.")