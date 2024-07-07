import pandas as pd
import matplotlib.pyplot as plt

def sucess_vs_orbit(data):
   # Update the success condition to consider only "True RTLS" and "True ASDS" as successful outcomes
    data['Success'] = data['Outcome'].apply(lambda x: 1 if x in ['True RTLS', 'True ASDS'] else 0)

    # Calculate the success rate for each orbit type
    success_rate = data.groupby('Orbit')['Success'].mean().reset_index()

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(success_rate['Orbit'], success_rate['Success'], color='skyblue')
    plt.xlabel('Orbit Type')
    plt.ylabel('Success Rate')
    plt.title('Success Rate of Each Orbit Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def payload_vs_launchsite(data):
    plt.figure(figsize=(10, 5))
    # Plot Scatter 
    plt.scatter(data['PayloadMass'], data['LaunchSite'])
    plt.title(f'Scatter Plot for (PayloadMass) vs (LaunchSite)')
    plt.ylabel(f'Number of LaunchSite')
    plt.xlabel('PayloadMass')
    plt.show()

def flight_vs_orbit(data):
    plt.figure(figsize=(10, 5))
    # Plot Scatter 
    plt.scatter(data['FlightNumber'], data['Orbit'])
    plt.title(f'Scatter Plot (FlightNumber) vs (Orbit)')
    plt.ylabel(f'Orbit Type')
    plt.xlabel('Flight Number')
    plt.show()

def payload_vs_orbit(data):
    plt.figure(figsize=(10, 5))
    # Plot Scatter 
    plt.scatter(data['PayloadMass'], data['Orbit'])
    plt.title(f'Scatter Plot (PayloadMass) vs (Orbit)')
    plt.ylabel(f'Orbit Type')
    plt.xlabel('Pay load Mass')
    plt.show()

def yearly_lunch_success(data):
    # create new column conaint just year that export from (Date) column
    data['Date'] = pd.to_datetime(data['Date'])
    data['year_date'] = data['Date'].dt.year

    plot_data = data['year_date'].value_counts().reset_index()
    plot_data.columns = ['year_date', 'count']
    plot_data = plot_data.sort_values('year_date')

    plt.plot(plot_data['year_date'], plot_data['count'], marker='o')
    plt.title('Line Chart of Trend success LAunch Site yearly') 
    plt.xlabel('Years')
    plt.ylabel('Total Success launch site')
    plt.show()


def main():
    # Load the dataset
    data = data = pd.read_csv("dataset_collected.csv")
    
    yearly_lunch_success(data)  # Trend of LaunchSite yearly

    sucess_vs_orbit(data)  # Success rate for each Orbit type

    payload_vs_launchsite(data)  # Payload VS LunchSite

    flight_vs_orbit(data)  # FlightNumber VS Orbit

    payload_vs_orbit(data)  # Payload VS Orbit
    

if __name__ == '__main__':
  main()