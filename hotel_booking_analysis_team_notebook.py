# -*- coding: utf-8 -*-
"""Hotel Booking Analysis-Team_notebook

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gg0Xlqxhmg2od2XQz_rkYiTm1YQMqlXG

#**Exploratary Data Analysis(EDA) on Hotel Bookings**

## **Importing Libraries**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

import seaborn as sns

from datetime import datetime
from datetime import date

import warnings
warnings.filterwarnings('ignore') #Used when finding the outliers

from google.colab import drive
drive.mount('/content/drive')

# Enabling the Google drive access
# Created filepath directory

path="/content/drive/MyDrive/Almabetter/Python for data science/Python Projects /EDA capstone project 1/Hotel Bookings (1).csv"
df=pd.read_csv(path)

"""## **Data Understanding**

* Data understanding focuses on the comprehension of the information available in the project.

"""

df.shape

df.head(5)

list(df.columns)

df.describe()

"""## **Variables and their meaning in the dataframe.**

**hotel**
* Provided Hotel type 
* Resort or City hotel

**is_canceled**
* Value provided information about cancellation by customer.
* If canceled = 1
* If not canceled = 0

**lead_time**
* The Booking Lead Time is the *number of days* between the time a guest books their room and the time they are scheduled to arrive at the hotel.


**arrival_date_year**
* Year of arrival of the Customer.

**arrival_date_week_number**
* week number of arrival of the Customer.

**arrival_date_day_of_month**
* Month of arrival of the Customer.

**stays_in_weekend_nights**
* Number of weekend nights (Saturday night or Sunday night) the guest stayed or booked to stay at the hotel.

**stays_in_week_nights**
* Number of week nights (Monday to Friday) the guest stayed or booked to stay at the hotel.

**adults**
* Number of adults stayed or booked to stay at the hotel

**children**
* Number of children stayed or booked to stay at the hotel

**babies**
* Number of babies stayed or booked to stay at the hotel

**meal**
* Type of meals Booked.
   - BB: Bed & Breakfast

  - HB: Half Board (Breakfast and Dinner normally)

  - FB: Full Board (Beakfast, Lunch or Dinner)

  - Undefined/SC: Rooms only packages without meals.

**countries**
* Country of origin of the customer.
* Country name provided based on ISO 3166 country codes.

**market_segment**
* Market segment distinction
* Provides source of information through which customer booked
* Term "TA" - "Travel Agent"
* Term "TO" - "Tour operators" 
* Both "TA" and "TO" considers as same kind of market segment.

**distribution_channel**
* also called "marketing channel"
* Is the Network through which customer booked.

**is_repeated_guest**
* Value provided information about whether the customer is new or old.
* If new to the hotel = 1
* If not new to the hotel = 0

**previous_cancellations**
* Number of bookings previously canceled by the customer, Before current booking.

**previous_bookings_not_canceled**
* Number of bookings previously not canceled by the customer, Before current booking.

**reserved_room_type** 
* Type of room reserved stored in alphabat codes.

**assigned_room_type**
* Type of room reserved stored in alphabat codes.

**booking_changes**
* Number of changes made to the booking until check-in or completely canceled.

**deposit_type**
* The purpose of the advance deposit is to guarantee a reservation
* There are 3 types of deposit,
 * 'No Deposit' - No deposit need by the hotel on booking
 * 'Refundable' - Deposit that can be refunded while vacating the room, Which included in total Room-stay cost.
 * 'Non Refundable' - Amount paid that can't be refunded once paid  Which included in total Room-stay cost.

**agent**
 * Unique ID code of the Travel agent through which booking made.

**company**
* Unique ID code of the company or entity who made booking and responsible for payment.

**days_in_waiting_list**
* Number of days the booking was in the waiting list before it was confirmed to the customer.

**customer_type**
  * 'Transient' - Simply individual guests requiring a short stay at the hotel
  * 'Contract' - Agreement between hotel authority and customer to requiring volume room bookings on contract basis.
  * 'Transient-Party' - Booking is Transient and associated with other transient booking
  * 'Group' - Multiple rooms are booked under single customer responsibility

