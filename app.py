# Created on Tuesday, March 7, 2566 BE (GMT+7) Time in Suthep, Mueang Chiang Mai District, Chiang Mai
# @author: natthanaphop.isa

import numpy as np
import pickle
import streamlit as st

# Loading the saved model
with open('logistic_model_frailty.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Creating a function for Prediction
def frailty_prediction(input_data):
    # Changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # Reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = loaded_model.predict(input_data_reshaped)

    if prediction[0] == 0:
        return 'You have a LOW probability of becoming FRAIL.'
    else:
        return 'You have a HIGH probability of becoming FRAIL. We suggest that you should meet with a doctor for early exercise and nutrition interventions.'

def main():
    # Giving a title
    st.title('Frailty Classification Using Machine Learning Model - Web App')

    # Define the format function
    def format_func(option, choices):
        return choices[option]

    # Getting the input data from the user
    age = st.number_input("Tell us about your age", step=1)

    sex_choices = {1: "Male", 2: "Female"}
    sex = st.selectbox("What is your sex?", options=list(sex_choices.keys()), format_func=lambda x: format_func(x, sex_choices))

    stat_choices = {1: "Living Alone", 0: "Not Living Alone"}
    stat = st.selectbox("Living Status: Do you live alone?", options=list(stat_choices.keys()), format_func=lambda x: format_func(x, stat_choices))

    HT_choices = {1: "Yes", 0: "No"}
    HT = st.selectbox("Do you have Hypertension?", options=list(HT_choices.keys()), format_func=lambda x: format_func(x, HT_choices))

    lipid_choices = {1: "Yes", 0: "No"}
    lipid = st.selectbox("Do you have Hyperlipidemia?", options=list(lipid_choices.keys()), format_func=lambda x: format_func(x, lipid_choices))

    BMI = st.number_input("Body Mass Index (BMI: kg/m^2)")
    waistcir = st.number_input("Waist Circumference (cm)")
    calfcir = st.number_input("Calf Circumference (cm)")

    exhaustion_choices = {
        0: "0 = rarely or none of the time (<1 day)",
        1: "1 = some or a little of the time (1–2 days)",
        2: "2 = a moderate amount of the time (3–4 days)",
        3: "3 = most of the time"
    }
    exhaustion = st.selectbox("Level of Exhaustion*", options=list(exhaustion_choices.keys()), format_func=lambda x: format_func(x, exhaustion_choices))

    if exhaustion <= 1:
        exhaustion = 0
    else:
        exhaustion = 1

    st.write("""
    *Read the following two statements and answer the question:
    (a) I felt that everything I did was an effort; 
    (b) I could not get going. 
    Question: “How often in the last week did you feel this way?”
    """)

    # Code for Prediction
    diagnosis = ''

    # Creating a button for prediction
    if st.button("Frailty Test Result"):
        diagnosis = frailty_prediction([age, sex, stat, HT, lipid, BMI, waistcir, calfcir, exhaustion])
        st.success(diagnosis)

if __name__ == '__main__':
    main()
