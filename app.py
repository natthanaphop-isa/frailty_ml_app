"""
Created on Tuesday, March 7, 2566 BE (GMT+7) Time in Suthep, Mueang Chiang Mai District, Chiang Mai
@author: natthanaphop.isa """

import numpy as np
import pickle 
import streamlit as st

# Loading the saved model
loaded_model = pickle.load(open('logistic_model_frailty.pkl', 'rb'))

# Creating a function for Prediction 

def frailty_prediction(input_data):
    
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)

    if (prediction[0] == 0):
     return f'You have a LOW probability of frailty. We suggest that you should continue your lifestyle and do not forget to exercise and eat well! :D'
    else:
     return 'You have a HIGH probability of frailty. We suggest that you should meet with a doctor for early exercise and nutrition interventions.'
    
def main():
    # Giving a title
    st.title('Frailty Classification Using Machine Learning Web App')
    def format_func(option):
        return CHOICES[option]
    # Getting the input data from the user
    ## age
    age = st.number_input("Tell us about your age", step = 1)

    ## sex
    CHOICES = {1: "Male", 2: "Female"}
    sex = st.selectbox("What is your sex?", options=list(CHOICES.keys()), format_func=format_func)
    st.write(f"You selected: {format_func(sex)}")
    #st.write(sex)

    ## Living Status
    CHOICES = {1: "Living Alone", 0:"Not Living Alone"}
    stat = st.selectbox("Living Status: Do you live alone?", options=list(CHOICES.keys()), format_func=format_func)
    st.write(f"You selected: {format_func(stat)}")
    #st.write(stat)

    ##Underlying disease: Hypertension
    CHOICES = {1: "Yes", 0:"No"}
    HT = st.selectbox("Do you have Hypertension?", options=list(CHOICES.keys()), format_func=format_func)
    st.write(f"You selected: {format_func(HT)}")
    #st.write(HT)

    ##Underlying disease: Hyperlipidemia
    CHOICES = {1: "Yes", 0:"No"}
    lipid = st.selectbox("Do you have Hyperlipidemia?", options=list(CHOICES.keys()), format_func=format_func)
    st.write(f"You selected: {format_func(lipid)}")
    #st.write(lipid)

    ##Anthropometric
    BMI = st.number_input("Body Mass Index (BMI: kg/m^2)")
    waistcir = st.number_input("Waist Circumference (cm)")
    calfcir = st.number_input("Calf Circumference (cm)")

    ##exhaustion
    CHOICES = {0:"0 = rarely or none of the time (<1 day)", 1:"1 = some or a little of the time (1–2 days)", 2: "2 = a moderate amount of the time (3–4 days)", 3:"3 =most of the time"}
    exhaustion = st.selectbox("Level of Exhaustion*", options=list(CHOICES.keys()), format_func=format_func)
    #st.write(f"You selected: {format_func(exhaustion)}")
    if exhaustion <=1:
       exhaustion = 0
    else:
       exhaustion = 1
    #st.write(exhaustion)
    st.write("""*Using the CES–D Depression Scale, the following two statements are read. 
    (a) I felt that everything I did was an effort; 
    (b) I could not get going. 
    The question is asked “How often in the last week did you feel this way?” 
    """)

    # code for Prediction
    diagnosis = ''

    # Creating a botton for prediction 

    if st.button("Frailty Test Result"):
       diagnosis = frailty_prediction([age,sex,stat,HT,lipid,BMI,waistcir,calfcir,exhaustion])

    st.success(diagnosis)

if __name__ == '__main__':
   main()