**adr**
  * The Average Daily Rate (ADR) is the price to be paid by customer for staying per day/night in the room.

**required_car_parking_spaces**
* Number of vehicle space requested by customer while booking.

**total_of_special_requests**
* Total number of special request made by customer while booking.

**reservation_status**
* Reservation status when data created.
* It stored in three types:
  * 'Check-Out' - Customer already vacated from the room booked.
  * 'Canceled' - Booking was canceled by the customer.
  * 'No-Show' -  Room was booked, yet customer neither 'Checked-in' nor 'Canceled'

**reservation_status_date**
* Date on which reservation_status checked

#**Data Cleaning**  - Cleaning / Filling Missing Data.

1.   List item


###**Checking for null values in each columns:**
"""

# Finding the total number of null values in the each variables or column.

df.isnull().sum()
A = df.isnull().sum()
print(A)

# Finding the percentage of Null values in each variables.

B = df.isnull().sum()/len(df.index)* 100
print(B)

# Concat both series we found.

df_nulldata = pd.concat([A,B] , axis = 1, keys = ["null_values","percentage of null values"])
df_nulldata

"""##**Dropping columns with high null values**

* From the above observation, we found the percentage's of null values highest in "agent" and "company" columns.
* Now, Dropping those columns with the highest number of null value as part of data cleaning

"""

# Before droping it was 32 columns in df.
df.shape

# Dropping 

df.drop(["agent","company"], axis =1 , inplace = True)

# After droping it is 30 columns in df.
df.shape

# To virtually find the further null values that exist in the dataframe.

sns.heatmap(df.isnull(),yticklabels=False,cbar=False,cmap='plasma')
plt.figure(figsize = (10,5))

"""* Still variables "children" and "country" has some mininum number of the null values
* Hence, filling those null values with appropriate values.
* That is,
 * Filling the null values in the children column as "0" 
 * Filling the null values in the country with country name which has maximum count in the data.
"""

# For children

df["children"].isnull().value_counts()

# Filling those 4 cell with "0"

df["children"] = df["children"].fillna(0)

#checking 

df["children"].isnull().value_counts()

# For country

df["country"].isnull().value_counts()

# finding the country from which most number of customer booked.
# so that filling the null value of country column with that country code.
df["country"].mode()

# Filling null values in the country with "PRT"

df["country"].fillna("PRT", inplace = True)

#Checking

df["country"].isnull().value_counts()

"""#### Now, all the columns are filled with non-null values.

#### Let us now deal with the dtype of each variable, if need convert it to appropriate one.
"""

# Date values in the "reservation_status_date" is in object
# hence converting it to datetime format
df["reservation_status_date"]

"""## Converting object into datetype in "reservation_status_date"         """

df["new_reservation_status_date"] = df["reservation_status_date"].apply(lambda x : datetime.strptime(x, "%Y-%m-%d"))
df["new_reservation_status_date"]

"""## Converting the dtype of column "babies" into int"""

df["babies"].astype(int)

"""### Creating the New set of dataframe in which no rows have value "0" in number of adults, children, babies."""

df = df[~((df["adults"]) == 0 & (df["children"] ==0) & (df["babies"] == 0))]
df

# Actual shape of the dataframe reduced.
df.shape

"""## Finding the Outliers of each variable.
#### This helps to clean the data futher by observing the upper and lower limit.
"""

# Virtualization of the each variables
# Using for loop to iterate on each.
n=1
plt.figure(figsize=(12,15))
for i in range(31):
  if df.iloc[:,i].dtype == int or df.iloc[:,i].dtype== float:
    plt.subplot(6,3,n)
    n+=1
    sns.boxplot(df.iloc[:,i])
    plt.tight_layout();

