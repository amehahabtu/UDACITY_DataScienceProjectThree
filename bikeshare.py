'''
Name : Ameha Habtu
Description: This program reads csv files for 3 cities,interacts with users to filter by month &/day or both and get stats. The stats incudes trip time , trip duration, stations, users profile information.
Date : 9/26/2021

'''
import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': './chicago.csv',
              'new york city': './new_york_city.csv',
              'washington': './washington.csv' }
  
cities =['chicago','new york city','washington']
months = ['all','january','february','march','april','may','june']
days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    global city, month,day
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
     # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs    

    city = input('Enter the city\'s name that you would like to take a look (Chicago|New York City|Washington):  ').lower().strip()
    while(city not in cities) : 
        print('Sorry! The city you entered doesn\'t exist in our record.')
        city_name = input('please re-enter valid city\'s name: ').lower().strip()
        city=city_name
      
    # Get user input for month (all, january, february, ... , june)
  
    month = input('Please enter the month you would like to filter your data(ALL|January|February|March|April|May|June): ').lower().strip()
    while(month not in months) : 
        print('Sorry! The month you entered doesn\'t exist in our record.')
        mon_period = input('Please re-enter the valid month for the given city: ').lower().strip()
        month = mon_period

    # Get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Please enter day you would like to check you would like to filter your data(ALL|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday): ').lower().strip()
    while (day not in days): 
        print('Oops! The day you entered doesn\'t exist in our record.')
        day_period = input('Please re-enter the valid day as appeared in the above: ').lower().strip()
        day = day_period    

    print('-'*80)
    print(f'Your filtering Criteria is\nCity : {city.title()}\tMonth: {month.title()}\tDay: {day.title()}')
    return city, month, day


def load_data(city, month, day):    
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all' : 
        months_index =['january','february','march','april','may','june']
        month = months_index.index(month) + 1
        df = df[df['month'] == month]
    else: 
        df
    if day != 'all' : 
        df = df[df['day_of_week'] == day.title()]
    else: 
         df        
    return df

 
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month

    df['Start Time'] = pd.to_datetime(df['Start Time'])    
    most_common_month= df['Start Time'].dt.month_name().mode()[0]  # check the issue with ValueError: 0 is not in range
    print(f'{most_common_month} is the most common month which has many users.')

    # Display the most common day of week
    
    df['Start Time'] = pd.to_datetime(df['Start Time']) 
    most_common_day= df['Start Time'].dt.day_name().mode()[0]
    print(f'{most_common_day} is the most common day of week which has many users.')

    # Display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time']) 
    most_common_start_hour= df['Start Time'].dt.hour.mode()[0]
    print(f'{most_common_start_hour} o\'clock is the most common starting time hour which has many users.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station= df['Start Station'].mode()[0]
    print(f'The most common start station in the given city:  {most_common_start_station}')

    # Display most commonly used end station
    most_common_end_station= df['End Station'].mode()[0]
    print(f'The most common end station in the given city:  {most_common_end_station}')

    #Display most frequent combination of start station and end station trip
   
    most_common_start_and_end_station = df['Start Station'].append(df['End Station']).mode()[0]
    print(f'The most common start and end station in the given city:  {most_common_start_and_end_station}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_in_minutes = total_travel_time/60
    total_travel_time_in_hours= total_travel_time_in_minutes/60
    print(f"The total travel time is {round(total_travel_time)} seconds or {round(total_travel_time_in_minutes)} minutes or {round(total_travel_time_in_hours)} hours.")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()  
    mean_travel_time_in_minutes = mean_travel_time/60
    print(f"The mean travel time is {round(mean_travel_time)} seconds or {round(mean_travel_time_in_minutes)} minutes.")

    # Display maximum travel time
    max_travel_time = df['Trip Duration'].max()  
    max_travel_time_in_minutes = max_travel_time/60
    print(f"The maximum travel time is {round(max_travel_time)} seconds or {round(max_travel_time_in_minutes)} minutes.")
    
    # Display minimum travel time
    min_travel_time = df['Trip Duration'].min()  
    min_travel_time_in_minutes = min_travel_time/60
    print(f"The minimum travel time is {round(min_travel_time)} seconds or {round(min_travel_time_in_minutes)} minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    number_of_user_types = df['User Type'].value_counts()
    print(f'Number of users by user type category:\n{number_of_user_types.to_string()}\n')
    # Display counts of gender
    try:
        counts_of_gender = df['Gender'].value_counts()       
        print(f'Number of users by gender category:\n{counts_of_gender.to_string()}\n')
    except KeyError:
        print('The Gender data doesn\'t exist for the given city.')    

    # Display earliest, most recent, and most common year of birth
    try:             
        earliest_year_of_birth = int(df['Birth Year'].min())
        most_recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].mode()[0])
        print('Users\'Year of Birth\n')
        print(f'The Oldest: {earliest_year_of_birth}\nThe Youngest: {most_recent_year_of_birth}\nThe most common Year of Birth: {most_common_year_of_birth}')
    except KeyError:
         print('The Birth Year data doesn\'t exist for the given city.')    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def display_five_raw_records(df): 
    ans ='Y'
    i=0 
    n=5
    while ans=='Y'or ans=='y':      
        ans= input("Would you like to see 5 lines of raw data for your search (Enter y or Y for Yes , n or N for No)? ").upper()  
        print(df.iloc[i:n])
        i += 5
        n += 5  

def main():  
    print('\nHello! Welcome to US BikeShare Data Analystics. Let\'s explore some bikeshare data!\n')
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_five_raw_records(df)

        restart = input('\nWould you like to another search on US bikeshare?(Enter y or Y for yes , n or N for no): ')
        if restart.lower() != 'y':
            break
    print('\nThank you for visiting the US Bikeshare Data Analystics Platform! You can give us your comment via usbikeshare@datanalytics.com')
if __name__ == "__main__":
	main()