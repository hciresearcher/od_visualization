#%%
# -*- coding: utf-8 -*-
from mapboxgl.viz import *
from mapboxgl.utils import *
import pandas as pd
import numpy as np
import json
from datetime import datetime
from time import time
import pickle
import gc
from glob import glob
import pydeck as pdk
import geopandas as gpd
from tqdm import tqdm
'''
https://wooiljeong.github.io/python/mapboxgl/ 링크 참고해서 아래 my_token에 본인 토큰 넣기
'''
my_token = "pk.eyJ1IjoiY2tkcnJycmxsbCIsImEiOiJjbHEzb2dmZnEwZTJiMmtvMzI3bWQ0eDRpIn0.VbkRym5dGEvZoD6aik7duA"
poly_filepath = r'D:/Data_Visualization/polycode/SEOUL_LIVMOV_POLYCODE_SHP/SEOUL_LIVMOV_POLYCODE_변환.shp'
polydata = gpd.read_file(poly_filepath, encoding='utf-8')

pd.set_option('display.max_columns', None)

year = ['2020년']
month = [' 1월']
hour = [' 6시', ' 7시', ' 8시', ' 9시', ' 10시']
age = [' 20세', ' 30세', ' 40세', ' 50세', ' 60세']
dropdowns = ['유입+유출', '남성', '이동인구수(명)', 'OrRd', '100']

move_text = dropdowns[0]
gender_text = dropdowns[1]
scatter_text = dropdowns[2]
color_text = dropdowns[3]
maxscale_text = dropdowns[4]

#%%
total_start = time()

day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
print(f'---- 1. 데이터 로드 ---- {day}')

###### test1 ######
start1 = time()

# OD 핕터링 
inflow_file = glob(f'D://Data_Visualization//Data//kt_전처리//*유입.pkl')
outflow_file = glob(f'D://Data_Visualization//Data//kt_전처리//*유출.pkl')

filter_file_2 = []
filter_file_3 = []
filter_file_4 = []
filter_file_5 = []
filter_file_6 = []

# 성별 핕터링
if gender_text == "남성":
    filter_file_2 = [file for file in filter_file_1 if "남성" in file]
elif gender_text == "여성":
    filter_file_2 = [file for file in filter_file_1 if "여성" in file]
else:
    filter_file_2 = filter_file_1

# 연도, 월, 시간, 연령 필터링
for y in year:
    filter_file_3 += [file for file in filter_file_2 if f"{y}" in file]

for m in month:
    filter_file_4 += [file for file in filter_file_3 if f"{m}" in file]

for h in hour:
    filter_file_5 += [file for file in filter_file_4 if f"{h}" in file]

for a in age:
    filter_file_6 += [file for file in filter_file_5 if f"{a}" in file]

end1 = time()
print(f"test 1 걸린 시간은 {end1-start1:.4f}초입니다.")
# -> 10368개의 pickle 파일

#%%
###### test2 ######
start1 = time()

# 모든 DataFrame을 하나로 합칩니다.
all_data = pd.DataFrame()
list_df = []

for file_name in filter_file_6:
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
        list_df.append(data)
        
del filter_file_6
gc.collect()

all_data = pd.concat(list_df, axis=0, ignore_index=True)
    
end1 = time()
print(f"test 2 걸린 시간은 {end1-start1:.4f}초입니다.")

#%%

all_data[all_data.duplicated()]

###### test3 ######
# start1 = time()

# all_data.drop(['lon_des', 'lat_des', 'lon_ori', 'lat_ori'], axis=1, inplace=True)

# end1 = time()
# print(f"test 3 걸린 시간은 {end1-start1:.4f}초입니다.")

# #%%
# ###### test5 ######
# start1 = time()

# print(f"중복 제거 되기 전 행 개수 : {all_data.shape[0]}")
# print(f"중복된 행 개수 : {all_data.duplicated().sum()}")

# duplicate_rows = all_data[all_data.duplicated(keep=False)]
# print(duplicate_rows)

# #%%
# test_data = all_data.drop_duplicates(
#                             keep='first', ignore_index=True)

# print(f"중복 제거된 후 행 개수 : {test_data.shape[0]}")

# end1 = time()
# print(f"test 5 걸린 시간은 {end1-start1:.4f}초입니다.")

#%%
###### test4 ######
start1 = time()

