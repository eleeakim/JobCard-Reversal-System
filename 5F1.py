from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import date
import pyodbc
import tkinter.messagebox as messagebox

root = Tk()
root.title("Job Card Reversal")
root.geometry("780x700")
root.resizable(False, False)

# Establish connection to SQL Server database
driver = "{ODBC Driver 17 for SQL Server}"
server = "DESKTOP-8R2SKOA\\SQLEXPRESS"
database = "Job Costing"
username = "nyawinda"
password = "nyawinda"

conn = pyodbc.connect("DRIVER=" + driver
+ ";SERVER=" + server
+ ";DATABASE=" + database
+ ";UID=" + username
+ ";PWD=" + password )

# Define a function to search for a job card
def search_job_card():
    # Get the search term from the search box
    search_term = search_box.get()
    # Clear the existing data from the job card list
    trv.delete(*trv.get_children())
    # Execute SQL query to retrieve matching job cards
    cursor.execute(f"SELECT IdJCMaster, cJobCode, iClientId, cDescription, iStatus FROM _btblJCMaster WHERE cJobCode LIKE '%{search_term}%'")
    rows = cursor.fetchall()
    # Insert matching job cards into the treeview widget
    for row in rows:
        # Strip any leading or trailing spaces from the data
        cleaned_row = [item.strip() if isinstance(item, str) else item for item in row]
        trv.insert("", "end", values=cleaned_row)

# Execute SQL query to retrieve data from table"""
"""def display_corresponding_rows(event):
    selected_item = trv.focus()
    selected_item_values = trv.item(selected_item, 'values')
    id_jc_master = selected_item_values[0]
    cursor.execute(f"SELECT idJCTxLines, iStockID, cDescription, iSource, fUnitPriceIncl, fUnitCost, fTransQty, iWarehouseID FROM _btblJCTxLines WHERE iJCMasterID={id_jc_master} AND iSource = 0")
    rows = cursor.fetchall()
    # Clear existing rows from trv2
    for child in trv2.get_children():
        trv2.delete(child)
    # Insert new rows into trv2
    for row in rows:
    # Strip any leading or trailing spaces from the data
     cleaned_row = [item.strip() if isinstance(item, str) else item for item in row]
     trv2.insert("", "end", values=cleaned_row)"""

def display_corresponding_rows(event):
    selected_item = trv.focus()
    selected_item_values = trv.item(selected_item, 'values')
    if selected_item_values:
        id_jc_master = selected_item_values[0]
        cursor.execute(f"SELECT idJCTxLines, iStockID, cDescription, iSource, fUnitPriceIncl, fUnitCost, fTransQty, iWarehouseID FROM _btblJCTxLines WHERE iJCMasterID={id_jc_master} AND iSource = 0")
        rows = cursor.fetchall()
        # Clear existing rows from trv2
        for child in trv2.get_children():
            trv2.delete(child)
        # Insert new rows into trv2
        for row in rows:
            # Strip any leading or trailing spaces from the data
            cleaned_row = [item.strip() if isinstance(item, str) else item for item in row]
            trv2.insert("", "end", values=cleaned_row)


def update_amount_entry(*args):
    try:
        unit_cost = float(unit_cost_entry.get())
        quantity = float(quantity_entry.get())
        amount = unit_cost * quantity
        amount_entry.delete(0, END)
        amount_entry.insert(0, amount)
    except ValueError:
        pass

# Define a function to display the selected row's values in the textboxes
"""def display_selected_row_values(event):
    # Get the selected row's values
    selected_item = trv2.focus()
    selected_item_values = trv2.item(selected_item, 'values')
    update_amount_entry()
    
    
    item_code_entry.delete(0, END)
    item_code_entry.insert(0, selected_item_values[1])  
    
    description_entry.delete(0, END)
    description_entry.insert(0, selected_item_values[2])
    
    source_entry.delete(0, END)
    source_entry.insert(0, selected_item_values[3])
    
    unit_price_entry.delete(0, END)
    unit_price_entry.insert(0, selected_item_values[4])
    
    unit_cost_entry.delete(0, END)
    unit_cost_entry.insert(0, selected_item_values[5])
    
    quantity_entry.delete(0, END)
    quantity_entry.insert(0, selected_item_values[6])
    
    warehouse_entry.delete(0, END)
    warehouse_entry.insert(0, selected_item_values[7])"""



