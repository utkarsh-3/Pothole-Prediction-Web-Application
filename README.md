
The web application will detect the potholes in the image uploaded on the app and validated pothole image along with pic metadata will be stored in the database and visible to admin.

Steps To Run

1.Download the project.
2.Install all the requirements of the project "pip install -r requirement.txt". If any error in downloading any module use "pip install <module_name>"

3.Run command "python database.py" to create necessary tables in the databases.

4.Edit the "app.py" change the directory location of your "upload" folder. app.config["IMAGE_UPLOADS"] = "C:/Users/Desktop/project/flask-tutorial/uploads"

5.Run the command in cmd "python app.py"

Functionalities

Login/Register to the Web Application
Upload pothole picture along with other data.
Machine learning model (accuracy>95%) will predict the presence of pothole in the image.
If the pothole is detected, the data associated with that image will be stored in the database.
Note: Feel free to modify and contact.
