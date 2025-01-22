# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

import streamlit as st

# Test if 'Snowflake' key exists in the secrets
if "Snowflake" in st.secrets:
    st.write("Snowflake secrets are configured correctly!")
    # Optionally, print out a part of the Snowflake secrets to debug (e.g., user name)
    st.write(f"User: {st.secrets['Snowflake']['user']}")
else:
    st.write("No Snowflake secrets found. Please check your Streamlit secrets.")


# Write directly to the app
st.title("Customize your own smoothie :cup_with_straw:")
st.write("""Choose the fruits you want for your custom smoothie.""")

# Get the name on the smoothie
name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your Smoothie will be', name_on_order)

# Connect to Snowflake
cnx = st.connection("Snowflake")  # Ensure Snowflake connection is defined in your Streamlit secrets
session = cnx.session()

# Fetch available fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Display fruit options in a multiselect
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe['FRUIT_NAME'].tolist())

# Handling the selected ingredients
if ingredients_list:
    # Concatenate selected ingredients into a string
    ingredients_string = ', '.join(ingredients_list)
    
    # Insert SQL statement
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES (%s, %s)
    """
    
    # Create a button to submit the order
    time_to_insert = st.button('Submit order')
    
    if time_to_insert:
        # Using parameterized queries to avoid SQL injection
        session.sql(my_insert_stmt, (ingredients_string, name_on_order)).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


