import os
from sqlalchemy import VARCHAR
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from PIL import Image
import mysql.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["listingsdb"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

@st.experimental_memo(ttl=600)
def run_query(in_to):
    with conn.cursor() as cur:
        cur.execute(in_to)
        return cur._batch_insert()

# listing_data = ("assets/listings.xlsx")
# df = pd.read_excel(listing_data)

st.set_page_config(layout="wide")

"""CREATE TYPE input_data AS VARCHAR(20) ARRAY[100];"""
# --- SETTINGS ---
input_data = ('''INSERT INTO listings VALUES (
            :agents,
            :seller_name,
            :phone_number,
            :email_address,
            :contact_method,
            :property_address,
            :property_acreage,
            :sqft,
            :instructions,
            :total_rooms,
            :total_bathrooms,
            :list_price,
            :list_date,
            :soon_date,
            :active_date,
            :measured_date,
            :pre_inspection,
            :preinspection_date,
            :photography,
            :photo_date,
            :staged,
            :stage_date,
            :design,
            :style,
            :foundation,
            :finish,
            :roof,
            :roof_age,
            :roof_warranty,
            :foyer,
            :living_room,
            :dining_room,
            :kitchen_features,
            :kitchen_apps,
            :laundry,
            :half_bath,
            :master_bed,
            :bedroom_2,
            :bedroom_3,
            :bedroom_4,
            :bonus_room,
            :other_room1,
            :other_room2,
            :master_bathroom,
            :bathroom_2,
            :bathroom_3,
            :garage_carport,
            :heating,
            :cooling,
            :cooling_age,
            :water_heater,
            :water_heater_loc,
            :alarm,
            :alarm_leased,
            :attic,
            :property_type,
            :lot_description,
            :driveway_parking,
            :features,
            :water_sewer,
            :hoa,
            :sign,
            :lockbox,
            :pets,
            :gas_tank,
            :termite,
            :notes,
            :ext_photo), 
            {agents,
            seller_name,
            phone_number,
            email_address,
            con_method,
            property_address,
            property_acreage,
            property_sqft,
            show_instructions,
            tot_rooms,
            tot_baths,
            list_price,
            list_date,
            soon_date,
            active_date,
            measure_date,
            pre_inspect,
            pre_inspect_date,
            who_photo,
            photos_date,
            staged,
            staged_date,
            design,
            style,
            foundation,
            ext_finish,
            roof,
            roof_age,
            warranty,
            foyer,
            living_room,
            dining_room,
            kitchen_features,
            kitchen_appliances,
            laundry_room,
            half_bath,
            master_bedroom,
            bedroom_2,
            bedroom_3,
            bedroom_4,
            bonus_room,
            other_room_1,
            other_room_2,
            master_bathroom,
            bath_2,
            bath_3,
            garage_carport,
            heating,
            cooling,
            cooling_age,
            water_heater,
            water_heater_loc,
            alarm,
            alarm_leased,
            attic,
            property_type,
            lot_desc,
            drive_park,
            features,
            water,
            hoa,
            sign,
            lockbox,
            pets,
            gas_tank,
            termite,
            notes,
            uploaded_image}''')

seller_infos = ['Seller Name', 'Phone Number', 'Email Address', 'Preferred Contact Method']
property_infos = ["Property Address", "Property Acreage", "Home Square Footage", 
                "Showing Instructions", "# of Rooms (includes Bonus Room)", "# of Bathrooms"]
listing_infos = ['List Price', 'List Date', 'Coming Soon Date', 'Active Listing Date']
pro_services = ['When is a good date to get professionally measured?', 
                'Are the sellers ordering a pre-inspection on this house?', 
                'Pre-inspection Date',
                'Who is photographing this house?',
                'Photography Date',
                'Does this property need to be staged?',
                'Staging Date']

ext_features = ['Design','Style','Foundation','Exterior Finish','Roof',
                'Roof Age?','Roof Warranty?']

common_areas = ['Foyer','Living Room','Dining Room','Kitchen Features',
                'Kitchen Appliances','Laundry','Half Bath']

bedrooms = ['Master Bedroom','Bedroom #2','Bedroom #3','Bedroom #4',
                'Bonus Room','Other Room #1','Other Room #2']

bathrooms = ['Master Bathroom','Bathroom #2','Bathroom #3']

misc_features = ['Garage/Carport','Heating','Cooling','Age of the cooling system?',
                'Water Heater','What is the location of the water heater?',
                'Alarm System','Leased','Attic']
prop_features = ['Property Type','Lot Description','Driveway/Parking','Features','Water/Sewer','HOA?']
signs = ['Sign in the Yard?']
lockboxs = ['Lockbox on Door?']
pets = ['Pets on Site?']
gas_tanks = ['Gas Tank?']
termites = ['Termite Bond?']
notes = ['Notes']
agents = ["Lauren Rogers",
            "Charlene Bayne",
            "Gennifer Stancil", 
            "Darrell Erdman",
            "Nikki Painter", 
            "Jessica Tyler",
            "Brandi Stringfield",
            "Scott Daniels",
            "Tammy Register"]


image = Image.open('assets/hp-logo.png')
st.image(image)

# -- HIDE STREAMLIT STYLE ---
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Listing Info", "Coming Soon Listings"],
    icons=["pencil-fill", "bar-cart-fill"],
    orientation="horizontal",
)

