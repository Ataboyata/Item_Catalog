##Contents
*app.py: contains all the backend python code to manage users, CRUD operations, etc
*database_setup.py: contains the necessary code to start a Postgre SQL database
*lotsofitems.py: contains some random entries to start playing around with the app
*client_secrets.json: contains the necessary IDs to run Google OAuth
*/templates: folder containg all the html template files for the front-end
*/static: folder containing some basic css for styling

##Instructions
1. Create a virtual machine with Virtual Box and Vagrant. Make sure this virtual machine serves as a server that accepts TCP/IP connecting on the 8000 port in the local server.
2. From the terminal, run the database_setup.py (i.e. python database_setup.py)
3. From the terminal, run the app.py (i.e. python app.py)
4. On your local machine open up a browser an type "http://localhost:8000". This should take you directly to the main catalog. On the left side you should see the possible race categories and on the right side all the possible races. Clicking on any of the categories filters out the races to show those related to the category just clicked. 
*When clicking on "Add Race", a new browser window will be shown with the a "Google Sign-In" button. User must log-in using a Google account. After authenticating with the Google button, the browser will take you back to the main page. Now you are free to add or edit all items in the catalog. 
*When clicking on any of the races on the right side, a description of the specific race will appear. With the two options of editing or deleting the race. If the user is already logged-in, he will have the option of doing just that.
