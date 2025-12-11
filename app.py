# Date: 11/12/2025--dd/mm/yyyy. 
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
app = Flask(__name__)
@app.route("/")
def wheretogo():
    return 0
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