# ---INPUT & SAVE LISTINGS ---
if selected == "Listing Info":
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            agents = st.selectbox("Select Agent:", options=agents, key="agents")
        
        with col2:
            uploaded_image = st.file_uploader("Upload exterior photo for records", type=['.png','jpeg','jpg','heic'], key="uploaded_image")

        "---"
        col1, col2 = st.columns(2)
        # --- SELLER INFO ----
        with col1:
            with st.expander("Seller Info:"):
                seller_name = st.text_input("Seller Name", key="seller_name")
                phone_number = st.number_input("Phone Number", min_value=0, format="%i", key="phone_number")
                email_address = st.text_input("Email Address", key="email_address")
                con_method = st.radio("Contact Method", ('Call', 'Text', 'Email'), key="contact_method")
                
        # --- PROPERTY INFO ---
        with col2:
            with st.expander("Property Info:"):
                property_address = st.text_input("Property Address", key="property_address")
                property_acreage = st.number_input("Property Acreage", min_value=0.0, value=0.5, step=.10, format="%f", key="property_acreage")
                property_sqft = st.number_input("Property Sqft.", format="%i", key="property_sqft")
                show_instructions = st.text_area("Showing Instructions", key="show_instructions")
                tot_rooms = st.number_input("Total # of Rooms", min_value=0, format="%i", key="tot_rooms")
                tot_baths = st.number_input("Total # of Bathrooms", min_value=0, format="%i", key="tot_baths")
        
        # --- LISTING INFO ---
        with col1:
            with st.expander("Listing Specs:"):
                list_price = st.number_input("Listing Price", min_value=100000, step=100000, format="%i", key="list_price")
                list_date = st.date_input("Listing Date", key="list_date")
                soon_date = st.date_input("Coming Soon Date", key="soon_date")
                active_date = st.date_input("Active Listing Date", key="active_date")

        # --- PRO SERVICES ---
        with col2:
            with st.expander("Professional Services:"):
                measure_date = st.date_input("Date to do Measurements", key="measure_date")
                pre_inspect = st.radio("Pre-Inspection?", ('Yes', 'No'), key="pre_inspect")
                pre_inspect_date = st.date_input("Pre-Inspection Date", key="pre_inspect_date")
                who_photo = st.text_input("Who is taking the photographys?", key="who_photo")
                photos_date = st.date_input("Photography Date", key="photos_date")
                staged = st.radio("Need to be staged", ('Yes', 'No'), key="staged")
                staged_date = st.date_input("Staging Date", key="staged_date")
                
        # ---EXTERIOR FEATURES AND DESIGN ---
        with col1:
            with st.expander('Exterior Features & Design:'):
                design = st.multiselect("Home Design", options=['1 Story', '1.5 Story', 
                                '2 Story', '2.5 Story', 'Split Level', 'Expandable Ranch'], key="design")
                style = st.multiselect("Home Style", options=['Ranch','Bungalow','Craftsman',
                                'Farm House','Log Home','Traditional','Victorian',
                                'Cottage','Other'], key="style")
                foundation = st.multiselect("Foundation Type", options=['Basement',
                                'Block','Brick Foundation','Crawl Space','Slab',
                                'Stem Walls','Walk-In Crawl','Vapor Barrier','Other'], key="foundation")
                ext_finish = st.multiselect("Exterior Finish", options=['Vinyl Siding',
                                'Brick Veneer','Fiber Cement','Masonite','Other'], key="ext_finish")
                roof = st.multiselect("Roof type", options=['Shingle',
                                'Metal/Tin','Tile','Slate','Other'], key="roof")
                roof_age = st.number_input("Roof Age", min_value=0, format="%i", step=10, key="roof_age")
                warranty = st.radio("Is the roof warranted?", ('Yes', 'No'), key="warranty")

        with col2:
            with st.expander("Common Areas:"):
                foyer = st.multiselect("Foyer", options=['Gallery',
                                'Vaulted','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="foyer")
                living_room = st.multiselect("Living Room", options=["8' Ceilings","9' Ceilings",
                                'Vaulted','Trey','Coffered','Ceiling Fan','Carpet','Wood','Vinyl',
                                'Laminate','Eng. Hardwood'], key="living_room")
                dining_room = st.multiselect("Dining Room", options=['Separate/Formal',
                                'Breakfast Room','Eat-In Kitchen',
                                'Trey','Coffered','Carpet','Wood',
                                'Vinyl','Laminate','Eng. Hardwood'], key="dining_room")
                kitchen_features = st.multiselect("Kitchen Features", options=['Island','Pantry',
                                'Walk-In Pantry','Granite','Formica','Tile','Carpet',
                                'Wood','Vinyl','Laminte','Eng. Hardwood'], key="kitchen_features")
                kitchen_appliances = st.multiselect("Kitchen Appliances", options=['Refrigerator',
                                'Electric Range','Gas Range','Electric Cooktop','Microwave','Dishwasher',
                                'Other'], key="kitchen_appliances")
                laundry_room = st.multiselect("Laundry Room", options=['Laundry Room',
                                'Closet','Washer Conveys','Dryer Conveys','Tile','Carpet',
                                'Wood','Vinyl','Laminate','Eng. Hardwood'], key="laundry")
                half_bath = st.multiselect("Half Bath", options=['1st Floor','2nd Floor','Tile',
                                'Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="half_bath")

        with col1:
            with st.expander('Bedrooms:'):
                    master_bedroom = st.multiselect("Master Bedroom", options=["8' Ceilings","9' Ceilings",'Vaulted','Trey','Coffered','Ceiling Fan','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="master_bedroom")
                    bedroom_2 = st.multiselect("Bedroom #2", options=["8' Ceilings","9' Ceilings",'Vaulted','Trey','Coffered','Ceiling Fan','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="bedroom_2")
                    bedroom_3 = st.multiselect("Bedroom #3", options=["8' Ceilings","9' Ceilings",'Vaulted','Trey','Coffered','Ceiling Fan','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="bedroom_3")
                    bedroom_4 = st.multiselect("Bedroom #4", options=["8' Ceilings","9' Ceilings",'Vaulted','Trey','Coffered','Ceiling Fan','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="bedroom_4")
                    bonus_room = st.multiselect("Bonus Room", options=["Finished","Unfinished",'Ceiling Fan','HVAC','Mini Split','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="bonus_room")
                    other_room_1 = st.multiselect("Other Room #1", options=["8' Ceilings","9' Ceilings",'Vaulted','Trey','Coffered','Ceiling Fan','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="other_room_1")
                    other_room_2 = st.multiselect("Other Room #2", options=["8' Ceilings","9' Ceilings",'Vaulted','Trey','Coffered','Ceiling Fan','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="other_room_2")
                
        with col2:
            with st.expander('Bathooms:'):
                    master_bathroom = st.multiselect("Master Bathroom", options=['Ensuite','Hall','Garden Tub','Combo','Tub/Sep. Shower','Tile','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="master_bathroom")
                    bath_2 = st.multiselect("Bathroom #2", options=['Hall','Jack & Jill','Combo','Tub/Sep. Shower','Tile','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="bath_2")
                    bath_3 = st.multiselect("Bathroom #3", options=['Hall','Jack & Jill','Combo','Tub/Sep. Shower','Tile','Carpet','Wood','Vinyl','Laminate','Eng. Hardwood'], key="bath_3")

        with col1:
            with st.expander('Misc Features:'):
                    garage_carport = st.multiselect("Garage/Carport", options=['1-Car','2-Car','3-Car','Attached','Detached','Garage','Carport','Side Entry','TouchPad Entry','Workshop'], key="garage_carport")
                    heating = st.multiselect("Heating", options=['Heat Pump','Gas Pack','Single-Zone','Dual-Zone','Electric','Propane','Natural Gas'], key="heating")
                    cooling = st.multiselect("Cooling", options=['Central Air','Heat Pump','Window Unit','Single-Zone','Dual-Zone'], key="cooling")
                    cooling_age = st.radio("Cooling Age", ('Yes', 'No'), key="cooling_age")
                    water_heater = st.multiselect("Water Heater Type", options=['Electric','Gas','Tankless','Other'], key="water_heater")
                    water_heater_loc = st.text_input("Water Heater Location", key="water_heater_loc")
                    alarm = st.multiselect("Alarm System", options=['None', 'Monitored','Unmonitored','Leased'], key="alarm")
                    alarm_leased = st.text_input("Alarm System Leased?", key="leased")
                    attic = st.multiselect("Attic", options=['Skuttle','Pull Down','Permanent Stairs','Finished','Unfinished','Walk-In','Exhaust Fan','No Attic','Other'], key="attic")

        with col2:
            with st.expander('Property Type:'):
                    property_type = st.multiselect("Property Type", options=['Detached','Attached','Single-MFG','Double-MFG','Triple-MFG','Modular'], key="property_type")
                    lot_desc = st.multiselect("Lot Description", options=['Cul-De-Sac','Landscaped','Wooded','Fenced','Corner','Other'], key="lot_desc")
                    drive_park = st.multiselect("Driveway and Parking", options=['Concrete','Asphalt','Gravel','Earth','Brick','None','Other'], key="drive_park")
                    features = st.multiselect("Property Features", options=['Deck (Open)','Screened Porch','Covered Deck','Patio','Workshop/Barn','Gutters','Fenced Yard','Irrigation','Pool (Above','Pool (In-Ground)','Other'], key="features")
                    water = st.multiselect("Water", options=['County Water','City Water','Well','Tap Paid','County Sewer','On-Site Septic','Off-Site Septic','Other'], key="water")
                    hoa = st.radio("Is there a HOA?", ('Yes', 'No', 'Other'), key="hoa")

        with st.expander('Listing Extras:'):
                for sign in signs:
                    st.radio("Sign in the yard?", ('Yes', 'No'), key="sign")
                for lockbox in lockboxs:
                    st.radio("Is there a lockbox on the door?", ('Yes', 'No'), key="lockbox")
                for pet in pets:
                    st.radio("Are there pets on the proptery?", ('Yes', 'No'), key="pet")
                for gas_tank in gas_tanks:
                    st.radio("Is there a gas tank on the property?", ('Yes', 'No'), key="gas_tank")
                for termite in termites:
                    st.radio("Is there a termite bond?", ('Yes', 'No'), key="termite")

        for note in notes:
            notes = st.text_area('Notes', placeholder="Enter any additional notes here ...", key="notes")
    
        submitted = st.form_submit_button("Save Info")
        
        # $columns = implode(", ",array_keys($insData));
        # $escaped_values = array_map('mysql_real_escape_string', array_values($insData));
        # $values  = implode("', '", $escaped_values);
        # $sql = ("INSERT INTO `fbdata`($columns) VALUES ('$values')")

        if submitted:
            run_query(in_to)
        conn.commit()

        conn.close()
            
#             # df = df.append(submitted, ignore_index=True)
#             # df.to_excel(listing_data, index=False)
            
#             st.success("Data saved!")


# if selected == "Coming Soon Listings":
#     st.header("Coming Soon Listings")

#     for row in rows:
#         st.write(f"{seller_name}")

#     # selection = df[['Agents', 'Property Address', 'Listing Date', 'Coming Soon Date', 'Active Listing Date', 'Property Acreage', 'Property Sqft', 'Showing Instructions', 
#     #                 'Total # of Rooms', 'Total # of Baths', 'Listing Price', 'Notes']]

#     # today = datetime.today()
#     # selection[df['Listing Date'] > today]
