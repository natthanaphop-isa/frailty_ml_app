"""
Created on Tuesday, March 7, 2566 BE (GMT+7) Time in Suthep, Mueang Chiang Mai District, Chiang Mai
@author: natthanaphop.isa """

import numpy as np
import pickle 
import streamlit as st

# Loading the saved model
loaded_model = pickle.load(open('/Users/natthanaphopisaradech/Documents/Data_Hub/frailty_ml_app/logistic_model_frailty.sav', 'rb'))

# Creating a function for Prediction 

def frailty_prediction(input_data):
    
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)

    if (prediction[0] == 0):
     return 'The person is ROBUST'
    else:
     return 'The person is FRAIL'
    
def main():
    # Giving a title
    st.title('Frailty Classification Using Machine Learning Web App')

    # Getting the input data from the user
    ## age
    age = st.number_input("Tell us about your age", step = 1)

    ## sex
    display = ("Male", "Female")
    options = [1,2]
    sex = st.selectbox("What is your sex?", options, format_func=lambda x: display[x])
    st.write(sex)

    ## Living Status
    display = ("Living Alone", "Not Living Alone")
    options = [1,0]
    stat = st.selectbox("Living Status: Do you live alone?", options, format_func=lambda x: display[x])
    st.write(stat)

    ##Underlying disease: Hypertension
    display = ("Yes", "No")
    options = [1,0]
    HT = st.selectbox("Do you have Hypertension?", options, format_func=lambda x: display[x])
    st.write(HT)

    ##Underlying disease: Hyperlipidemia
    display = ("Yes", "No")
    options = [1,0]
    lipid = st.selectbox("Do you have Hyperlipidemia?", options, format_func=lambda x: display[x])
    st.write(lipid)

    ##Anthropometric
    BMI = st.number_input("Body Mass Index (BMI: kg/m^2)")
    waistcir = st.number_input("Waist Circumference (cm)")
    calfcir = st.number_input("Calf Circumference (cm)")

    ##exhaustion
    display = ["0 = rarely or none of the time (<1 day)", 
    "1 = some or a little of the time (1–2 days)", 
    "2 = a moderate amount of the time (3–4 days)",
    "3 =most of the time"]
    options = [0,0,1,1]
    lipid = st.selectbox("Level of Exhaustion*", options, format_func=lambda x: display[x])
    st.wrtie("""*Using the CES–D Depression Scale, the following two statements are read. 
    (a) I felt that everything I did was an effort; 
    (b) I could not get going. 
    The question is asked “How often in the last week did you feel this way?” 
    """)

    # code for Prediction
    diagnosis = ''

    # Creating a botton for prediction 

    if st.botton("Frailty Test Result"):
       diagnosis = frailty_prediction([age,sex,stat,HT,lipid,BMI,waistcir,calfcir,exhaustion])

    st.success(diagnosis)

if __name__ == '__main__':
   main()