import streamlit as st
import datetime
import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

model = joblib.load(r'./models/GBR_KCHouseSalesMk1.pkl')

#Initialising session state variables
if 'predicted_value' not in st.session_state:
    st.session_state.predicted_value = 0
min_lat = [47.6256, 47.1593, 47.5380, 47.3942, 47.2574, 47.6480, 47.1559, 47.4824, 47.6394, 47.2558, 47.4142, 47.4545]
max_lat = [47.7776, 47.4536, 47.6760, 47.5935, 47.4396, 47.7769, 47.7654, 47.6515, 47.7759, 47.4143, 47.5473, 47.6609]
min_long = [-122.416, -122.113, -122.225, -122.515, -122.519 , -122.286, -121.924, -122.327, -122.124, -122.243 , -122.283, -122.094]
max_long = [-122.263, -121.867, -122.088, -122.277, -122.244, -122.118, -121.315, -122.211, -121.857, -122.105, -122.063, -121.892]
bathroom_vals = []

class Features:
    def __init__(self, bedrooms, bathrooms, sqft_lot, floors, waterfront, view, condition, grade, sqft_above, sqft_basement, lat, long, sqft_living15, sqft_lot15, no_yrs_built, no_yrs_renovated, yr_sold, neighbourhood_0=0, neighbourhood_1=0, neighbourhood_2=0,neighbourhood_3=0,neighbourhood_4=0,neighbourhood_5=0,neighbourhood_6=0,neighbourhood_7=0,neighbourhood_8=0,neighbourhood_9=0,neighbourhood_10=0,neighbourhood_11=0):
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.sqft_lot= sqft_lot
        self.floors= floors
        self.waterfront = waterfront
        self.view = view
        self.condition = condition
        self.grade = grade
        self.sqft_above = sqft_above
        self.sqft_basement = sqft_basement
        self.lat = lat
        self.long = long
        self.sqft_living15 = sqft_living15
        self.sqft_lot15 = sqft_lot15
        self.no_yrs_built = no_yrs_built
        self.no_yrs_renovated = no_yrs_renovated
        self.yr_sold = yr_sold
        self.neighbourhood_0 = neighbourhood_0
        self.neighbourhood_1 = neighbourhood_1
        self.neighbourhood_2 = neighbourhood_2
        self.neighbourhood_3 = neighbourhood_3
        self.neighbourhood_4 = neighbourhood_4
        self.neighbourhood_5 = neighbourhood_5
        self.neighbourhood_6 = neighbourhood_6
        self.neighbourhood_7 = neighbourhood_7
        self.neighbourhood_8 = neighbourhood_8
        self.neighbourhood_9 = neighbourhood_9
        self.neighbourhood_10 = neighbourhood_10
        self.neighbourhood_11 = neighbourhood_11

    def return_object(self):
        # Convert the features to a dictionary
        return {
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'sqft_lot': self.sqft_lot,
            'floors': self.floors,
            'waterfront': self.waterfront,
            'view': self.view,
            'condition': self.condition,
            'grade': self.grade,
            'sqft_above': self.sqft_above,
            'sqft_basement': self.sqft_basement,
            'lat': self.lat,
            'long': self.long,
            'sqft_living15': self.sqft_living15,
            'sqft_lot15': self.sqft_lot15,
            'no_yrs_built': self.no_yrs_built,
            'no_yrs_renovated': self.no_yrs_renovated,
            'yr_sold': self.yr_sold,
            'neighbourhood_0': self.neighbourhood_0,
            'neighbourhood_1': self.neighbourhood_1,
            'neighbourhood_2': self.neighbourhood_2,
            'neighbourhood_3': self.neighbourhood_3,
            'neighbourhood_4': self.neighbourhood_4,
            'neighbourhood_5': self.neighbourhood_5,
            'neighbourhood_6': self.neighbourhood_6,
            'neighbourhood_7': self.neighbourhood_7,
            'neighbourhood_8': self.neighbourhood_8,
            'neighbourhood_9': self.neighbourhood_9,
            'neighbourhood_10': self.neighbourhood_10,
            'neighbourhood_11': self.neighbourhood_11
        }
