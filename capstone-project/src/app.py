import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import process_dataframe_with_currency_conversion, remove_empty_entries

def create_dashboard(df):
    st.subheader("Interactive Dashboard")
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Get unique values for filtering
    age_ranges = pd.cut(df['Age'], bins=[0, 25, 35, 45, 55, 100], 
                       labels=['18-25', '26-35', '36-45', '46-55', '55+'])
    
    # Filter selectors
    selected_age = st.sidebar.multiselect(
        "Select Age Range",
        options=age_ranges.unique()
    )
    
    selected_education = st.sidebar.multiselect(
        "Select Education Level",
        options=df['Education_Level'].unique()
    )
    
    # Add loan purpose filter to sidebar
    selected_purpose = st.sidebar.multiselect(
        "Select Loan Purpose",
        options=df['Loan_Purpose'].unique()
    )
    
    # Apply filters
    mask = pd.Series(True, index=df.index)
    if selected_age:
        mask &= age_ranges.isin(selected_age)
    if selected_education:
        mask &= df['Education_Level'].isin(selected_education)
    if selected_purpose:
        mask &= df['Loan_Purpose'].isin(selected_purpose)
    
    filtered_df = df[mask]
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Loan Amount", f"${filtered_df['Loan_Amount'].mean():,.2f}")
    with col2:
        st.metric("Average Income", f"${filtered_df['Income'].mean():,.2f}")
    with col3:
        st.metric("Total Applications", len(filtered_df))
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Loan Amount by Education Level
        fig1 = px.box(filtered_df, x='Education_Level', y='Loan_Amount',
                     title='Loan Amount Distribution by Education Level')
        st.plotly_chart(fig1)
    
    with col2:
        # Average Income by Education Level
        avg_income = filtered_df.groupby('Education_Level')['Income'].mean().reset_index()
        fig2 = px.bar(avg_income, x='Education_Level', y='Income',
                      title='Average Income by Education Level')
        st.plotly_chart(fig2)

    # Risk Rating Analysis
    st.subheader("Risk Rating Analysis")
    col3, col4 = st.columns(2)
    
    with col3:
        # Risk Rating Distribution
        fig4 = px.histogram(filtered_df, x='Risk Rating', 
                          title='Risk Rating Distribution',
                          color='Education_Level')
        st.plotly_chart(fig4)
    
    with col4:
        # Average Loan Amount by Risk Rating
        risk_loan = filtered_df.groupby('Risk Rating')['Loan_Amount'].mean().reset_index()
        fig5 = px.bar(risk_loan, x='Risk Rating', y='Loan_Amount',
                      title='Average Loan Amount by Risk Rating')
        st.plotly_chart(fig5)

    # Risk Correlations
    st.subheader("Risk Rating Correlations")
    
    # Select numerical columns for correlation analysis
    numeric_cols = ['Age', 'Income', 'Credit_Score', 'Debt_to_Income_Ratio', 
                    'Loan_Amount', 'Risk Rating']
    correlation_df = filtered_df[numeric_cols]
    
    # Create correlation matrix
    correlation = correlation_df.corr()
    
    # Plot correlation heatmap
    fig6 = px.imshow(correlation,
                     labels=dict(color="Correlation"),
                     x=correlation.columns,
                     y=correlation.columns,
                     color_continuous_scale="RdBu",
                     aspect="auto",
                     title="Risk Factor Correlation Matrix")
    
    # Update layout for better readability
    fig6.update_traces(text=correlation.round(2), texttemplate="%{text}")
    st.plotly_chart(fig6)

    # Risk Rating Metrics
    st.subheader("Risk Metrics")
    risk_metrics_cols = st.columns(3)
    
    with risk_metrics_cols[0]:
        avg_risk = filtered_df['Risk Rating'].mean()
        st.metric("Average Risk Rating", f"{avg_risk:.2f}")
    
    with risk_metrics_cols[1]:
        high_risk = len(filtered_df[filtered_df['Risk Rating'] >= 7])
        st.metric("High Risk Applications", high_risk)
    
    with risk_metrics_cols[2]:
        low_risk = len(filtered_df[filtered_df['Risk Rating'] <= 3])
        st.metric("Low Risk Applications", low_risk)
    
    # Correlation heatmap
    numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns
    correlation = filtered_df[numeric_cols].corr()
    fig3 = px.imshow(correlation, title='Correlation Matrix')
    st.plotly_chart(fig3)

    # Add Loan Purpose Analysis section
    st.subheader("Loan Purpose Analysis")
    col5, col6 = st.columns(2)
    
    with col5:
        # Average loan amount by purpose
        purpose_loan = filtered_df.groupby('Loan_Purpose')['Loan_Amount'].mean().reset_index()
        fig7 = px.bar(purpose_loan, 
                      x='Loan_Purpose', 
                      y='Loan_Amount',
                      title='Average Loan Amount by Purpose')
        fig7.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig7)
    
    with col6:
        # Risk rating distribution by loan purpose
        fig8 = px.box(filtered_df, 
                      x='Loan_Purpose', 
                      y='Risk Rating',
                      title='Risk Rating Distribution by Loan Purpose')
        fig8.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig8)
    
    # Add purpose-specific metrics
    st.subheader("Loan Purpose Metrics")
    purpose_metrics = st.columns(3)
    
    with purpose_metrics[0]:
        most_common = filtered_df['Loan_Purpose'].mode()[0]
        st.metric("Most Common Purpose", most_common)
    
    with purpose_metrics[1]:
        highest_avg_loan = purpose_loan.loc[purpose_loan['Loan_Amount'].idxmax()]
        st.metric("Highest Avg Loan Purpose", highest_avg_loan['Loan_Purpose'])
    
    with purpose_metrics[2]:
        lowest_avg_loan = purpose_loan.loc[purpose_loan['Loan_Amount'].idxmin()]
        st.metric("Lowest Avg Loan Purpose", lowest_avg_loan['Loan_Purpose'])