"""* The above distribution provides the information about the outliers
* hence, upper and lower Quartile limit can be fixed 
* Dataframe can be further cleaned for analysis.

## With the help of above outliers, cleaning the data based on Quartile value.
"""

df = df.loc[df['lead_time'] < df['lead_time'].quantile(0.99)]
df = df.loc[df['stays_in_weekend_nights'] < df['stays_in_weekend_nights'].quantile(0.99)]
df = df.loc[df['stays_in_week_nights'] < df['stays_in_week_nights'].quantile(0.99)]
df = df.loc[df['adults'] < 5]
df = df.loc[df['children'] < 3]
df = df.loc[df['babies'] < 3]
df = df.loc[df['required_car_parking_spaces'] < 4]
df = df.loc[df['adr'] < 700]

df.shape

"""##**Data validation and Publishing**

### **Univariable study:**

##1. Number of Bookings in each Hotel type
"""

hotel = df["hotel"].value_counts()
hotel.plot(kind = "bar")

plt.title('Numbers of hotels in each type')
plt.ylabel('Total hotels')
plt.xlabel('Types of Hotel')

plt.rcParams['figure.figsize'] = (10, 5)

"""Observation:
* Customer prefered City Hotel more than Resort Hotel

##2. Length of stay in each hotel type Box plot
"""

#getting length of stay
df['length_of_stay']=df['stays_in_weekend_nights']+df['stays_in_week_nights']
df['length_of_stay'].tail()+df

#Box plot for length of stay according to Hotel type
plt.figure(figsize=(10,5))
ax = sns.boxplot(x="length_of_stay", y="hotel", data=df, orient="h")
ax.set_title('Length of stay for type of hotels',fontsize = 20)
ax.set_xlabel("Length of stay", fontsize = 15)
ax.set_ylabel("Type of Hotel", fontsize = 15)

"""Observation
*   If we ignore the outliers, the maximum length of stay is more in resort type as resort is mostly used for vacation purpose.
* Median of both the hotels are approximately equal.

##3. Number of Booking month-wise
"""

monthly_data = df["arrival_date_month"].value_counts().reset_index(drop = False)
monthly_data = monthly_data.set_index("index")
monthly_data = monthly_data.sort_values( by = "arrival_date_month", ascending = False)
print(monthly_data)

monthly_data.plot(kind = "bar")
plt.title('Monthly booking details')
plt.xlabel('Months')
plt.ylabel('No.of Customers');

"""Obervation:
* Bookings in August is highest 
* January found lowest numbers in booking counts.

##4. ADR for each hotel type according to year (Line Plot)
"""

adr_year = df.groupby(['arrival_date_year','hotel'])['adr'].mean().unstack()  #arranging mean adr for city and resort hotel according to year
adr_year

#line plot of adr year wise
adr_year.plot()

plt.title('ADR time series for resort and city hotel')
plt.ylabel('Mean ADR')
plt.xlabel('Year')
plt.rcParams['figure.figsize'] = (11, 5)

"""Observation:
* City hotels has always higher (adr) than resort hotel.
* If the trend continues like that, resort hotel (adr) showing maximum increased inclination which means in few years resort hotel adr will cross the city hotel.

##5. Average daily rates(adr) for both hotels in every month
"""

plt.figure(figsize=(15,6))
sns.lineplot(data = df, x = 'Average_daily_rate', y = 'adr', hue = 'hotel').set_title('Average daily rates for both hotels in every Month')
plt.tight_layout();

"""Observation:
* In the month of July and till the last week of August Resort hotels received more "adr" than City hotel
* City hotel although dominating in 'adr' in remaining months of the year.

##6. Stays in weekend and weekdays in hotels vs Bookings
"""

stay = df[["stays_in_week_nights","stays_in_weekend_nights"]].value_counts()
stay.plot(kind = "bar");

"""Observation:
* Maximum Booking done by customer for "2" weeknights stay and "0" weekend nights 
"""

# On further observation
stay = df[["stays_in_week_nights","stays_in_weekend_nights"]].mean()
stay.plot(kind = "bar");

