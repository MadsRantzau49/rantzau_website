import random
from flask import Flask, render_template, request
import os
import ast

#Making it a webpage
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/find_the_thai.html', methods=['POST','GET'])
def find_the_thai():
    numbers_of_thais = 5
    imageLst =[]
    for image in os.listdir('C:/Users/madsr/OneDrive/Documents/privat_programmering/RobinHoodCasino/spil/find_the_thai/static/'):
        if image[0] != "1":
            imageLst.append(image)
    random.shuffle(imageLst)
    

    random_img = []
    for i in range(numbers_of_thais):
        random_img.append(imageLst[i])
                          
    if request.method == 'POST':
        placedBet = int(request.form['placedBet'])
        choosenThai = int(request.form['choosenThai'])
        # Get the string representation of the list from the form
        same_images_str = request.form['resendImages']

        # Convert the string representation back to a list
        same_images_list = ast.literal_eval(same_images_str)
    
        result = random.randint(0,4)
        if result == choosenThai:
            profit = placedBet * 5
        else:
            profit = -1* placedBet

        return render_template("find_the_thai.html",numbers_of_thais=numbers_of_thais, profit=profit,choosenThai=choosenThai,placedBet=placedBet,result=result,first_time=0,random_img=same_images_list)
    else:
        return render_template("find_the_thai.html",numbers_of_thais=numbers_of_thais,first_time=1,random_img=random_img)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5001',debug=True)
