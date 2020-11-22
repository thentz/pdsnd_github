import time
import pandas as pd
import numpy as np

# original data files
CITY_DATA = { 'chi': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'wash': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    If valid city has not been entered after 3 attempts,
        return 'invalid'/'invalid'/'invalid'
    If a valid month has not been entered after 3 attempts, default to ALL
    If a valid day of week has not been entered after 3 attempts, default to ALL

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
        (str) day - name of the day of week to filter by, or "all"

    """
    print('Welcome. Let\'s explore Bikeshare data\
    \nAvailable cities: Chicago (CHI), New York City (NYC), Washington (WASH)\
    \nTimeframe: January (JAN) to June (JUN) 2017!')

    # Get user input for city (chicago, new york city, washington)
    valid_city = False
    counter = 0
    city = ''

    while not valid_city:
        if city in CITY_DATA:
            valid_city = True
        elif counter == 3:
            print('Maximum attempts reached')
            return 'invalid', 'invalid', 'invalid'
        else:
            city = str(input('Please enter the name of the city to analyze.\
                       \nEnter CHI for Chicago\
                       \nEnter NYC for New York City\
                       \nEnter WASH for Washington\
                       \nYou will be given 3 attempts.\n').lower())
            counter += 1

    # Get user input for month
    valid_month = False
    counter = 0
    month = ''
    months = ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']
    month_data = { 'jan': 'january',
             'feb': 'february',
             'mar': 'march',
             'apr': 'april',
             'may': 'may',
             'jun': 'june'}

    while not valid_month:
        if month in months:
            valid_month = True
        elif counter == 3:
            print('Maximum attempts reached. Default to ALL.')
            month = 'all'
            valid_month = True
        else:
            month = str(input('Please enter the month to analyze.\
                        \nYou may select ALL or one of the following:\
                        \n    JAN, FEB, MAR, APR, MAY, JUN\
                        \nAfter 3 attempts we will default to ALL\n').lower())
            month = month[0:3]
            counter += 1

    # Get user input for day of week
    valid_day = False
    counter = 0
    day = ''
    days = ['all', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    day_of_week_data = { 'sun': 'sunday',
                    'mon': 'monday',
                    'tue': 'tuesday',
                    'wed' : 'wednesday',
                    'thu' : 'thursday',
                    'fri' : 'friday',
                    'sat' : 'saturday'
                   }

    while not valid_day:
        if day in days:
            valid_day = True
        elif counter == 3:
            print('Maximum attempts exceeded. Default to ALL.')
            day = 'all'
            valid_day = True
        else:
            day = str(input('Please enter the day of week to analyze.\
                      \nYou may select ALL or one of the following:\
                      \n    SUN, MON, TUE, WED, THU, FRI, SAT\
                      \nAfter 3 attempts we will default to ALL\n').lower())
            day = day[0:3]
            counter += 1

    if month != 'all':
        month = month_data[month]

    if day != 'all':
        day = day_of_week_data[day]

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month/day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" (default)
        (str) day - name of the day of week to filter by, or "all" (default)

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # choose the .csv for selected city
    # filter for month - 'all' or the selected month
    # then filter for day - 'all' or the selected day of the week

    city_data = CITY_DATA[city]
    df = pd.read_csv(city_data)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    # for runtime statistics:
    start_time = time.time()

    # Display the most common month
    month_data = { 1: 'January',
                    2: 'February',
                    3: 'March',
                    4: 'April',
                    5: 'May',
                    6: 'June'
                     }

    month = df['month']
    most_common_month = month.mode()[0]
    most_common_month_count = month[month == most_common_month].count()
    most_common_month = month_data[most_common_month]

    print('\nThe most common month for travel is {} ({} trips)'
          .format(most_common_month, most_common_month_count))

    # Display the most common day of week
    day_of_week = df['day_of_week']
    most_common_day = day_of_week.mode()[0]
    most_common_day_count = day_of_week[day_of_week == most_common_day].count()

    print('\nThe most common day of the week for travel is {} ({} trips)'
          .format(most_common_day, most_common_day_count))

    # Display the most common start hour
    start_hour = df['Start Time'].dt.hour
    most_common_hour = start_hour.mode()[0]
    most_common_hour_count = start_hour[start_hour == most_common_hour].count()

    am_pm = ''
    if most_common_hour > 12:
        most_common_hour -=12
        am_pm = 'PM'
    else:
        am_pm = 'AM'

    print('\nThe most common hour to initiate travel is {}{} ({} trips)'
          .format(most_common_hour, am_pm, most_common_hour_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    # for runtime statistics:
    start_time = time.time()

    # Display most commonly used start station


    start_station = df['Start Station']
    most_common_start_station = start_station.mode()[0]
    most_common_start_count = start_station[start_station ==
                                            most_common_start_station].count()

    print('\nThe most common station for initiation of travel is {} ({} trips)'
          .format(most_common_start_station.title(), most_common_start_count))

    # Display most commonly used end station
    end_station = df['End Station']
    most_common_end_station = end_station.mode()[0]
    most_common_end_count = end_station[end_station ==
                                        most_common_end_station].count()

    print('\nThe most common station for completion of travel is {} ({} trips)'
          .format(most_common_end_station.title(), most_common_end_count))


    # Display most frequent combo start station/end station
 ##   df['Combo'] = df['Start Station'] + ' to ' + df['End Station']
    combo = df['Start Station'] + ' to ' + df['End Station']
    most_common_combo_station = combo.mode()[0]
    most_common_combo_count = combo[combo == most_common_combo_station].count()

    print('\nThe most frequent combination start/end station is {} ({} trips)'
          .format(most_common_combo_station, most_common_combo_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    # for runtime statistics:
    start_time = time.time()

    # Display total travel time
    # travel time format is in seconds so convert to H:M:S
    total_travel_time = df['Trip Duration'].sum()
    min, sec = divmod(total_travel_time, 60)
    hour, min = divmod(min, 60)

    print('\nThe total travel time is {}:{}:{} (H:M:S)'.format(hour, min, sec))

    # Display mean travel time in the filtered data
    # travel time format is in seconds so convert to H:M:S
    mean_travel_time = df['Trip Duration'].mean()
    min, sec = divmod(mean_travel_time, 60)
    hour, min = divmod(min, 60)

    print('\nThe average travel time is {:.0f}:{:.0f}:{:.2f} (H:M:S)'
          .format(hour, min, sec))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    # for runtime statistics:
    start_time = time.time()

    # Display the total number of users in the filtered data
    total_users = df['Start Time'].count()
    print('\nThe total number of users in the analyzed data is {}'
          .format(total_users))


    # Display counts of user types
    # User Type is not available for all records - count missing info
    user_type = df.groupby('User Type')['User Type'].count()

    print('\nNumber of Users by User Type: {}'.format(user_type))

    user_type = df['User Type']
    no_user_type_avail = user_type.isnull().sum().sum()
    print('\nThere is no user type available for {} users'
          .format(no_user_type_avail))


    # Display counts of gender in the filtered data
    # not all cities have gender information
    # Gender is not available for all records -count missing info
    if 'Gender' in df.columns:
        gender_group = df.groupby('Gender')['Gender'].count()
        print('\nNumber of Users by Gender: {}'.format(gender_group))
        gender = df['Gender']
        no_gender_avail = gender.isnull().sum().sum()
        print('\nThere is no gender available for {} users'
              .format(no_gender_avail))
    else:
        print('\nAnalysis by Gender is not available for the selected city')


    # Display earliest, most recent, and most common year of birth
    # not all cities have birth year information
    # Birth Year is not available for all records - count missing info
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        birth_year_youngest = birth_year.max()
        birth_year_oldest = birth_year.min()
        birth_year_common = birth_year.mode()[0]
        birth_year_common_count = birth_year[birth_year ==
                                             birth_year_common].count()
        no_birth_year_avail =  birth_year.isnull().sum().sum()
        print('\nThe oldest user was born in: {:.0f}'.format(birth_year_oldest))
        print('\nThe youngest user was born in: {:.0f}'
              .format(birth_year_youngest))
        print('\nThe most common birth year for users is: {:.0f} ({} users)'
              .format(birth_year_common, birth_year_common_count))
        print('\nThere is no birth year available for {} users'
              .format(no_birth_year_avail))
    else:
        print('\nAnalysis by Birth Year is not available for the selected city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()

        if city == 'invalid':
            print('\nInvalid City entered. You will need to begin again.\n')
            break

        df = load_data(city, month, day)
        city_data = { 'chi': 'chicago',
                    'nyc': 'new york city',
                    'wash': 'washington'
                   }

        city = city_data[city]

        print('Analyzing data for City: {}, Month: {}, Day of Week: {}'
              .format(city.title(), month.title(), day.title()))

        index = df.index
        number_of_rows = len(index)
        print('Number of records analyzed: ', number_of_rows)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        see_raw = input('\nWould you like to see the raw data?' +
                  '\nData will be displayed 5 rows at a time.' +
                  '\nEnter YES or NO.' +
                  '\nThe default is NO - press Enter to accept.\n')
        counter = 0
        while see_raw == 'yes':
            print(df[counter: counter + 5])
            counter += 5
            see_raw = input('\nWould you like to see more raw data?' +
                      '\nEnter YES or NO.' +
                      '\nThe default is NO - press Enter to accept.\n')

        restart = input('\nWould you like to restart? \nEnter YES or NO.\
                  \nThe default is NO - press Enter to accept.\n')
        if restart.lower() != 'yes':
            print('\nExiting now. \nThank you for using our system.' +
                  '\nIf you would like additional analysis, please restart.\n')
            break


if __name__ == "__main__":
	main()




pwd