def validate_float(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False
    


def reduce_fTransQty():
    # Get the data from the text boxes
    unit_cost = unit_cost_entry.get()
    quantity = quantity_entry.get()
    warehouse = warehouse_entry.get()

    # Execute SQL query to update the record
    selected_item = trv2.focus()
    selected_item_values = trv2.item(selected_item, 'values')
    current_fTransQty = float(selected_item_values[6])
    new_quantity = float(quantity)
    new_fTransQty = current_fTransQty - new_quantity
    
    cursor.execute(f"UPDATE _btblJCTxLines SET fTransQty={new_fTransQty} WHERE idJCTxLines={selected_item_values[0]}")

    # Update the display
    display_corresponding_rows(None)



def display_selected_row_values(event):
    # Get the selected row's values
    selected_item = trv2.focus()
    selected_item_values = trv2.item(selected_item, 'values')
    
    # Display the values in the textboxes
    item_code_entry.delete(0, END)
    item_code_entry.insert(0, selected_item_values[1])  
    
    description_entry.delete(0, END)
    description_entry.insert(0, selected_item_values[2])

    source_entry.delete(0, END)
    source_entry.insert(0, selected_item_values[3])
    
    unit_price_entry.delete(0, END)
    unit_price_entry.insert(0, selected_item_values[4])
    
    unit_cost_entry.delete(0, END)
    unit_cost_entry.insert(0, selected_item_values[5])
    
    quantity_entry.delete(0, END)
    quantity_entry.insert(0, selected_item_values[6])
    
    warehouse_entry.delete(0, END)
    warehouse_entry.insert(0, selected_item_values[7])
    
    update_amount_entry()

# Define a function to insert data into the database table
"""def insert_data():
    # Get the data from the text boxes
    item_code = item_code_entry.get()
    description = description_entry.get()
    source = source_entry.get()
    unit_price = unit_price_entry.get()
    unit_cost = unit_cost_entry.get()
    quantity = quantity_entry.get()
    warehouse = warehouse_entry.get()
    amount =  amount_entry.get()
    return_date = return_date_entry.get()

    reduce_fTransQty()

    # Execute the SQL statement to insert the data into the database table
    cursor.execute(f"INSERT INTO _btblJCTxLines (iStockID, cDescription, iSource, fUnitPriceIncl, fUnitCost, fTransQty, iWarehouseID) VALUES ('{item_code}', '{description}', '{source}', '{unit_price}', '{unit_cost}', '{quantity}', '{warehouse}')")
    cursor.execute(f"INSERT INTO PostST (TxDate, Id, Credit, Description, Quantity, Cost, WarehouseID)  VALUES ('{return_date}', '{item_code}','{amount}', '{description}', '{quantity}', '{unit_cost}', '{warehouse}')")
    cursor.execute(f"INSERT INTO PostGL (TxDate, Id, Debit, Description)  VALUES ('{return_date}', '{item_code}', '{amount}', '{description}')")
    cursor.execute(f"INSERT INTO PostGL (TxDate, Id,Credit, Description)  VALUES ('{return_date}', '{item_code}', '{amount}', '{description}')")
    cursor.execute(f"INSERT INTO _etblStockQtys (StockID, WhseID, QtyJCWIP) VALUES ('{item_code}', '{warehouse}','{quantity}')")
    # Commit the changes to the database
    conn.commit()"""



def insert_data():
    # Get the data from the text boxes
    item_code = item_code_entry.get()
    description = description_entry.get()
    source = source_entry.get()
    unit_price = unit_price_entry.get()
    unit_cost = unit_cost_entry.get()
    quantity = quantity_entry.get()
    warehouse = warehouse_entry.get()
    amount = amount_entry.get()
    return_date = return_date_entry.get()

    reduce_fTransQty()

    # Ask for confirmation before executing SQL statements
    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to insert the data?")
    if not confirmed:
        return

    try:
        # Execute the SQL statement to insert the data into the database table
        cursor.execute(f"INSERT INTO _btblJCTxLines (iStockID, cDescription, iSource, fUnitPriceIncl, fUnitCost, fTransQty, iWarehouseID) VALUES ('{item_code}', '{description}', '{source}', '{unit_price}', '{unit_cost}', '{quantity}', '{warehouse}')")
        cursor.execute(f"INSERT INTO PostST (TxDate, Id, Credit, Description, Quantity, Cost, WarehouseID)  VALUES ('{return_date}', '{item_code}','{amount}', '{description}', '{quantity}', '{unit_cost}', '{warehouse}')")
        cursor.execute(f"INSERT INTO PostGL (TxDate, Id, Debit, Description)  VALUES ('{return_date}', '{item_code}', '{amount}', '{description}')")
        cursor.execute(f"INSERT INTO PostGL (TxDate, Id,Credit, Description)  VALUES ('{return_date}', '{item_code}', '{amount}', '{description}')")
        cursor.execute(f"INSERT INTO _etblStockQtys (StockID, WhseID, QtyJCWIP) VALUES ('{item_code}', '{warehouse}','{quantity}')")
        # Commit the changes to the database
        conn.commit()

        # Show success message
        messagebox.showinfo("Success", "Data has been inserted successfully!")
    except Exception as e:
        # Show error message if there is any exception
        messagebox.showerror("Error", f"Error occurred while inserting data:\n{str(e)}")



trv = ttk.Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height="5")
trv.grid(row=0, column=0, columnspan=6, padx=20, pady=20)
trv.heading(1, text="IdJCMaster")
trv.heading(2, text="Job Code")
trv.heading(3, text="Customer")
trv.heading(4, text="Description")
trv.heading(5, text="Status")
trv.bind("<Double-1>", display_corresponding_rows)
trv.column(1, width=0, stretch=tk.NO)
trv.column(2, width=100)
trv.column(3, width=100)
trv.column(4, width=380)
trv.column(5, width=150)

