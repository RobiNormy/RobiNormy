from flask import *
import pymysql as ps
app = Flask(__name__)

app.secret_key ="udjdjkjjjfo"

@app.route("/hypertension",methods=["GET","POST"])
def project():
    if request.method == "POST":
            data = request.form
            import pandas
            data = pandas.read_csv("datasets/Hypertension-risk-model-main.csv")
            data['Risk'].replace({1:"At Risk",0:"Not at Risk"},inplace=True)
            data['gender'].replace({"Male":1,"Female":0},inplace=True)
            data['currentSmoker'].replace({"Yes":1,"No":0},inplace=True)
            data['diabetes'].replace({"Yes":1,"No":0},inplace=True)
            data['BPMeds'].replace({"Yes":1,"No":0},inplace=True)
            
            array = data.values
            X = array[:,0:12]
            Y =array[:,12]
            from sklearn  import model_selection
            X_train,X_test,Y_train,Y_test = model_selection.train_test_split(X, Y, test_size=0.1,random_state=42)
            from sklearn.naive_bayes import GaussianNB
            from sklearn.linear_model import LogisticRegression
            from sklearn.svm import SVC
            model = SVC()
            model.fit(X_train, Y_train)
            gender = request.form['Gender']
            age = request.form['Age']
            currentSmoker = request.form['currentSmoker']
            cigsPerDay = request.form['cigsPerDay']
            BPMeds = request.form['BPMeds']
            diabetes = request.form['diabetes']
            totChol = request.form['totChol']
            sysBP = request.form['sysBP']
            diaBP = request.form['diaBP']
            BMI = request.form['BMI']
            heartRate = request.form['heartRate']
            glucose = request.form['glucose']
            data = [[gender,age,currentSmoker,cigsPerDay,BPMeds,diabetes,totChol,sysBP,diaBP,BMI,heartRate,glucose]]
            response = model.predict(data)
            return render_template("datascience.html",prediction=response)
    else:
      return render_template("datascience.html")
if __name__ == "__main__":
	app.run(debug=True)





