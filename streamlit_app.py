# Import python packages. 
import streamlit as st 
from snowflake.snowpark.functions import col 
import requests 
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:") 
st.write("Choose the fruits you want in your custom Smoothie!") 
name_on_order = st.text_input('Name on Smoothies:') 
st.write('The name on your Smoothies will be:', name_on_order) 
cnx = st.connection("snowflake") 
session = cnx.session() 
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'),col('SEARCH_ON') )

#st.dataframe(data=my_dataframe, use_container_width=True) 
#st.stop() 

pd_df=my_dataframe.to_pandas() 
#st.dataframe(pd_df) 
#st.stop()

# Call API using selected fruit

ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe, max_selections=5
)

if ingredients_List:
    ingredients_string = ''


    for fruit_chosen in ingredients_List:
        ingredients_string += fruit_chosen + ' '  

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The Search value for ', fruit_chosen, ' is ', search_on, '.')

        st.subheader(f"{fruit_chosen} Nutrition Information")

        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        

        sf_df=st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )
    


    my_insert_stmt = """
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES (?, ?)
    """

    st.write("Your order:", ingredients_string)


    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt, [ingredients_string, name_on_order]).collect()
        st.success(f'Your Smoothie is Ordered, {name_on_order}!', icon="✅")
        st.stop()

    