if move_text == '유출':
    rip_data = all_data.drop(['destination'], axis=1)
    rip_data.rename(columns={'origin': 'polycode'}, inplace=True)
    
elif move_text == '유입':
    rip_data = all_data.drop(['origin'], axis=1)
    rip_data.rename(columns={'destination': 'polycode'}, inplace=True)
    
else:
    rip_data = all_data.drop(['origin'], axis=1)
    rip_data.rename(columns={'destination': 'polycode'}, inplace=True)
    
    add_data = all_data.drop(['destination'], axis=1)
    add_data.rename(columns={'origin': 'polycode'}, inplace=True)
    
    concat_data = pd.concat([rip_data, add_data], axis=0, ignore_index=True)

end1 = time()
print(f"test 4 걸린 시간은 {end1-start1:.4f}초입니다.")

#%%

###### test6 ######
start1 = time()

# rip_data.drop(['gender', 'age', 'od', 'nationality', 'oriYear', 'desYear',
#                 'oriMonth', 'desMonth', 'oriHour', 'desHour'], axis=1, inplace=True)

end1 = time()
print(f"test 6 걸린 시간은 {end1-start1:.4f}초입니다.")
#%%
###### test7 ######
# allData = rip_data.astype({'polycode': 'int64'})

day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
print(f'---- 2. group by ---- {day}')
#%%
###### test8 ######        
start1 = time()                
groupby_data = round(concat_data.groupby('polycode')['ttime'].mean(), 2).to_frame('평균 이동시간(분)').reset_index()
dist_data = round(concat_data.groupby('polycode')['dist'].mean(), 2).to_frame('평균 이동거리(m)').reset_index()
person_data = round(concat_data.groupby('polycode')['personcount'].sum(), 2).to_frame('이동인구수(명)').reset_index()
end1 = time()
print(f"test 8 걸린 시간은 {end1-start1:.4f}초입니다.")

#%%
###### test9 ######
start1 = time()
final_data = pd.merge(concat_data, groupby_data, how="left", on='polycode')
final_data = pd.merge(final_data, dist_data, how="left", on='polycode')
final_data = pd.merge(final_data, person_data, how="left", on='polycode')

#%%
print(final_data.dtypes)
merge_gpd = pd.merge(polydata, final_data, how="right", on="polycode")
#%%
max_color = int(merge_gpd[scatter_text].max())
avg_color = int(merge_gpd[scatter_text].mean())

#%%
# *** 여기서부터는 바꾸지 못하는 부분 ***

day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
print(f'---- 3. create geojson ---- {day}')
#%%

merge_str = merge_gpd.to_json()
    
#%%
merge_str2 = str(merge_gpd.to_dict(orient='index'))

#%%
merge_geojson = json.loads(merge_str)

#%%
# 최대 기준치 관련 설정
if maxscale_text == '선택안함':
    step = int(int(max_color)/5)
    color_breaks = np.arange(0, max_color+1, step).tolist()
else:
    step = int(int(maxscale_text)/5)
    color_breaks = np.arange(0, int(maxscale_text)+1, step).tolist()    

color_stops = create_color_stops(color_breaks, colors=color_text)
map_center = [126.986, 37.565]

# 2D 지도 생성
viz = ChoroplethViz(
    access_token= my_token,
    data=merge_geojson,
    color_property=scatter_text,
    color_stops=color_stops,
    center=map_center,
    zoom=10)

# html = open('D:\\Data_Visualization\\Code\\web_flask\\templates\\test.html', "w", encoding="UTF-8")
# html.write(viz.create_html())
# html.close()

day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
print(f'---- 4. visaulize ---- {day}')

total_end = time()
print(f"총 걸린 시간은 {total_end-total_start:.4f}초입니다.")

viz.show()

#%%

year = ['2020년']
# month = [' 1월', ' 2월', ' 3월', ' 4월', ' 5월', ' 6월', ' 7월', ' 8월', ' 9월', ' 10월', ' 11월', ' 12월']
month = [' 10월']
# hour = [' 0시', ' 1시', ' 2시', ' 3시', ' 4시', ' 5시', ' 6시', ' 7시', ' 8시', ' 9시', ' 10시', ' 11시', ' 12시', ' 13시', ' 14시', ' 15시', ' 16시', ' 17시', ' 18시', ' 19시', ' 20시', ' 21시', ' 22시', ' 23시']
hour = [' 0시']
# age = [' 0세', ' 10세', ' 20세', ' 30세', ' 40세', ' 50세', ' 60세', ' 70세', ' 80세']
age = [' 0세']
dropdowns = ['유입+유출', '남성+여성', 'personcount', 'OrRd', '100']

