import random
import os
import ast
from flask import render_template, request

def find_the_thai(dir):
    numbers_of_thais = 5
    image_lst = [image for image in os.listdir(os.path.join(dir, 'static')) if not image.startswith('1')]
    random.shuffle(image_lst)
    
    random_img = image_lst[:numbers_of_thais]
    
    if request.method == 'POST':
        try:
            placed_bet = int(request.form['placedBet'])
            choosen_thai = int(request.form['choosenThai'])
            same_images_str = request.form.get('resendImages', '[]')
            same_images_list = ast.literal_eval(same_images_str)
        except (ValueError, SyntaxError):
            placed_bet = 0
            choosen_thai = 0
            same_images_list = []
        
        result = random.randint(0, 4)
        profit = placed_bet * 5 if result == choosen_thai else -placed_bet

        return render_template("test/find_the_thai.html",
                               numbers_of_thais=numbers_of_thais,
                               profit=profit,
                               choosenThai=choosen_thai,
                               placedBet=placed_bet,
                               result=result,
                               first_time=0,
                               random_img=same_images_list)
    else:
        return render_template("test/find_the_thai.html",
                               numbers_of_thais=numbers_of_thais,
                               first_time=1,
                               random_img=random_img)