"""Observation:
* On average, customers booking for 2-3 week-nights stay and 1 weekend-nights stay

##7. Count of adults,children,babies in booking
"""

fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize = (15, 5))
sns.countplot(df['adults'],ax=ax1)
ax1.title.set_text('No.of adults')

sns.countplot(df['children'],ax=ax2)
ax2.title.set_text('No. of children')

sns.countplot(df['babies'],ax=ax3)
ax3.title.set_text('No. of babies')

"""Observation:
* Bookings are mostly made for 2 adults with 1 children in combination

##8. Preference of the meal by customer
"""

plt.figure(figsize=(10,6))
df["meal"].value_counts().plot(kind = "bar")
plt.title('Preferred Meal')
plt.xlabel('Meal type')
plt.ylabel('count');

"""Observation:
* Customers of any type preferring "BB" Bed and breakfast type of meals.

##9. Top 10 country of origin of customer
"""

df["country"].value_counts()[0:10].plot(kind='bar')

plt.title('Top 10 origin country of customer')
plt.xlabel('Countries')
plt.ylabel('No.of Customers');

"""Observation:
* It should be noted that more number of bookings done by customer from country PRT(Portugal)

##10. Market_segment and bookings
"""

plt.figure(figsize=(10,6))
sns.countplot(df['market_segment'],order=pd.value_counts(df['market_segment']).index,hue=df['hotel'],palette='Set2')
plt.title('Bookings by market-segment');

"""Observation:
* Travel agency (TA) or Tour operator (TO) Plays vital role in Hotel booking
* Except "Direct bookings", all market-segment has more number of bookings in  city hotel type.

##11. Number of Weekdays booked vs market segment
"""

plt.figure(figsize=(12,6))
sns.boxplot(x = "market_segment", y = "stays_in_week_nights", data = df, hue = "hotel", palette = 'Set3');
plt.title('No of weekdays Vs Markert segment')
plt.ylabel('Stays in week nights')
plt.tight_layout()

"""Observation:
* Customer from direct market segment staying in same range numbers of week nights.
* Offline TA/TO and Group market segment has some deviation over stays week-nights between Resort and City hotels
* Undefined and Aviation market segment customer had not shown interest in the Resort Hotel

##12. Number of Weekend nights booked vs market segment
"""

plt.figure(figsize=(12,6))
sns.boxplot(x = "market_segment", y = "stays_in_weekend_nights", data = df, hue = "hotel", palette = 'Set3');
plt.title('No of weekend night Vs Markert segment')
plt.ylabel('Stays in weekends nights')
plt.tight_layout()

"""Observation:
* Direct market segment customer prefer to stay more weekend nights in the Resort Hotel type.
* Online TA customer equally preferring between Resort and City hotels.

##13. Total special request in each type of market segment
"""

total_special_request=df.groupby(['market_segment'])['total_of_special_requests'].sum(). #arranging total special request for each market segment
total_special_request

# Create the figure object for total special request
histogram_special_request=total_special_request.plot.bar(figsize = (10,6),fontsize = 14)

# Set the title
histogram_special_request.set_title("Total Special requests in each market segment type", fontsize = 20)

# Set x and y-labels
histogram_special_request.set_xlabel("Market segment type", fontsize = 15)
histogram_special_request.set_ylabel("Total special requests", fontsize = 15)

"""##14. Preference of Room types by customer"""

plt.figure(figsize=(10,6))
df["reserved_room_type"].value_counts().plot(kind = "bar")
plt.title('Preference of Room types by customer')
plt.xlabel('Types of Room types')
plt.ylabel('No. of Bookings');

"""Observation:
* Room type of "A" preferred mostly by customers
* Also it should be note the maximum numbers of booking done in the rooms type of A,D,E than others with minimum number of bookings

##15. Rooms assigned to customer vs Rooms Reserved by the customer
"""

relation = pd.crosstab(index=df['reserved_room_type'],columns=df['assigned_room_type'],normalize='index',margins=True).round(2)*100

