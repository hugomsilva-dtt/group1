import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from utils.helpers import process_dataframe_with_currency_conversion, remove_empty_entries

# Update the custom color scheme
COLOR_PALETTE = {
    'primary': '#FF6B00',    # Orange
    'secondary': '#FFB800',  # Yellow
    'background': '#1A1A1A', # Dark background
    'surface': '#2D2D2D',    # Darker surface
    'text': '#FFFFFF'        # White text
}

# Update the custom CSS
st.markdown(
    """
    <style>
    /* Main app background and text */
    .stApp {
        background-color: #1A1A1A;
        color: white;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2D2D2D;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #2D2D2D !important;
        color: white !important;
        border: 1px solid #FF6B00 !important;
        border-radius: 4px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #FF6B00, #FFB800);
        color: white;
        border: none;
        font-weight: bold;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #2D2D2D;
        color: white;
        border: 1px solid #FF6B00;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2D2D2D;
        border-radius: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        color: white;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #FF6B00;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #FF6B00;
        font-weight: bold;
    }

    /* DataFrame */
    .dataframe {
        background-color: #2D2D2D !important;
        color: white !important;
    }

    /* Charts background */
    .js-plotly-plot {
        background-color: #2D2D2D !important;
    }

    /* Logo container */
    .logo-container {
        background: linear-gradient(135deg, #FF6B00, #FFB800);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: #2D2D2D;
    }

    ::-webkit-scrollbar-thumb {
        background: #FF6B00;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Update the logo generation
def generate_logo():
    logo = """
    <div class="logo-container">
        <h1 style="color: white; font-size: 3rem; margin: 0;">🏦 LoanWise</h1>
        <p style="color: white; font-size: 1.2rem; margin-top: 0.5rem;">Smart Loan Risk Analysis</p>
    </div>
    """
    return st.markdown(logo, unsafe_allow_html=True)

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
    fig6 = px.imshow(
        correlation,
        labels=dict(color="Correlation"),
        x=correlation.columns,
        y=correlation.columns,
        color_continuous_scale=[
            [0, '#FF6B00'],
            [0.5, '#FFB800'],
            [1, '#4CAF50']
        ],
        aspect="auto",
        title="Risk Factor Correlation Matrix"
    )

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

    # Update plot color schemes
    fig1.update_traces(marker_color='#FF6B00')
    fig2.update_traces(marker_color='#FFB800')
    fig4.update_layout(
        plot_bgcolor='#FFF9F2',
        paper_bgcolor='#FFF9F2'
    )
    fig5.update_traces(marker_color='#4CAF50')
    
    # Update plot themes
    plot_template = {
        'layout': {
            'plot_bgcolor': '#2D2D2D',
            'paper_bgcolor': '#2D2D2D',
            'font': {'color': 'white'},
            'title': {'font': {'color': 'white'}},
            'xaxis': {'gridcolor': '#444444', 'color': 'white'},
            'yaxis': {'gridcolor': '#444444', 'color': 'white'}
        }
    }

    # Apply dark theme to all plots
    for fig in [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8]:
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='#2D2D2D',
            paper_bgcolor='#2D2D2D',
            font_color='white'
        )

def create_risk_heatmap(data):
    """Create risk analysis heatmap with proper colorscale"""
    
    # Define proper colorscale format
    colorscale = [
        [0.0, '#FF6B00'],  # Orange for low risk
        [0.5, '#FFB800'],  # Yellow for medium risk  
        [1.0, '#4CAF50']   # Green for high risk
    ]

    # Create heatmap figure
    fig = px.imshow(
        data,
        title='Risk Analysis Heatmap',
        color_continuous_scale=colorscale,  # Use proper colorscale property
        aspect='auto'
    )

    # Update layout
    fig.update_layout(
        paper_bgcolor='#2D2D2D',
        plot_bgcolor='#2D2D2D',
        font_color='#FFFFFF'
    )

    # Update colorbar
    fig.update_traces(
        showscale=True,
        colorbar=dict(
            title='Risk Level',
            titleside='right',
            ticktext=['Low', 'Medium', 'High'],
            tickvals=[0, 0.5, 1],
            tickmode='array',
            tickfont=dict(color='#FFFFFF'),
            titlefont=dict(color='#FFFFFF')
        )
    )

    return fig

def calculate_risk_rating(age, income, credit_score, dti_ratio, education_level, loan_purpose, loan_amount):
    """Calculate risk rating based on input parameters using both datasets for training"""
    try:
        # Load and process training data
        df1 = pd.read_excel("C:\Dev\Training\Week3_FinalExercise\group1\group1\input\Dataset1.xlsx")
        df2 = pd.read_excel("C:\Dev\Training\Week3_FinalExercise\group1\group1\input\Dataset1.xlsx")
        
        # Validate DTI ratio is between 0 and 1
        if not (0 <= dti_ratio <= 1):
            raise ValueError("Debt to Income ratio must be between 0 and 1")

        # Calculate risk weights based on correlation analysis
        weights = {
            'Credit_Score': 0.3,    # Higher credit score = lower risk
            'DTI': 0.25,           # Higher DTI = higher risk
            'Income': 0.2,         # Higher income = lower risk
            'Loan_Amount': 0.15,   # Higher loan amount = higher risk
            'Age': 0.1             # Age has less impact
        }
        
        # Normalize and score each factor
        credit_score_norm = (credit_score - 300) / (850 - 300)  # Credit score range: 300-850
        dti_score = dti_ratio                                    # DTI already in 0-1 range
        income_norm = min(income / 200000, 1)                   # Cap income at 200k
        loan_amount_norm = min(loan_amount / 150000, 1)         # Cap loan at 150k
        age_norm = min(age / 100, 1)                           # Cap age at 100
        
        # Calculate risk score (0 = lowest risk, 1 = highest risk)
        risk_score = (
            weights['Credit_Score'] * (1 - credit_score_norm) +  # Invert credit score
            weights['DTI'] * dti_score +
            weights['Income'] * (1 - income_norm) +              # Invert income
            weights['Loan_Amount'] * loan_amount_norm +
            weights['Age'] * (1 - age_norm)                      # Invert age
        )
        
        # Convert to 0-2 scale matching the training data
        final_risk_rating = round(risk_score * 2)
        
        return min(max(final_risk_rating, 0), 2)  # Ensure output is 0, 1, or 2
        
    except Exception as e:
        st.error(f"Error calculating risk rating: {str(e)}")
        return None

def risk_calculator_tab():
    """Risk calculator interface"""
    st.subheader("Risk Rating Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        income = st.number_input("Annual Income ($)", min_value=0, max_value=1000000, value=50000)
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=700)
    
    with col2:
        dti_ratio = st.number_input(
            "Debt to Income Ratio (0-1)", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.3,
            step=0.01,
            help="Enter a value between 0 and 1, e.g., 0.3 equals 30%"
        )
        education_level = st.selectbox(
            "Education Level",
            options=['High School', 'Bachelor', 'Master', 'PhD']
        )
        loan_purpose = st.selectbox(
            "Loan Purpose",
            options=[
                'Home',
                'Education',
                'Business',
                'Car',
                'Personal',
                'Medical',
                'Debt Consolidation'
            ]
        )
    
    loan_amount = st.number_input("Loan Amount ($)", min_value=0, max_value=1000000, value=100000)
    
    if st.button("Calculate Risk Rating"):
        risk_rating = calculate_risk_rating(
            age, income, credit_score, dti_ratio, 
            education_level, loan_purpose, loan_amount
        )
        
        # Display result with corrected scale
        col1, col2, col3 = st.columns(3)
        with col2:
            # Adjust color scale for 0-2 range
            color = "#4CAF50" if risk_rating == 0 else "#FFB800" if risk_rating == 1 else "#FF6B00"
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
    """Return description based on 0-2 scale"""
    if rating == 0:
        return "Low Risk"
    elif rating == 1:
        return "Medium Risk"
    else:
        return "High Risk"

def main():
    # Display logo
    generate_logo()
    
    st.title("Loan Risk Analysis Dashboard")
    st.write("Upload your loan data for comprehensive analysis")

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