cursor = conn.cursor()
cursor.execute('SELECT IdJCMaster, cJobCode, iClientId, cDescription, iStatus FROM _btblJCMaster')
rows = cursor.fetchall()

# Insert data into treeview widget
for row in rows:
    # Strip any leading or trailing spaces from the data
    cleaned_row1 = [item.strip() if isinstance(item, str) else item for item in row]
    trv.insert("", "end", values=cleaned_row1)

search_box = Entry(root)
search_box.grid(row=1, column=0)
search_button = Button(root, text="Search Job card", command=search_job_card)
search_button.grid(row=1, column=1)

trv2 = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height="9")
trv2.grid(row=2, column=0, columnspan=8, padx=20, pady=20)
# Define the style for the column header
style = ttk.Style()
style.configure("Treeview.Heading", font=("Georgia", 8), background="Red")
trv2.heading(1, text=" ")
trv2.heading(2, text="Item Code")
trv2.heading(3, text="Description")
trv2.heading(4, text="Source")
trv2.heading(5, text="Unit Price")
trv2.heading(6, text="Unit Cost")
trv2.heading(7, text="Quantity")
trv2.heading(8, text="Warehouse")

# Bind the display_selected_row_values function to the Double-1 event of the trv2 treeview widget
trv2.bind("<Double-1>", display_selected_row_values)
trv2.column(1, width=0, stretch=tk.NO)
trv2.column(2, width=90)
trv2.column(3, width=250)
trv2.column(4, width=80)
trv2.column(5, width=80)
trv2.column(6, width=80)
trv2.column(7, width=80)
trv2.column(8, width=80)

cursor.execute('SELECT idJCTxLines, iStockID, cDescription, iSource, fUnitPriceIncl, fUnitCost, fTransQty, iWarehouseID FROM _btblJCTxLines WHERE iSource = 0' )
rows = cursor.fetchall()

# Insert data into treeview widget
for row in rows:
    # Strip any leading or trailing spaces from the data
    cleaned_row = [item.strip() if isinstance(item, str) else item for item in row]
    trv2.insert("", "end", values=cleaned_row)

# Create labels for the text boxes
label1 = Label(root, text="Item Code")
label2 = Label(root, text="Description")
label3 = Label(root, text="Source")
label4 = Label(root, text="Unit Price")
label5 = Label(root, text="Unit Cost")
label6 = Label(root, text="Quantity")
label7 = Label(root, text="Warehouse")
label8 = Label(root, text="Return date")
label9 = Label(root, text="Amount")

# Create text boxes
item_code_entry = Entry(root)
description_entry = Entry(root)
source_entry = Entry(root)
unit_price_entry = Entry(root)
unit_cost_entry = Entry(root)
quantity_entry = Entry(root, validate="key", validatecommand=(validate_float, '%P'), width=20)
warehouse_entry = Entry(root)
return_date_entry = Entry(root)

today = date.today()
return_date_entry.insert(0, today.strftime("%m/%d/%Y"))
return_date_entry.config(state='readonly')

amount_entry = Entry(root)
unit_cost_entry.bind("<KeyRelease>", update_amount_entry)
quantity_entry.bind("<KeyRelease>", update_amount_entry)

quantity_entry.bind('<FocusOut>', update_amount_entry) # Bind the function to the FocusOut event of the Entry widget

# Set the position of labels and text boxes using grid layout
label1.grid(row=3, column=0, padx=10, pady=10)
label2.grid(row=4, column=0, padx=10, pady=10)
label3.grid(row=5, column=0, padx=10, pady=10)
label4.grid(row=6, column=0, padx=10, pady=10)
label5.grid(row=3, column=2, padx=10, pady=10)
label6.grid(row=4, column=2, padx=10, pady=10)
label7.grid(row=5, column=2, padx=10, pady=10)
label8.grid(row=6, column=2, padx=20, pady=10)
label9.grid(row=7, column=0, padx=20, pady=20)

# Set the position of text boxes using grid layout
item_code_entry.grid(row=3, column=1, pady=10)
description_entry.grid(row=4, column=1, padx=10, pady=10)
source_entry.grid(row=5, column=1, padx=10, pady=10)
unit_price_entry.grid(row=6, column=1, padx=10, pady=10)
unit_cost_entry.grid(row=3, column=3, padx=10, pady=10)
quantity_entry.grid(row=4, column=3, padx=10, pady=10)
warehouse_entry.grid(row=5, column=3, padx=10, pady=10)
return_date_entry.grid(row=6, column=3, padx=20, pady=5)
amount_entry.grid(row=7, column=1, padx=20, pady=20)

# Set the position of button using grid layout
insert_button = Button(root, text="Process", command=insert_data, width=10)
insert_button.grid(row=7, column=3, pady=10)

root.mainloop()