# First commant in the project.
# Date: 10/12/2025--dd/mm/yyyy. 
# Auther: Rashed Alothman.
# I just want to say to myself i wish you the best.
from flask import Flask

app = Flask(__name__)

@app.route("/")
def helloWorld():
    return "<p> Hello World How the fuck are you!</p>"