relation

"""Obsertion:
*  From crosstab, relationship of reserved and assigned rooms found.
* Hotel ensured that, 97.0 % of Customer getting the same room type as reserved in room type "G" and "H"
* Lowest possibility of getting the same room type when reserved in room type "L"
* AS we know, maximum number of booking done for room type "A" which ensured 85.0% of same room as reserved by the customer

##16. Total previous cancellation and not cancellation in each hotel type
"""

number_of_cancel=df.groupby(['hotel'])['previous_cancellations'].sum()
number_of_notcancel=df.groupby(['hotel'])['previous_bookings_not_canceled'].sum()

# Create the figure object for cancel number
cancel_number= number_of_cancel.plot.bar(figsize = (10,6),fontsize = 14)

# Set the title
cancel_number.set_title("Total previous cancellation", fontsize = 20)

# Set x and y-labels
cancel_number.set_xlabel("Hotel type", fontsize = 15)
cancel_number.set_ylabel("Total previous cancellations", fontsize = 15)

# Create the figure object for not canceled 
notcancel_number= number_of_notcancel.plot.bar(figsize = (10,6),fontsize = 14)

# Set the title
notcancel_number.set_title("Total of not cancelled previously", fontsize = 20)

# Set x and y-labels
notcancel_number.set_xlabel("Hotel type", fontsize = 15)
notcancel_number.set_ylabel("Sum of not cancelled previously", fontsize = 15)

"""* Total number of previously not cancelled booking is more in city hotel than a resort hotel.
* The city hotel is used more frequently compared to resort hotel thus the canceled and not canceled booking will be more in city hotel.

##17. waiting time vs cancellation
"""

(sns.FacetGrid(df, hue = 'is_canceled',height = 5, xlim = (0,100)).map(sns.kdeplot, 'days_in_waiting_list', shade = True).add_legend());

"""Obervation:
* As found from the density,
* Increase in days in waiting list increasing the cancellation of the booking

##18. Total cancellations for each hotel type
"""

total_cancellation=df.groupby(['hotel'])['is_canceled'].sum()  #total number of cancellation for each type of hotel
total_bookings=df['hotel'].value_counts(). #total number of bookings for each type of hotel

#percentage of total_cancellation for both the bookings 
percentage_of_cancellation=np.round(total_cancellation*100/total_bookings,2)
print(f"percentage of cancellation=\n{percentage_of_cancellation}")

# Create pie chart for total cancellation
bar_cancellation=total_cancellation.plot.pie(figsize = (10,6),fontsize = 14)

# Set the title
bar_cancellation.set_title("Total cancellations for each hotel type", fontsize = 20)

"""*   Percentage cancellation in city hotel is 41.09%.
*   Percentage cancellation in resort hotel is 27.66%

##19. Required Parking spaces vs hotel type
"""

plt.figure(figsize=(12,6))
sns.countplot(x="required_car_parking_spaces", data = df,hue='hotel')
plt.title('Required paking spaces for hotel type');

"""Observation:
* Mostly customers not demanding parking space.
* If demanding means, mostly in the number "1", that too maximum required in the Resort hotel.

##20. Sum of parking space according to type of booking
"""

total_parking=df.groupby(['customer_type'])['required_car_parking_spaces'].sum()
total_parking

# Create the figure object for total_parking
bar_parking=total_parking.plot.bar(figsize = (10,6),fontsize = 14)

# Set the title
bar_parking.set_title("Total parking space required for customer type", fontsize = 20)

# Set x and y-labels
bar_parking.set_xlabel("Customer type", fontsize = 15)
bar_parking.set_ylabel("Total of Parking space required", fontsize = 15)

"""* When customer type is Transient that means the stay is more few days so it is possible that customer bringing his/her own vehicle that's why the parking space required it high for Transient
* In contract and group booking customer will probably take a hired vehicle form hotel or from somewhere else that's why they do not need parking space.
"""