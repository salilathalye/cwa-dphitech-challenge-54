# app.py
# Streamlit application for serving a Machine Learning Model
# Salil Athalye

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import pycaret
import streamlit as st
from pycaret.regression import load_model, predict_model

# TODO: We could have a list of models saved in a JSON file, allow user to pick one
# For now. use Catboost
MODEL_CATBOOST = "dphi_ch54_1_catboost"
MODEL_PATH = "models/" + MODEL_CATBOOST


def main():
    # print(f"Pandas version: {pd.__version__}")
    # print(f"PyCaret version: {pycaret.__version__}")

    # print(pathlib.Path.cwd())
    final_model = load_model(MODEL_PATH)

    st.title("DPhi Tech - Machine Learning Bootcamp (Advanced Track)")
    st.header("Assignment #3 - Data Challenge #54")
    dphi_link = "[DPhi Tech](https://dphi.tech/practice/challenge/54)"
    st.markdown(dphi_link, unsafe_allow_html=True)
    st.subheader("Salil Athalye")
    link = "[GitHub](https://github.com/salilathalye/cwa-dphitech-challenge-54)"
    st.markdown(link, unsafe_allow_html=True)

    # TODO: Read from config/training_data_columns.json
    data_columns = [
        "Loan_ID",
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Loan_Amount_Term",
        "Credit_History",
        "Property_Area",
    ]

    st.sidebar.header("Loan Application Details")
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
    married = st.sidebar.selectbox("Married", ["No", "Yes"])
    dependents = st.sidebar.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.sidebar.selectbox("Education Level", ["Graduate", "Not Graduate"])
    self_employment = st.sidebar.selectbox("Self-employed", ["No", "Yes"])
    # Training data had missing values so pandas set dtype as float64, slightly squirrely!
    # TODO: Change to reflect a business language set of choices and flip to float64 for the model
    credit_history = st.sidebar.selectbox(
        "Credit History [1.0 - No Outstanding Debts]", ["1.0", "0.0"]
    )
    property_area = st.sidebar.selectbox(
        "Property Area", ["Rural", "Urban", "Semiurban"]
    )

    applicant_income = st.sidebar.number_input(
        "Applicant Annual Income $", 0, 100000, 5000
    )
    coapplicant_income = st.sidebar.number_input(
        "Co-applicant Annual Income $", 0, 100000, 1500
    )
    loan_amount = st.sidebar.number_input("Loan Amount $", 0, 1000, 125)
    # TODO: Check on PyCaret features, is it converting to dummies/indicator features?
    loan_amount_term = st.sidebar.selectbox(
        "Loan Term (Days)", ["12", "30", "60", "90", "180", "300", "360", "480"]
    )

    # In a Production system, the front-end would capture a unique loan ID.
    inputs = [
        "LP009999",
        gender,
        married,
        dependents,
        education,
        self_employment,
        applicant_income,
        coapplicant_income,
        loan_amount,
        loan_amount_term,
        credit_history,
        property_area,
    ]

    prediction_inputs_dict = dict(zip(data_columns, inputs))
    prediction_inputs_df = pd.DataFrame([prediction_inputs_dict])
    print(prediction_inputs_df.head())
    print(prediction_inputs_df.info())
    # TODO: Check that input schema complies with model schema
    st.header("Loan Application Details")
    st.subheader("Fill in your details, then click Submit")
    display_dataframe = prediction_inputs_df.T
    display_dataframe.columns = ["Your Response"]
    st.table(display_dataframe)
    prediction_label = 0
    prediction_message = "Rejected"
    prediction_score = 0.0
    # st.text(prediction_inputs)
    submit_button = st.button("Submit")
    if submit_button:
        st.text("Submitted")
        print(prediction_inputs_df)
        # TODO: Use threshold obtained from optimized_threshold_results.json
        prediction = predict_model(
            final_model, data=prediction_inputs_df, verbose=False
        )
        print(prediction)
        prediction_label = prediction["Label"].values
        prediction_message = "Approved" if prediction_label == 1 else "Rejected"
        prediction_score = prediction["Score"].values
        if prediction_label == 1:
            st.success(prediction_message)
        else:
            st.info(prediction_message)


if __name__ == "__main__":
    main()