def predictModel():
    global predicted_value
    #Sum up all the bathrooms
    feature_input = Features(bedrooms, sum(bathroom_vals), sqft_lot, floors, int(waterfront), view, condition, grade, sqft_above, sqft_basement, lat, long, sqft_living15, sqft_lot15, no_yrs_built, no_yrs_renovated, yr_sold)
    setattr(feature_input, f'neighbourhood_{int(neighbourhood)-1}', 1)
    feature_input = pd.DataFrame(feature_input.return_object(), index=[0])
    print(feature_input)
    st.session_state.predicted_value = model.predict(feature_input)

st.title('King County House Sales')

col1, col2, col3 = st.columns(3)

with col1:
    bedrooms = st.number_input(label='Number of Bedrooms', max_value=50)
    floors = st.slider(label='Number of floors', min_value=0.0, max_value=5.0, step=0.5)
    waterfront = st.checkbox(label='Waterfront', value=[1,0])
    view = st.slider(label='view', min_value=0, max_value=4)
    condition = st.slider(label='Condition of the apartment', min_value=1, max_value=5)
    grade = st.slider(label='Grade of Construction and Design', min_value=1, max_value=13)
    neighbourhood = st.selectbox(label='Which neighbourhood', options=[i+1 for i in range(12)])
    lat = st.number_input(label='lat', min_value=min_lat[neighbourhood-1],max_value=max_lat[neighbourhood-1], step=0.0001, format='%.4f')
    long = st.number_input(label='long', min_value=min_long[neighbourhood-1],max_value=max_long[neighbourhood-1], step=0.001, format='%.3f')

with col2:
    sqft_above = st.number_input(label='Land space above ground level', max_value=2000000)
    sqft_basement = st.number_input(label='Land space below ground level', max_value=2000000)
    st.write(sqft_above+sqft_basement)
    sqft_lot = st.number_input(label='Land space(Sqft)', max_value=2000000)
    sqft_living15 = st.number_input(label='Average interior living space for 15 neighbours', max_value=2000000)
    sqft_lot15 = st.number_input(label='Average land space for 15 neighbours', max_value=2000000)
    no_yrs_built = st.number_input(label='How old the building is', min_value=0, max_value=100)
    no_yrs_renovated = st.number_input(label='How old the renovation is', min_value=0, max_value=100)
    yr_sold = st.selectbox(label='The year the building is sold', options=[year for year in range(1990,datetime.datetime.now().year+11)])
bathrooms_cont = st.container()
with bathrooms_cont:
    bathrooms = st.slider(label='Bathrooms', min_value=1, max_value=12, step=1)
    if bathrooms<=6:
        bathroom_cols = st.columns(bathrooms)
        for i in range(bathrooms):
            with bathroom_cols[i]:
                bathroom_vals.append(st.number_input(label=f'Bathroom {i+1}', min_value=0.0, max_value=1.0, step=0.25))
    else:
        bathroom_cols1 = st.columns(bathrooms//2)
        bathroom_cols2 = st.columns(bathrooms-(bathrooms//2))
        for i in range(bathrooms//2):
            with bathroom_cols1[i]:
                bathroom_vals.append(st.number_input(label=f'Bathroom {i+1}', min_value=0.0, max_value=1.0, step=0.25))
        for i in range(bathrooms-(bathrooms//2)):
            with bathroom_cols2[i]:
                bathroom_vals.append(st.number_input(label=f'Bathroom {i+7}', min_value=0.0, max_value=1.0, step=0.25))

with col3:
    st.write(st.session_state.predicted_value)
    st.button(label='Predict', on_click=predictModel)
