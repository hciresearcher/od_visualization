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
from tqdm import tqdm

'''
https://wooiljeong.github.io/python/mapboxgl/ 링크 참고해서 아래 my_token에 본인 토큰 넣기
'''
class Showmap:
    def __init__(self, year, month, hour, age, dropdowns, token, polydata):
        self.year = year
        self.month = month
        self.hour = hour
        self.age = age
        self.remain_condition = dropdowns
        self.token = token
        self.polydata = polydata
    
    def heatmap(self):
        
        total_start = time()

        day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
        print(f'---- 1. 데이터 로드 ---- {day}')
        
        move_text = self.remain_condition[0]
        gender_text = self.remain_condition[1]
        scatter_text = self.remain_condition[2]
        color_text = self.remain_condition[3]
        maxscale_text = self.remain_condition[4]

        ###### test1 ######
        start1 = time()
        
        # OD 핕터링
        if move_text == "유입+유출":
            filter_file_1_1 = glob('D://Data_Visualization//Data//kt_전처리_ver2//heat//*유입.pkl')
            filter_file_1_2 = glob('D://Data_Visualization//Data//kt_전처리_ver2//heat//*유출.pkl')
            filter_file_1 = filter_file_1_1 + filter_file_1_2
        else:
            filter_file_1 = glob(f'D://Data_Visualization//Data//kt_전처리_ver2//heat//*{move_text}.pkl')
        
        filter_file_2 = []; filter_file_3 = []; filter_file_4 = []; filter_file_5 = []; filter_file_6 = []
        
        # 성별 핕터링
        if gender_text == "남성":
            filter_file_2 = [file for file in filter_file_1 if "남성" in file]
        elif gender_text == "여성":
            filter_file_2 = [file for file in filter_file_1 if "여성" in file]
        else:
            filter_file_2 = filter_file_1
        
        # 연도, 월, 시간, 연령 필터링
        for y in self.year:
            filter_file_3 += [file for file in filter_file_2 if f"{y}" in file]

        for m in self.month:
            filter_file_4 += [file for file in filter_file_3 if f"{m}" in file]
        
        for h in self.hour:
            filter_file_5 += [file for file in filter_file_4 if f"{h}" in file]
        
        for a in self.age:
            filter_file_6 += [file for file in filter_file_5 if f"{a}" in file]
        
        end1 = time()
        print(f"test 1 걸린 시간은 {end1-start1:.4f}초입니다.")
        
        ###### test2 ######
        start1 = time()


        # 모든 DataFrame을 하나로 합칩니다.
        all_data = pd.DataFrame()
        list_df = []
        
        
        
        for index, file_name in enumerate(tqdm(filter_file_6)):
            data = pd.read_pickle(file_name)
            
            list_df.append(data)
            del data
            
        del filter_file_1, filter_file_2, filter_file_3, filter_file_4, filter_file_5, filter_file_6
        gc.collect()
                
        all_data = pd.concat(list_df, axis=0, ignore_index=True)
        end1 = time()
        print(f"test 2 걸린 시간은 {end1-start1:.4f}초입니다.")
        
        ###### test3 ######
        start1 = time()
        
        del list_df
        gc.collect()
        

        if move_text == '유출':
            concat_data = all_data.drop(['destination'], axis=1)
            concat_data.rename(columns={'origin': 'polycode'}, inplace=True)
            
        elif move_text == '유입':
            concat_data = all_data.drop(['origin'], axis=1)
            concat_data.rename(columns={'destination': 'polycode'}, inplace=True)
            
        else:
            add1_data = all_data.drop(['origin'], axis=1)
            add1_data.rename(columns={'destination': 'polycode'}, inplace=True)
            
            add2_data = all_data.drop(['destination'], axis=1)
            add2_data.rename(columns={'origin': 'polycode'}, inplace=True)
            
            concat_data = pd.concat([add1_data, add2_data], axis=0, ignore_index=True)
        
        del all_data
        gc.collect()
        
        end1 = time()
        print(f"test 3 걸린 시간은 {end1-start1:.4f}초입니다.")

        day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
        print(f'---- 2. group by ---- {day}')
        
        ###### test4 ######        
        start1 = time()                
        groupby_data = round(concat_data.groupby('polycode')['ttime'].mean(), 2).to_frame('평균 이동시간(분)').reset_index()
        dist_data = round(concat_data.groupby('polycode')['dist'].mean(), 2).to_frame('평균 이동거리(m)').reset_index()
        person_data = round(concat_data.groupby('polycode')['personcount'].sum(), 2).to_frame('이동인구수(명)').reset_index()
        end1 = time()
        
        concat_data.drop(['ttime', 'dist', 'personcount'], axis=1, inplace=True)
        
        print(f"test 4 걸린 시간은 {end1-start1:.4f}초입니다.")

        ###### test5 ######
        print("---- 전체 merge ---- {day}")

        start1 = time()
        
        groupby_data = pd.merge(groupby_data, dist_data, on='polycode')
        groupby_data = pd.merge(groupby_data, person_data, on='polycode')
        
        self.polydata = self.polydata.astype({'polycode': 'uint32'})
        merge_gpd = self.polydata.merge(groupby_data, how="left", on="polycode")
        
        del concat_data, groupby_data, dist_data, person_data, self.polydata
        gc.collect()
        
        max_color = int(merge_gpd[scatter_text].max())
        avg_color = int(merge_gpd[scatter_text].mean())
        
        end1 = time()
        print(f"test 5 걸린 시간은 {end1-start1:.4f}초입니다.")
        
        # *** 여기서부터는 바꾸지 못하는 부분 ***
        
        day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
        print(f'---- 4. create geojson ---- {day}')
        
        test1 = time()
        merge_gpd = merge_gpd.dropna().reset_index(drop=True)
        merge_str = merge_gpd.to_json()             
        merge_geojson = json.loads(merge_str)
        
        
        del merge_str
        gc.collect()
        
        test2 = time()
        print(f"test2-test1 걸린 시간은 {test2-test1:.4f}초입니다.")
        
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
            access_token=self.token,
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

        return viz.create_html()

    def flowmap(self):
        
        day = datetime.now().strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
        print(f'---- 1. 데이터 로드 ---- {day}')
        
        move_text = self.remain_condition[0]
        gender_text = self.remain_condition[1]
        scatter_text = self.remain_condition[2]
        color_text = self.remain_condition[3]
        minscale_text = self.remain_condition[4]

        # OD 핕터링
        if move_text == "유입+유출":
            filter_file_1 = glob('D://Data_Visualization//Data//kt_전처리_ver2//flow//*.pkl')
        else:
            filter_file_1 = glob(f'D://Data_Visualization//Data//kt_전처리_ver2//flow//*{move_text}.pkl')
        
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
        for y in self.year:
            filter_file_3 += [file for file in filter_file_2 if f"{y}" in file]

        for m in self.month:
            filter_file_4 += [file for file in filter_file_3 if f"{m}" in file]
        
        for h in self.hour:
            filter_file_5 += [file for file in filter_file_4 if f"{h}" in file]
        
        for a in self.age:
            filter_file_6 += [file for file in filter_file_5 if f"{a}" in file]
                
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
        
        # 최소 표시 기준 관련 설정
        all_data['person_mean'] = all_data[scatter_text].mean()
        
        if minscale_text == '선택안함':
            display_data = all_data[all_data['personcount'] >= all_data['person_mean']]
        else:
            display_data = all_data[all_data['personcount'] >= int(minscale_text)]

        all_data.drop(['person_mean'], axis=1, inplace=True)
        
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
                
        return flow_html