def calculate_risk_rating(age, income, credit_score, dti_ratio, education_level, loan_purpose, loan_amount):
    """Calculate risk rating based on input parameters using both datasets for training"""
    # Load and combine training data from both files
    df1 = pd.read_excel("C:\Dev\Training\Week3_FinalExercise\group1\group1\input\Dataset1.xlsx")
    df2 = pd.read_excel("C:\Dev\Training\Week3_FinalExercise\group1\group1\input\Dataset2.xlsx")
    
    # Clean and process both datasets
    df1 = remove_empty_entries(df1)
    df2 = remove_empty_entries(df2)
    df1 = process_dataframe_with_currency_conversion(df1)
    df2 = process_dataframe_with_currency_conversion(df2)
    
    # Combine cleaned datasets
    training_data = pd.concat([df1, df2])
    
    # Calculate weights based on correlation with Risk Rating
    weights = {
        'Age': abs(training_data['Age'].corr(training_data['Risk Rating'])),
        'Income': abs(training_data['Income'].corr(training_data['Risk Rating'])),
        'Credit_Score': abs(training_data['Credit_Score'].corr(training_data['Risk Rating'])),
        'DTI': abs(training_data['Debt_to_Income_Ratio'].corr(training_data['Risk Rating'])),
        'Loan_Amount': abs(training_data['Loan_Amount'].corr(training_data['Risk Rating']))
    }
    
    # Calculate normalized scores
    age_score = (age - training_data['Age'].mean()) / training_data['Age'].std()
    income_score = (income - training_data['Income'].mean()) / training_data['Income'].std()
    credit_score = (credit_score - training_data['Credit_Score'].mean()) / training_data['Credit_Score'].std()
    dti_score = (dti_ratio - training_data['Debt_to_Income_Ratio'].mean()) / training_data['Debt_to_Income_Ratio'].std()
    loan_amount_score = (loan_amount - training_data['Loan_Amount'].mean()) / training_data['Loan_Amount'].std()
    
    # Calculate weighted risk score
    risk_score = (
        weights['Age'] * age_score +
        weights['Income'] * income_score +
        weights['Credit_Score'] * credit_score +
        weights['DTI'] * dti_score +
        weights['Loan_Amount'] * loan_amount_score
    )
    
    # Scale to 1-10 range
    min_risk = -3
    max_risk = 3
    scaled_risk = ((risk_score - min_risk) / (max_risk - min_risk)) * 9 + 1
    
    return min(max(round(scaled_risk, 1), 1), 10)

def risk_calculator_tab():
    st.subheader("Risk Rating Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        income = st.number_input("Annual Income ($)", min_value=0, max_value=1000000, value=50000)
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=700)
    
    with col2:
        dti_ratio = st.number_input("Debt to Income Ratio (%)", min_value=0.0, max_value=100.0, value=30.0)
        education_level = st.selectbox(
            "Education Level",
            options=['High School', 'Bachelor', 'Master', 'PhD']
        )
        loan_purpose = st.selectbox(
            "Loan Purpose",
            options=['Home', 'Education', 'Business', 'Car', 'Personal']
        )
    
    loan_amount = st.number_input("Loan Amount ($)", min_value=0, max_value=1000000, value=100000)
    
    if st.button("Calculate Risk Rating"):
        risk_rating = calculate_risk_rating(
            age, income, credit_score, dti_ratio, 
            education_level, loan_purpose, loan_amount
        )
        
        # Display result with color coding
        col1, col2, col3 = st.columns(3)
        with col2:
            color = "green" if risk_rating <= 3 else "orange" if risk_rating <= 7 else "red"
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <h2>Calculated Risk Rating</h2>
                    <h1 style='color: {color};'>{risk_rating}</h1>
                    <p>({risk_rating_description(risk_rating)})</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

def risk_rating_description(rating):
    if rating <= 3:
        return "Low Risk"
    elif rating <= 7:
        return "Medium Risk"
    else:
        return "High Risk"

def main():
    st.title("Loan Data Processor and Analytics Dashboard")
    st.write("Upload an Excel file to process and analyze loan data")

    # File uploader
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])

    if uploaded_file is not None:
        try:
            # Read and process the data
            df = pd.read_excel(uploaded_file)
            df = remove_empty_entries(df)
            processed_df = process_dataframe_with_currency_conversion(df)
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["Raw Data", "Dashboard", "Risk Calculator"])
            
            with tab1:
                st.subheader("Processed Data")
                st.dataframe(processed_df)
                
                # Download button
                csv = processed_df.to_csv(index=False)
                st.download_button(
                    label="Download processed data as CSV",
                    data=csv,
                    file_name="processed_data.csv",
                    mime="text/csv"
                )
            
            with tab2:
                create_dashboard(processed_df)
                
            with tab3:
                risk_calculator_tab()

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        # Show only risk calculator if no file is uploaded
        risk_calculator_tab()

if __name__ == "__main__":
    main()