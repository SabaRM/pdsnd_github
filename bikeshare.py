import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    #Gets user input for city and deals with any incorrect inputs
    city = str(input("Which city would you like to find out about (Chicago, New York City or Washington)?\n\n"))
    city = city.lower()


    while city not in CITY_DATA.keys():
          city = str(input("\nWhoops! Let's try that again. Which city would you like to find out about (Chicago, New York City or Washington)?\n"))
          city = city.lower()


    # Gets user input for month and deals with any incorrect inputs
    month = input("\nPlease go ahead and specify a month of the year in word format (e.g January)\n")
    month = month.lower()

    while month not in ('all', 'january','february','march','april','may','june'):
          month = input("\nThat is not a valid month for this dataset. Please try again! \n")


    # Gets user input for day of week and deals with any incorrect user inputs
    day = input ("\nGreat! Now, please enter a day of the week\n")
    day = day.lower()
    while day not in ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
          day = input ("\nThat is not a valid day of the week. Please try again.\n")
          day = day.lower()


    print('-'*40)
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
    filename = CITY_DATA.get(city)

    print("filename is:",filename)

    df = pd.read_csv(filename)
    # Converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracts month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filters by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Filters by month to create the new dataframe
        df = df[df['month'] == month]

    # Filters by day of week if applicable
    if day != 'all':
        # Filters by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df,day,month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month ONLY if the user chooses to analyse 'all' months
    if month == 'all':
     popular_month = df['month'].mode()[0]
     months = ['january', 'february', 'march', 'april', 'may', 'june']
     pop_month_word = months[popular_month - 1]
     print("The most popular month is: ", pop_month_word.upper())
    else: print("Common month not displayed as a specific month was chosen. Please go back and type 'all' if you would like to know the most common month for this dataset.")

    # Displays the most common day of week only if the user wants chooses to analyse 'all' days
    if day == 'all':
     popular_dayofweek = df['day_of_week'].mode()[0]
     print("The most popular day of the week is: ", popular_dayofweek.upper())
    else: print("Most common day not displayed as a specific weekday was chosen. Please go back and type 'all' if you would like to know the most common day of the week for this dataset.")


    # The following steps are to identify the most common start hour
    # Step 1 converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Step 2 extracts hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

   # Finds the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

   # Replaces NaN values with 0
    df.fillna(0)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""


    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', popular_start_station.upper())

    # Displays most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common end station:', popular_end_station.upper())

    """The most frequent combination of start station and end station is calculated by combining the start and end   stations into a newly created column in the dataframe. The trips are then grouped and counted. The most frequent trip corresponds to the trip with the maximum count"""

    df['Start and end station'] = df['Start Station'] + ' ' + str('to') + ' ' + df['End Station']
    Trip_count = df.groupby('Start and end station').count()
    Trip_count_trimmed = Trip_count.iloc[:,0:1]
    Trip_count_trimmed.columns = ['Trip count']
    Popular_trip = Trip_count_trimmed['Trip count'].idxmax()

    print('The most popular trip is {}'.format(Popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    total_traveltime = df['Trip Duration'].sum()
    print ('Total travel time: {} seconds'.format(total_traveltime))

    # Displays mean travel time
    mean_traveltime = df['Trip Duration'].mean()
    print('Mean travel time: {} seconds'.format(mean_traveltime))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays count of user types
    user_count = df.groupby('User Type').count()
    #print(user_count)
    print('\nCount of Customers:{}\nCount of Subscribers:{}'.format(user_count.iloc[0,0],user_count.iloc[1,0]))

    # Displays count of gender where relevant
    if 'Gender' in df:
        gender_count = df.groupby('Gender').count()
        print('\nFemale count:{}\nMale count: {}'.format(gender_count.iloc[0,0],gender_count.iloc[1,0]))
    else: print('\nSorry! There is no gender information for this dataset')

    # Displays earliest, most recent, and most common year of birth where relevant. If no birth or gender data is
    # available in the dataset, a relevant user message is displayed.
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        popular_birth_year = df['Birth Year'].mode()[0]

        print('\nThe earliest birth year: {}\nThe most recent birth year: {}\nThe most common birth year: {}'.format(earliest_birth_year, recent_birth_year,popular_birth_year))

    else: print('\nSorry! There is no Birth year information for this dataset')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# This function asks the user if they would like to view the raw data and displays 5 more lines of data each time the response is 'yes'
def display_data(city):

    filename = CITY_DATA.get(city)
    raw_data = pd.read_csv(filename)
    pd.options.display.max_rows = 400000

    data_rows = 5
    while True:
        Data_Display = (input("\nWould you like to view the raw data? Enter yes or no (Note: 5 extra rows of data will be displayed each time you say 'yes').\n"))
        if Data_Display.lower() != 'yes':
         break
        else: print(raw_data.head(data_rows))
        data_rows += 5


    # If the user was seen to try and view more than 50 rows in the previous segment (without stopping the user from viewing 5 rows at a time), the following segment asks the user if they would prefer to specify a number of rows from the raw dataset.

    if data_rows > 50:
        while True:
         specific_data_Display = (input("\nWoah that was a lot of data! Did you want to view a specific number of rows of data? Enter yes or no.\n"))
         if specific_data_Display.lower() != 'yes':
            break
         elif specific_data_Display == 'yes':
                specific_rownumber = int(input("\nHow many rows would you like to view?\n"))
                print(raw_data.head(specific_rownumber))
         else:
            break


# Calls functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,day,month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(city)

        # Asks the user if they would like to restart from the top
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
