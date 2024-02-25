import streamlit as st
import pandas as pd
import openai
import json


# Read API key from a file
with open('API_KEY.txt', 'r') as file:
    api_key = file.read().strip()
    
    
# Set your OpenAI API key
openai.api_key = api_key



def extract_financial_data(text):
    prompt = get_prompt_financial() + text
    response = openai.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages =[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content
    

    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])

    except (json.JSONDecodeError, IndexError):
        pass

    return pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })


def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following new article. If you can't find the information from this article then return "". 
    Do not make things up. Then retrieve a stock symbol corresponding to that company. 
    For this you can use your general knowledge (it doesn't have to be from this article).
    Always return your response as a valid JSON string. The format of that string should be this,
    {
        "Company Name" : "Walmart",
        "Stock Symbol" : "WMT",
        "Revenue" : "12.34 million",
        "EPS" : "$ 2.5
    }
    News Article:
    ===============

    '''


def main():
    
    st.title("Finance Data Extraction Tool")

    col1, col2 = st.columns([3,2])

    financial_data_df = pd.DataFrame({
            "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
            "Value": ["", "", "", "", ""]
        })

    with col1:
        news_article = st.text_area("Paste your financial news article here", height=300)
        if st.button("Extract"):
            financial_data_df = extract_financial_data(news_article)

    with col2:
        st.markdown("<br/>" * 5, unsafe_allow_html=True)  # Creates 5 lines of vertical space
        st.dataframe(
            financial_data_df,
            column_config={
                "Measure": st.column_config.Column(width=150),
                "Value": st.column_config.Column(width=150)
            },
            hide_index=True
        )


if __name__ == "__main__":
    main()
