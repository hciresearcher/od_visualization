from flask import Flask, render_template, jsonify
import os
from flask import request
import geopandas as gpd
from showmap import Showmap
# from showmap_test import Showmap
from time import time

print(f"현재 위치: {os.getcwd()}")

'''
https://wooiljeong.github.io/python/mapboxgl/
위의 링크 참고해서 아래 my_token에 본인 토큰 넣기
'''
my_token = "pk.eyJ1IjoiY2tkcnJycmxsbCIsImEiOiJjbHEzb2dmZnEwZTJiMmtvMzI3bWQ0eDRpIn0.VbkRym5dGEvZoD6aik7duA"
poly_filepath = r'D:/Data_Visualization/polycode/SEOUL_LIVMOV_POLYCODE_SHP/SEOUL_LIVMOV_POLYCODE_변환.shp'
polydata = gpd.read_file(poly_filepath, encoding='utf-8')

app = Flask(__name__)

@app.route('/')
def first():
    # with open(r'D:/Data_Visualization/Code/web_flask2/templates/first_page.html', 'r', encoding='UTF-8') as f:
    #     init_html = f.read()
    return render_template('first_page.html')

@app.route('/main')
def main():
    with open(r'D:/Data_Visualization/Code/web_flask2/templates/init_html.html', 'r', encoding='UTF-8') as f:
        init_html = f.read()
    return render_template('index.html', map_html=init_html)

@app.route('/main/heat', methods=['GET','POST'])
def heat():
    if request.method == 'POST':
        
        selected_year = request.form.getlist('year')
        selected_month = request.form.getlist('month')
        selected_hour = request.form.getlist('hour')
        selected_age = request.form.getlist('age')
        selected_od = request.form['od']
        selected_sex = request.form['sex']
        selected_dist = request.form['distribution']
        selected_color = request.form['map_color']
        selected_criteria = request.form['criteria_value']
        
        button_value = request.form['submit_button']
        
        selected_dropdowns = [selected_od, selected_sex, selected_dist, selected_color, selected_criteria]

        print(f"선택 연도: {selected_year}"); print(f"선택 월: {selected_month}"); print(f"선택 시간대: {selected_hour}"); print(f"선택 나이대: {selected_age}")
        print(f"Selected dropdowns: {selected_dropdowns}")

        print(f"선택한 버튼: {button_value}")
        
        showmap = Showmap(selected_year, selected_month, selected_hour, selected_age, selected_dropdowns, my_token, polydata)
        
        generated_html = showmap.heatmap()
        return render_template('index.html', map_html=generated_html, selected_year1=selected_year, selected_month1=selected_month, 
        selected_hour1=selected_hour, selected_age1=selected_age, selected_od1=selected_od, 
        selected_sex1=selected_sex, selected_dist1=selected_dist, selected_color1=selected_color,
        selected_criteria1=selected_criteria
        )
        
@app.route('/main/flow', methods=['GET','POST'])
def flow():
    if request.method == 'POST':
        
        selected_year = request.form.getlist('year')
        selected_month = request.form.getlist('month')
        selected_hour = request.form.getlist('hour')
        selected_age = request.form.getlist('age')
        selected_od = request.form['od']
        selected_sex = request.form['sex']
        selected_dist = request.form['distribution']
        selected_color = request.form['map_color']
        selected_criteria = request.form['criteria_value']
        
        button_value = request.form['submit_button']
        
        selected_dropdowns = [selected_od, selected_sex, selected_dist, selected_color, selected_criteria]

        print(f"선택 연도: {selected_year}"); print(f"선택 월: {selected_month}"); print(f"선택 시간대: {selected_hour}"); print(f"선택 나이대: {selected_age}")
        print(f"Selected dropdowns: {selected_dropdowns}")

        print(f"선택한 버튼: {button_value}")
        
        showmap = Showmap(selected_year, selected_month, selected_hour, selected_age, selected_dropdowns, my_token, polydata)
        
        generated_html = showmap.flowmap()
        return render_template('index.html', map_html=generated_html, selected_year2=selected_year, selected_month2=selected_month, 
                    selected_hour2=selected_hour, selected_age2=selected_age, selected_od2=selected_od, 
                    selected_sex2=selected_sex, selected_dist2=selected_dist, selected_color2=selected_color,
                    selected_criteria2=selected_criteria, button_value = button_value
                    )
            
if __name__ == '__main__':
    app.run(debug=True)