move_text = dropdowns[0]
gender_text = dropdowns[1]
scatter_text = dropdowns[2]
color_text = dropdowns[3]
minscale_text = dropdowns[4]

#%%
total_start = time()

day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
print(f'---- 1. 데이터 로드 ---- {day}')

###### test1 ######
start1 = time()

# OD 핕터링
if move_text == "유입+유출":
    filter_file_1 = glob('D://Data_Visualization//Data//kt_전처리_ver2//flow//*.pkl')
else:
    filter_file_1 = glob(f'D://Data_Visualization//Data//kt_전처리//*{move_text}.pkl')


filter_file_2 = []
filter_file_3 = []
filter_file_4 = []
filter_file_5 = []
filter_file_6 = []

# 성별 핕터링
if gender_text == "남성":
    filter_file_2 = [file for file in filter_file_1 if "남성" in file]
elif gender_text == "여성":
    filter_file_2 = [file for file in filter_file_1 if "여성" in file]
else:
    filter_file_2 = filter_file_1

# 연도, 월, 시간, 연령 필터링
for y in year:
    filter_file_3 += [file for file in filter_file_2 if f"{y}" in file]

for m in month:
    filter_file_4 += [file for file in filter_file_3 if f"{m}" in file]

for h in hour:
    filter_file_5 += [file for file in filter_file_4 if f"{h}" in file]

for a in age:
    filter_file_6 += [file for file in filter_file_5 if f"{a}" in file]

end1 = time()
print(f"test 1 걸린 시간은 {end1-start1:.4f}초입니다.")
# -> 10368개의 pickle 파일

#%%
###### test2 ######
start1 = time()

all_data = pd.DataFrame()
list_df = []

for file_name in filter_file_6:
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
        list_df.append(data)
        
print(filter_file_6)
del filter_file_6
gc.collect()

all_data = pd.concat(list_df, axis=0, ignore_index=True)
end1 = time()
print(f"test 2 걸린 시간은 {end1-start1:.4f}초입니다.")

# 최소 표시 기준 관련 설정
all_data['person_mean'] = all_data[scatter_text].mean()

if minscale_text == '선택안함':
    display_data = all_data[all_data['personcount'] >= all_data['person_mean']]
else:
    display_data = all_data[all_data['personcount'] >= int(minscale_text)]
        
layer = pdk.Layer(
    'ArcLayer',
    display_data,
    get_source_position='[lon_ori, lat_ori]',
    get_target_position='[lon_des, lat_des]',
    get_width='1 + 5 * normalized',
    get_source_color='[255, 255, 120]',
    get_target_color='[255, 0, 0]',
    pickable=True,
    auto_highlight=True
)

# pydeck.data_utils.compute_view 는 Points 들의 경도, 위도를 리스트로 주면, 알아서 view_state 를 만들어줍니다.
view_state = pdk.data_utils.compute_view(all_data[['lon_ori', 'lat_ori']].values)
view_state.zoom = 10.2
view_state.bearing = -10
view_state.pitch = 30

flow_map = pdk.Deck(layers=[layer], initial_view_state=view_state)
flow_html = flow_map.to_html(as_string=True)

day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
print(f'---- 2. visaulize ---- {day}')
        
# %%






import geopandas as gpd

# Shapefile 경로 설정
poly_filepath = r'D:/Data_Visualization/polycode/SEOUL_LIVMOV_POLYCODE_SHP/SEOUL_LIVMOV_POLYCODE_변환.shp'

# Shapefile 읽기
polydata = gpd.read_file(poly_filepath, encoding='utf-8')

# 'polycode' 열을 int32로 변환
a1 = polydata.astype({'polycode': 'int32'})

# 결과 확인
print(a1.dtypes)

# 새로운 Shapefile 경로 설정
poly_filepath2 = 'D://Data_Visualization//polycode//SEOUL_LIVMOV_POLYCODE_SHP//SEOUL_LIVMOV_POLYCODE_변환2.shp'

# 변환된 데이터를 새로운 Shapefile로 저장
a1.to_file(poly_filepath2)
# %%

a2 = gpd.read_file(poly_filepath2, encoding='utf-8')
a2.dtypes
# %%
