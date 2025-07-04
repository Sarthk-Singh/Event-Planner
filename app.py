import streamlit as st
import pandas as pd
import os
import qrcode
from PIL import Image
from io import BytesIO

# Define the directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
QR_FOLDER = os.path.join(BASE_DIR, "qrcodes")

ATTENDEES_PATH = os.path.join(DATA_DIR, "attendees.csv")
MENU_PATH = os.path.join(DATA_DIR, "menu.csv")
ORDERS_PATH = os.path.join(DATA_DIR, "orders.csv")

os.makedirs(QR_FOLDER, exist_ok=True)

# Load CSVs
def load_data():
    attendees = pd.read_csv(ATTENDEES_PATH)
    menu = pd.read_csv(MENU_PATH)
    orders = pd.read_csv(ORDERS_PATH)
    return attendees, menu, orders

def save_data(attendees, menu, orders):
    attendees.to_csv(ATTENDEES_PATH, index=False)
    menu.to_csv(MENU_PATH, index=False)
    orders.to_csv(ORDERS_PATH, index=False)

def generate_qr(attendee_id, name, paid, checked_in):
    base_url = "https://Sarthk-Singh.github.io/Event-Planner/checkin.html"
    url_data = f"{base_url}?id={attendee_id}&name={name}&paid={paid}&checked_in={checked_in}"
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")  # Convert to PIL.Image.Image
    img_path = os.path.join("qrcodes", f"{attendee_id}_{name}.png")
    img.save(img_path)
    return img_path, img

