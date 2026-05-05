import streamlit as st
import pandas as pd
from database import init_db, add_item, get_items, update_item, delete_item

# Initialize database
init_db()

st.set_page_config(page_title="Inventory System", layout="wide")

st.title("📦 Inventory Management System")

# Sidebar for navigation
menu = ["Dashboard", "Add Item", "Manage Inventory"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Dashboard":
    st.subheader("📊 Dashboard")
    df = get_items()
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Items", len(df))
        col2.metric("Total Stock", df['quantity'].sum())
        col3.metric("Total Value", f"${(df['quantity'] * df['price']).sum():.2f}")
        
        st.write("### Low Stock Alerts")
        low_stock = df[df['quantity'] < 5]
        if not low_stock.empty:
            st.warning(f"Found {len(low_stock)} items with low stock!")
            st.dataframe(low_stock, use_container_width=True)
        else:
            st.success("All items are well stocked.")
    else:
        st.info("Inventory is empty. Add items to see statistics.")

elif choice == "Add Item":
    st.subheader("➕ Add New Item")
    with st.form("add_form"):
        name = st.text_input("Item Name")
        category = st.selectbox("Category", ["Electronics", "Furniture", "Groceries", "Clothing", "Other"])
        quantity = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price ($)", min_value=0.0, step=0.01)
        
        submitted = st.form_submit_button("Add Item")
        if submitted:
            if name:
                add_item(name, category, quantity, price)
                st.success(f"Added {name} to inventory!")
            else:
                st.error("Please provide an item name.")

elif choice == "Manage Inventory":
    st.subheader("🛠️ Manage Inventory")
    df = get_items()
    
    if not df.empty:
        # Search and filter
        search = st.text_input("Search by Name", "")
        if search:
            df = df[df['name'].str.contains(search, case=False)]
            
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        st.write("### Edit or Delete Item")
        
        item_to_edit = st.selectbox("Select Item to Update/Delete", df['name'].tolist())
        item_data = df[df['name'] == item_to_edit].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander(f"Update {item_to_edit}"):
                new_name = st.text_input("New Name", value=item_data['name'])
                new_cat = st.selectbox("New Category", ["Electronics", "Furniture", "Groceries", "Clothing", "Other"], 
                                     index=["Electronics", "Furniture", "Groceries", "Clothing", "Other"].index(item_data['category']))
                new_qty = st.number_input("New Quantity", min_value=0, value=int(item_data['quantity']))
                new_price = st.number_input("New Price ($)", min_value=0.0, value=float(item_data['price']))
                
                if st.button("Update Item"):
                    update_item(item_data['id'], new_name, new_cat, new_qty, new_price)
                    st.success("Item updated successfully!")
                    st.rerun()
        
        with col2:
            with st.expander(f"Delete {item_to_edit}", expanded=False):
                st.error(f"Are you sure you want to delete {item_to_edit}?")
                if st.button("Confirm Delete"):
                    delete_item(item_data['id'])
                    st.success("Item deleted!")
                    st.rerun()
    else:
        st.info("No items in inventory.")
