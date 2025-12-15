# Date: 15/12/2025--dd/mm/yyyy. 
# Auther: Rashed Alothman.

# --- ROUTE STRUCTURE YOU PROVIDED ---
# "/" → landing/diagnostic page
# "/home" → main dashboard
# "/home/tasks/add_tasks" → add a task
# "/home/task/delete_task" → delete a task
# "/home/AddUsersToAccount" → placeholder
# "/home/User/about" → about‑me page
# "/login" → login page
from flask import Flask ,request,render_template
tasks = []
app = Flask(__name__, template_folder='templates', static_folder='static')
@app.route("/")
def wheretogo():
    return 0
@app.route("/home")
def helloWorld():
    return "<p> Hello World How the fuck are you!</p>"

@app.route("/home/tasks", methods=["GET"])
def get_tasks():
    return {'tasks': tasks}

@app.route("/home/tasks/add_Tasks",methods=["POST"])
def AddTasks():
    data = request.get_json()
    description = data.get("description")
    task ={
        "id":len(tasks)+1,
        "description":description
    }
    tasks.append(task)
    return {"message":"task addad","task":task},201

@app.route("/home/tasks/delete_task",methods=["DELETE"])
def deleteTask():
    data=request.get_json()
    if not data:
        return ({"error":" No data Provided"}), 400
    task_id=data.get("id")
    TaskHaveBeenDeleted = False
    if not task_id:
        return ({"error": "Task ID is requried"}), 400
    else:
        for task in tasks:
            if task["id"]==task_id:
                tasks.remove(task)
                TaskHaveBeenDeleted =True
                break
    if TaskHaveBeenDeleted:
        return ({"message":" Task deleted"}), 200
    else:
        return ({"message": "Task not found, no found"}), 404

@app.route("/home/AddUsersToAccout")
def addUsers(email):
    return 0
@app.route("/home/User/about me")
def aboutMe():
    return 0
@app.route("/login")
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)
