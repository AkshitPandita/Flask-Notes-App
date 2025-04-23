#print("Hello world")
from flask import Flask,request,jsonify,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

class Notes(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    note=db.Column(db.String(500),nullable=False)
    time=db.Column(db.DateTime,default=datetime.now())

    def __repr__(self):
        return f"{self.title}-{self.note}"
    
# with app.app_context():
#     db.create_all()

@app.route('/', methods=["POST","GET"])
def hello():

    if request.method=="POST":
        title = request.form.get("title")
        note = request.form.get("note")
        notes=Notes(title=title ,note=note)
        db.session.add(notes)
        db.session.commit()
    allnotes = Notes.query.all()
    
    # data={}
    # for no in allnotes:
    #     data[no.sno] = [no.title,no.note,no.time]
    # return data
    return render_template("index.html", allnotes=allnotes)
    

@app.route('/search', methods=["POST","GET"])
def search():
    allnotes = Notes.query.all()
    if request.method=="GET":
        query=request.args.get('query', '')
        if query:
            filtered_notes = [note for note in allnotes 
            if query.lower() in note.title.lower() or query.lower() in note.note.lower()
        ]
        else:
            filtered_notes = allnotes

    return render_template("index.html", allnotes=filtered_notes,query=query)

@app.route('/about', methods=["POST","GET"])
def about():
    return render_template("about.html")

@app.route('/delete/<int:sno>', methods=["POST","GET"])
def delete(sno):
    note=Notes.query.filter_by(sno=sno).first()
    db.session.delete(note)
    db.session.commit()

    return redirect("/")

@app.route('/update/<int:sno>', methods=["POST","GET"])
    
def update(sno):

    if request.method == "POST":
        title = request.form.get("title")
        note=request.form.get("note")
        new_note = Notes.query.filter_by(sno=sno).first()
        new_note.title=title
        new_note.note = note
        db.session.add(new_note)
        db.session.commit()
        return redirect("/")


    note = Notes.query.filter_by(sno=sno).first()
    return render_template("update.html", note=note)




if __name__=="__main__":
    app.run(debug=True)
