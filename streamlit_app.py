# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
import requests 

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# User input
name_on_order = st.text_input('Name on Smoothies:')
st.write('The name on your Smoothies will be:', name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit list
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe, max_selections=5
)

# If user selects ingredients
if ingredients_List:
    ingredients_string = ''

    # 🔁 Loop ONLY for displaying nutrition info
    for fruit_chosen in ingredients_List:
        ingredients_string += fruit_chosen + ' '   # space added

        st.subheader(f"{fruit_chosen} Nutrition Information")

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + fruit_chosen
        )

        st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    # ✅ SQL query OUTSIDE loop
    my_insert_stmt = """
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES (?, ?)
    """

    st.write("Your order:", ingredients_string)

    # ✅ Single button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt, [ingredients_string, name_on_order]).collect()
        st.success(f'Your Smoothie is Ordered, {name_on_order}!', icon="✅")
        st.stop()

    