st.set_page_config(page_title="Event Manager", layout="wide")
st.markdown(
    """
    <h1 style='text-align: center; font-size: 3.5em; color: ##FFFFFF; 
               text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3); 
               font-family: "Segoe UI", sans-serif;'>
        🎉 Event Manager Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

attendees, menu, orders = load_data()

# Sidebar navigation
page = st.sidebar.radio("📂 Pages", ["Manage Attendees", "Menu Upload", "Orders", "Check-In", "Summary"])

# Page: Manage Attendees
if page == "Manage Attendees":
    st.header("🧑‍🤝‍🧑 Attendee Management")

    qr_display = st.empty()
    qr_download = st.empty()

    with st.form("add_attendee"):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_id = st.text_input("ID")
            name = st.text_input("Name")
        with col2:
            age = st.selectbox("Age Bracket", ["25-30", "31-35", "36-40"])
            location = st.text_input("Location")
        with col3:
            paid = st.selectbox("Paid", ["Yes", "No"])

        submitted = st.form_submit_button("Add Attendee")

    if submitted:
        if new_id and name:
            # Add attendee to DataFrame
            attendees.loc[len(attendees)] = [new_id, name, age, location, paid, "No"]

            # Generate QR with all required info
            img_path, img = generate_qr(new_id, name, paid, "No")

            # Save updated data
            save_data(attendees, menu, orders)

            # Display QR image + download button
            st.success("✅ Attendee added and QR generated!")
            st.image(img, caption=f"QR for {name}", use_container_width=False)
            with open(img_path, "rb") as f:
                st.download_button(label="📥 Download QR", data=f, file_name=f"{name}_qr.png", mime="image/png")
        else:
            st.error("❌ ID and Name required")

    st.subheader("🗑️ Remove Attendee")
    attendee_to_remove = st.selectbox("Select Attendee to Remove", attendees['name'])
    if st.button("Remove Attendee"):
        attendees = attendees[attendees['name'] != attendee_to_remove]
        orders = orders[orders['name'] != attendee_to_remove]
        save_data(attendees, menu, orders)
        st.success(f"❌ Removed {attendee_to_remove} from attendees and orders")

    st.dataframe(attendees)

# Page: Menu Upload
elif page == "Menu Upload":
    st.header("📋 Upload or View Menu")
    uploaded_file = st.file_uploader("Upload menu CSV (columns: item, price)", type=["csv"])

    if uploaded_file:
        try:
            new_menu = pd.read_csv(uploaded_file)
            if "item" in new_menu.columns and "price" in new_menu.columns:
                menu = new_menu
                save_data(attendees, menu, orders)
                st.success("✅ Menu uploaded and saved!")
            else:
                st.error("❌ CSV must contain 'item' and 'price' columns")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

    st.subheader("📜 Current Menu")
    st.dataframe(menu)

# Page: Orders
elif page == "Orders":
    st.header("🛒 Manage Orders")
    selected_attendee = st.selectbox("Select Attendee", attendees["name"])
    attendee_row = attendees[attendees["name"] == selected_attendee].iloc[0]
    attendee_id = attendee_row["id"]

    attendee_orders = orders[orders["id"] == attendee_id]
    used_credit = attendee_orders["total"].sum()
    remaining_credit = 1000 - used_credit

    st.write(f"💰 Used: ₹{used_credit} / ₹1000 | Remaining: ₹{remaining_credit}")

    with st.form("add_order"):
        item = st.selectbox("Item", menu["item"])
        quantity = st.number_input("Quantity", min_value=1, value=1)

        if st.form_submit_button("Add Order"):
            price = int(menu[menu["item"] == item]["price"].values[0])
            total = price * quantity
            if remaining_credit - total >= 0:
                orders.loc[len(orders)] = [attendee_id, selected_attendee, item, quantity, price, total]
                save_data(attendees, menu, orders)
                st.success("✅ Order added!")
            else:
                st.warning("⚠️ Order exceeds ₹1000 limit")

    st.subheader("🧾 Order History")
    st.dataframe(attendee_orders)
    st.subheader("🗑️ Remove Order Item")

    # Re-index to get clean row numbers for dropdown
    attendee_orders_reset = attendee_orders.reset_index(drop=False)

    if not attendee_orders_reset.empty:
        # Let user select an order to remove
        selected_row_index = st.selectbox(
            "Select an order to remove:",
            attendee_orders_reset.index,
            format_func=lambda i: f"{attendee_orders_reset.loc[i, 'item']} x{attendee_orders_reset.loc[i, 'quantity']} = ₹{attendee_orders_reset.loc[i, 'total']}"
        )

        if st.button("❌ Remove Selected Order"):
            # Get the actual index in the original orders dataframe
            original_index = attendee_orders_reset.loc[selected_row_index, 'index']
            orders.drop(index=original_index, inplace=True)
            save_data(attendees, menu, orders)
            st.success("🗑️ Order removed!")
            st.rerun()

    else:
        st.info("No orders to remove.")

# Page: Check-In
elif page == "Check-In":
    st.header("🎟️ Check-In Attendees")

    input_id = st.text_input("Scan or Enter Attendee ID")
    if input_id:
        try:
            input_id_int = int(input_id.strip())
            match = attendees[attendees["id"] == input_id_int]
            if match.empty:
                st.error("❌ ID not found")
            else:
                row = match.iloc[0]
                st.success(f"✅ Found: {row['name']} from {row['location']}")
                st.write(f"Paid: {row['paid']} | Checked In: {row['checked_in']}")

                if row['checked_in'] == "No":
                    if st.button("Mark as Checked In"):
                        attendees.loc[attendees['id'] == input_id_int, 'checked_in'] = "Yes"
                        save_data(attendees, menu, orders)
                        st.success("🎉 Checked in!")
                else:
                    st.info("Already checked in")
        except ValueError:
            st.warning("⚠️ Please enter a valid numeric ID.")

    st.subheader("📋 All Attendees Overview")
    st.dataframe(attendees[['id','name', 'paid', 'checked_in']])

    st.subheader("💸 Update Payment Status")
    selected_payment_update = st.selectbox("Select Attendee", attendees['name'], key="payment_status")
    new_status = st.selectbox("New Payment Status", ["Yes", "No"], key="new_status")
    
    if st.button("Update Payment Status"):
        attendees.loc[attendees['name'] == selected_payment_update, 'paid'] = new_status
        save_data(attendees, menu, orders)
        st.success(f"✅ Payment status for {selected_payment_update} updated to {new_status}")

# Page: Summary
elif page == "Summary":
    st.header("📊 Per-Person Order Summary")

    show_only_checked_in = st.checkbox("Show only checked-in attendees")

    filtered_attendees = attendees
    if show_only_checked_in:
        filtered_attendees = attendees[attendees['checked_in'] == 'Yes']

    total_headcount = len(attendees)
    total_checked_in = len(attendees[attendees['checked_in'] == 'Yes'])
    total_money_from_checked_in = total_checked_in * 1500
    total_money_raised = total_headcount * 1500
    total_order_budget = total_checked_in * 1000
    
    checked_in_ids = attendees[attendees['checked_in'] == 'Yes']['id']
    checked_in_orders = orders[orders['id'].isin(checked_in_ids)]
    money_spent = checked_in_orders['total'].sum()
    remaining_order_money=total_order_budget-money_spent

    st.markdown(f"**👥 Total Headcount:** {total_headcount}")
    st.markdown(f"**✅ Checked-In Count:** {total_checked_in}")
    st.markdown(f"**💵 Total from Checked-Ins:** ₹{total_money_from_checked_in}")
    st.markdown(f"**🏦 Total Money Raised:** ₹{total_money_raised}")
    st.markdown(f"**🥂 Total Budget For Orders:** ₹{total_order_budget}")
    st.markdown(f"**🍽️ Total Money Spent by Checked-In Attendees:** ₹{money_spent}")
    st.markdown(f"**🍽️ Money Remaining from Order Money:** ₹{remaining_order_money}")

    summary_data = []
    for _, row in filtered_attendees.iterrows():
        attendee_id = row['id']
        name = row['name']
        person_orders = orders[orders['id'] == attendee_id]
        items = ', '.join(person_orders['item'].tolist()) or "None"
        total = person_orders['total'].sum()
        remaining = 1000 - total
        summary_data.append({"Name": name, "Items Ordered": items, "Total Spent": total, "Remaining Credit": remaining})

    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df)
