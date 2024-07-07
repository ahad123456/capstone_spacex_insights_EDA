import pandas as pd
import csv, sqlite3

def unique_launchsite():
    query = "SELECT Distinct launchSite from my_table"
    return query

def launchsite_with_KSC():
   query = "SELECT * from my_table WHERE launchSite LIKE 'KSC%' LIMIT 5"
   return query

def fiirst_success_landing():
   query = "SELECT Date from my_table WHERE Outcome in ('True ASDS','True RTLS') ORDER BY Date ASC LIMIT 1"
   return query

def total_payload():
   query = "SELECT sum(PayloadMass) from my_table WHERE customers LIKE 'NASA' "
   return query 

''' Get successful landing with payload between 4000 and 6000 '''
def success_landing():
   query = "SELECT BoosterVersion from my_table WHERE PayloadMass BETWEEN 4000 AND 6000 "
   return query

def total_success_fail():
   query = "SELECT s.succ , f.fal FROM (SELECT count(Flights) as succ from my_table WHERE Outcome LIKE 'True%' ) s, (SELECT count(Flights) as fal from my_table WHERE Outcome LIKE 'False%' ) f"
   return query

def max_payload():
   query = "SELECT max(PayloadMass), BoosterVersion from my_table"
   return query

def records_2015():
   query = """ SELECT BoosterVersion, Outcome , LaunchSite,
       CASE strftime('%m', Date)
           WHEN '01' THEN 'January'
           WHEN '02' THEN 'February'
           WHEN '03' THEN 'March'
           WHEN '04' THEN 'April'
           WHEN '05' THEN 'May'
           WHEN '06' THEN 'June'
           WHEN '07' THEN 'July'
           WHEN '08' THEN 'August'
           WHEN '09' THEN 'September'
           WHEN '10' THEN 'October'
           WHEN '11' THEN 'November'
           WHEN '12' THEN 'December'
       END month from my_table WHERE Date LIKE '2017%'
   """
   return query

def convert_date(val):
   '''
      Convert Date columns data to format yyyy-MM-dd
   '''   
   value = val[0:10]
   return value

def between_2010_2017():
   query = """SELECT s.succ AS "Success (ground pad)", f.fal AS "Failure (drone ship)" 
         FROM (SELECT count(Flights) as succ from my_table WHERE Outcome LIKE 'True%' AND Date between '2010-06-04' AND '2017-03-20' ) s, 
              (SELECT count(Flights) as fal from my_table WHERE Outcome LIKE 'False%' AND Date between '2010-06-04' AND '2017-03-20' ) f
         """
   return query

def excute_query(query, conn, text):
   result = pd.read_sql_query(query, conn)
   print(text)
   print(result)
   print("\n -------------------")

def main():
    df = pd.read_csv('dataset_collected.csv')  # Read CSV into a DataFramev

    # Create a SQLite in-memory database
    conn = sqlite3.connect(':memory:')  # Creates an in-memory database
    cursor = conn.cursor()
    df.to_sql('my_table', conn, index=False, if_exists='replace')   # Upload the DataFrame to the in-memory database
    
    # Convert date
    df['Date'] = df['Date'].apply(convert_date) 
 
    #query = "SELECT FlightNumber, PayloadMass FROM my_table WHERE launchSite = 'Kwajalein Atoll'"  # Step 4: Write and execute SQL queries

    unique_launchsite_query = unique_launchsite()  # The unique launch site
    excute_query(unique_launchsite_query, conn, 'The unique launch site are:')
    
    launchsite_with_KSC_query = launchsite_with_KSC()  # Launch Site Names Begin with 'KSC'
    excute_query(launchsite_with_KSC_query, conn, "Launch Site Names Begin with 'KSC' : ")
    
    fiirst_success_landing_query = fiirst_success_landing()  # First Successful Ground Landing Date
    excute_query(fiirst_success_landing_query, conn, "First Successful Ground Landing Date: ")
   
    success_landing_query = success_landing()  # Successful Drone Ship Landing with Payload between 4000 and 6000
    excute_query(success_landing_query, conn, "Successful Drone Ship Landing with Payload between 4000 and 6000 are: ")

    total_success_fail_query = total_success_fail() # Total Number of Successful and Failure Mission Outcomes
    excute_query(total_success_fail_query, conn, "Total Number of Successful and Failure Mission Outcomes are: ")

    max_payload_query = max_payload()  # Boosters Carried Maximum Payload
    excute_query(max_payload_query, conn, "Boosters Carried Maximum Payload")

    between_2010_2017_query = between_2010_2017()  # Rank Landing Outcomes Between 2010-06-04 and 2017-03-20
    excute_query(between_2010_2017_query, conn, "Rank Landing Outcomes Between 2010-06-04 and 2017-03-20")

    cursor.close()
    conn.close()
    


if __name__ == '__main__':
  main()
