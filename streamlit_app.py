# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app.
st.title("My Parents New Healthy Diner")
st.write("Choose the fruits you want in your custom Smoothie!")


name_on_order=st.text_input('Name on Smoothies:')
st.write('The name on your Smoothies will be:',name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe , max_selections=5
)

#st.write(ingredients_List)
#st.text(ingredients_List)



if ingredients_List:
    ingredients_string=''

    for fruit_chosen in ingredients_List:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

  
    my_insert_stmt = """ INSERT INTO smoothies.public.orders (ingredients,name_on_order) VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)


    #st.write(my_insert_stmt)

    #if ingredients_string:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")

    time_to_insert =st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt, [ingredients_string, name_on_order]).collect()
        st.success(f'Your Smoothie is Ordered!,{name_on_order}! ',icon="✅")
        st.stop()
    
