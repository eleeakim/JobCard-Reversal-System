# Video Demo
https://github.com/eleeakim/jobcard-reversal-application/assets/103770049/e43618f8-d46e-4deb-a569-0cb4855c6321

This code is a Python script that uses the tkinter library to create a graphical user interface (GUI) for a job costing application. The application connects to a SQL Server database to retrieve and update data. The GUI has several widgets, including text boxes, buttons, and treeview widgets, that allow the user to interact with the data.

The purpose of the code is to provide a way for users to search for and view job cards, which contain information about the work performed on a particular job. The user can search for job cards using a search box, and the matching job cards are displayed in a treeview widget.

When the user selects a job card from the treeview, the corresponding rows from the db table are displayed in a second treeview widget. The user can select a row from the second treeview to view and update the details of the job card. The user can update the unit cost, quantity, and warehouse of the selected row and then click on the "Process" button to save the changes back to the database.
