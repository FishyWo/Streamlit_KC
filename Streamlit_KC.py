import streamlit as st
import datetime
import joblib
import pandas as pd

model = joblib.load('./models/GBR_KCHouseSalesMk1.pkl')

#Initialising session state variables
if 'predicted_value' not in st.session_state:
    st.session_state.predicted_value = 0
min_lat = [47.4816, 47.3942, 47.1593, 47.6021, 47.2574, 47.1559, 47.3866, 47.612]
max_lat = [47.7754, 47.6118, 47.4812, 47.7769, 47.4427, 47.7654, 47.6025, 47.7776]
min_long = [-122.134, -122.515, -122.174, -122.262, -122.519, -121.943, -122.267, -122.416]
max_long = [-121.868, -122.241, -121.867, -122.048, -122.174, -121.315, -122.035, -122.256]
bathroom_vals = []

class Features:
    def __init__(self, bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition, grade, sqft_above, sqft_basement, lat, long, sqft_living15, sqft_lot15, no_yrs_built, no_yrs_renovated, yr_sold, neighbourhood_0=0, neighbourhood_1=0, neighbourhood_2=0,neighbourhood_3=0,neighbourhood_4=0,neighbourhood_5=0,neighbourhood_6=0,neighbourhood_7=0):
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.sqft_living = sqft_living
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
        # self.neighbourhood_8 = neighbourhood_8
        # self.neighbourhood_9 = neighbourhood_9
        # self.neighbourhood_10 = neighbourhood_10
        # self.neighbourhood_11 = neighbourhood_11

    def return_object(self):
        # Convert the features to a dictionary
        return {
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'sqft_living': self.sqft_living,
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
        }
def predictModel():
    global predicted_value
    #Sum up all the bathrooms
    feature_input = Features(bedrooms, sum(bathroom_vals), (sqft_above+sqft_basement), sqft_lot, floors, int(waterfront), view, condition, grade, sqft_above, sqft_basement, lat, long, sqft_living15, sqft_lot15, no_yrs_built, no_yrs_renovated, yr_sold)
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
    neighbourhood = st.selectbox(label='Which neighbourhood', options=[i+1 for i in range(8)])
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
    st.button(label='Predict', on_click=predictModel())