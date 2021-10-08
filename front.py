from flask import Flask, render_template, request
import sklearn
import jsonify
import pickle
import requests

app= Flask(__name__, static_folder = 'static')


classifier = pickle.load(open('model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def index():
    return render_template('carwebpage.html')

@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year= int(request.form["Year"])
        Owner= float(request.form["Owner"])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=float(request.form['Kms_Driven'])    
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
    if(Fuel_Type_Petrol=='Petrol'):
        Fuel_Type_Petrol=1
        Fuel_Type_Diesel=0
    elif(Fuel_Type_Petrol=='Diesel'):
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=1
    else:
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=0
    Year= 2021 - Year
    
    Seller_Type_Individual= request.form['Seller_Type_Individual']
    if(Seller_Type_Individual=='Individual'):
        Seller_Type_Individual=1
    else:
        Seller_Type_Individual=0
    
    Transmission_Manual = request.form['Transmission_Manual']
    if(Transmission_Manual=='Manual'):
        Transmission_Manual=1
    else:
        Transmission_Manual=0    
    
    predict_= classifier.predict([[Present_Price,Kms_Driven,Owner,Fuel_Type_Diesel,
                                   Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual,Year]])
    car_price = round(predict_[0],2)
    if car_price<0:
        return render_template('carwebpage.html',Predicted_Price= 'Sorry, your car is priceless. Do not sell it!')
    else:
        return render_template('carwebpage.html', Predicted_Price="The car can be sold at {} lakhs".format(car_price))
        
if __name__ == "__main__" :
    app.run(debug=True)