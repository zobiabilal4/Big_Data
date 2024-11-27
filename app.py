from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'secret_key_here'

# MongoDB configuration
client = MongoClient('mongodb+srv://bzobia2002:my04122002@cluster-lab5.xkizq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-lab5')  # Replace with your connection string if using MongoDB Atlas
db = client['linkedin_profiles']
collection = db['profiles']

# Flask-WTF Form for LinkedIn Profiles
class ProfileForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone")
    education = TextAreaField("Education")
    experience = TextAreaField("Professional Experience")
    submit = SubmitField("Save Profile")

@app.route("/", methods=["GET", "POST"])
def home():
    form = ProfileForm()
    if form.validate_on_submit():
        profile = {
            "name": form.name.data,
            "email": form.email.data,
            "phone": form.phone.data,
            "education": form.education.data,
            "experience": form.experience.data,
        }
        collection.insert_one(profile)
        return redirect(url_for("profiles"))
    return render_template("index.html", form=form)

@app.route("/profiles", methods=["GET"])
def profiles():
    profiles = list(collection.find())
    return render_template("profiles.html", profiles=profiles)

@app.route("/profile/delete/<profile_id>", methods=["POST"])
def delete_profile(profile_id):
    collection.delete_one({"_id": ObjectId(profile_id)})
    return redirect(url_for("profiles"))

print(client.list_database_names())

if __name__ == "__main__":
    app.run(debug=True)
