# First commant in the project.
# Date: 10/12/2025--dd/mm/yyyy. 
# Auther: Rashed Alothman.
# I just want to say to myself i wish you the best.
from flask import Flask ,request
app = Flask(__name__)

@app.route("/home")
def helloWorld():
    return "<p> Hello World How the fuck are you!</p>"

@app.route("home/tasks/add_Tasks",methods = ["POST"])
def AddTasks():
    data = request.get_json()
    descripton = data.get("description")
    task ={
        "id":len(tasks)+1,
        "descripton":descripton
    }
    task.append(task)
    return {"massage":"task addad","task":task},201

@app.route("home/task/delete_task")
def deleteTask(ID):
    return 0

@app.route("home/AddUsersToAccout")
def addUsers(email):
    return 0
@app.route("home/User/about me")
def aboutMe():
    return 0