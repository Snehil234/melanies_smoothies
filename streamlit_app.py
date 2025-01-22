# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests




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
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ' '
    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen + ' '
        smoothiefroot_response = requests.get(" https://www.fruityvice.com/api/fruit/watermelon")
        #st.text(smoothiefroot_response)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

    #st.write(ingredients_string) 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")




