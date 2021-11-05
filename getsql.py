#看資料庫table資料
import pandas as pd
import json
def downloadsql():
    import psycopg2
    import json
    conn = psycopg2.connect(database="trail", user="usertrail", password="0111", host="140.115.78.184", port="54326")
    cur=conn.cursor()
    print("Opened database successfully")
    #cur.execute('SELECT id,trail_id,trail_search_id,formatted_address,ST_AsText(location) as location, ST_AsText(viewport_northeast) as viewport_northeast, ST_AsText(viewport_southwest) as viewport_southwest,name,place_id,user_ratings_total FROM spaces_list ')
    cur.execute('SELECT * FROM trail_list ')
    #cur.execute('DELETE FROM spaces_list WHERE id > 0 RETURNING *') #刪除資料用
    #q = 'SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = %s; '
    #cur.execute(q,('trail_list',))
    db_results=cur.fetchall()
    columns = [column[0] for column in cur.description]
    conn.commit()
    cur.close()
    conn.close()
    return db_results, columns
def saveFile():
    trail_results, columns = downloadsql()
    results_json  = [dict(zip(columns, row)) for row in trail_results]
    with open('scenary_trail_list.json', 'w', encoding='utf-8') as f:
        json.dump(results_json, f,ensure_ascii=False)
def match_trail_list(): #還沒改好
    df_places = pd.read_json('./scenary_places_list.json')
    df_trail = pd.read_json('./scenary_trail_list.json')
    df_trail_saved = pd.read_json('./saved.json')
    indx_num = df_trail.index
    for indx in indx_num:
        trail_id = df_trail['id'][indx]
        trail_name = df_trail['name'][indx]
        address = df_places['formatted_address'][indx] 
        googleMap = 'https://www.google.com/maps/place/?q=place_id:' + df_places['place_id'][indx] 
        weatherUrl = ''
        weatherRefName = ''       
        longitude = df_places['location'][indx].split('(')[1].split(' ')[0]
        latitude = df_places['location'][indx].split(' ')[1].split(')')[0]
        location = {'longitude': longitude, 'latitude': latitude}
        #print(f'trail name: {trail_name}')
        # if  trail_name == '石門水庫楓林步道':
        #     print(type(df_trail_saved['trail_name']))
        if  trail_name in df_trail_saved['trail_name'].values:
            print(f'trail_id: {trail_id}')
            print(f'trail name: {trail_name}')
            print(f'address: {address}')
            print(f'googleMap: {googleMap}')
            print(f'weatherUrl: {weatherUrl}')
            print(f'weatherRefName: {weatherRefName}')
            print(f'location: {location}')

#拿所有的places回去對原本的trail id，並做出新的json file
def match_places_list():
    import numpy as np
    df_places = pd.read_json('/home/skai/flask/weatherguide-api/scenary_places_list.json')
    df_trail = pd.read_json('/home/skai/flask/weatherguide-api/scenary_trail_list.json')
    df_trail_saved = pd.read_json('/home/skai/flask/weatherguide-api/saved.json')
    indx_num = df_places.index
    trailNamesOld = df_trail_saved['trail_name'].values
    trailNames = df_trail['name'].values
    count = 0
    trail_list = []
    for indx in indx_num:
        trail_id = df_places['trail_id'][indx]
        trail_search_id = df_places['trail_search_id'][indx]
        trail_name = df_trail[df_trail['id']==trail_id].name.values[0]
        places_trail_name = df_places['name'][indx]
        address = df_places['formatted_address'][indx] 
        googleMap = 'https://www.google.com/maps/place/?q=place_id:' + df_places['place_id'][indx] 
        weatherUrl = ''
        weatherRefName = ''       
        longitude = df_places['location'][indx].split('(')[1].split(' ')[0]
        latitude = df_places['location'][indx].split(' ')[1].split(')')[0]
        location = {'longitude': longitude, 'latitude': latitude}
        #print(f'trail name: {trail_name}')
        # if  trail_name == '石門水庫楓林步道':
        #     print(type(df_trail_saved['trail_name']))
        trail_dict_temp={}
        if  (trail_name in trailNamesOld) and (trail_search_id == 1):
            trail_dict_temp={
                'trail_id': int(trail_id),
                'trail_name': trail_name,
                'google_trail_name': places_trail_name,
                'address': address,
                'googleMap': googleMap,
                'weatherUrl': weatherUrl,
                'weatherRefName': weatherRefName,
                'location': location
                }
            trailNamesOld = np.delete(trailNamesOld, np.where(trailNamesOld == trail_name)) #把對過的list刪掉
            count+=1
            print(f'---\nloop {count}/{indx_num.max()} times\n---')
        elif (trail_name in trailNames) and (trail_search_id == 1):
            trail_dict_temp={
                'trail_id': int(trail_id),
                'trail_name': trail_name,
                'google_trail_name': places_trail_name,
                'address': address,
                'googleMap': googleMap,
                'weatherUrl': weatherUrl,
                'weatherRefName': weatherRefName,
                'location': location
                }
            trailNames = np.delete(trailNames, np.where(trailNames == trail_name)) #把對過的list刪掉
            count+=1
            print(f'---\nloop {count}/{indx_num.max()} times\n---')
        else:
            continue
        trail_list.append(trail_dict_temp)

    print(f'not matched {len(trailNames)} items: {trailNames}') #當初使用google places搜尋trail_name時沒有結果的位置。
    with open('final_trail_list.json', 'w', encoding='utf-8') as f:
        json.dump(trail_list, f,ensure_ascii=False)

#把舊有的資料撈出來另外處理
def match_places_list():
    trail_all = pd.read_json('/home/skai/flask/weatherguide-api/final_trail_list.json', )
    df_trail_saved = pd.read_json('/home/skai/flask/weatherguide-api/saved.json')
    trailNamesOld = df_trail_saved['trail_name'].values
    index_num = trail_all.index
    for indx in index_num:
        #print(indx,trail_all['trail_name'][indx])
        trail_name = trail_all['trail_name'][indx]
        if trail_name in trailNamesOld:
            #trail = trail_all.iloc[indx].to_dict()
            trail_dict = df_trail_saved[df_trail_saved['trail_name']==trail_name].to_dict('r')[0]
            print(type(trail_dict))
            print(trail_dict)
            #trail_dict['weatherConditoin']={'description': '氣象局：臺灣各育樂區未來1週逐24小時天氣預報'}
            #print(trail_dict)
        else:
            continue
            #print(trail_all.iloc[indx].to_dict())

#拿所有的places回去對原本的trail id，僅輸出原有的trail name和id，places輸出網址，作人工對照。
def match_trail_and_places():
    import numpy as np
    df_places = pd.read_json('/home/skai/flask/weatherguide-api/scenary_places_list.json')
    df_trail = pd.read_json('/home/skai/flask/weatherguide-api/scenary_trail_list.json')
    df_trail_saved = pd.read_json('/home/skai/flask/weatherguide-api/saved.json')
    indx_num = df_places.index
    trailNamesOld = df_trail_saved['trail_name'].values
    trailNames = df_trail['name'].values
    count = 0
    for indx in indx_num:
        trail_id = df_places['trail_id'][indx]
        trail_search_id = df_places['trail_search_id'][indx]
        trail_name = df_trail[df_trail['id']==trail_id].name.values[0]
        places_trail_name = df_places['name'][indx]
        user_ratings_total= df_places['user_ratings_total'][indx]
        googleMapUrl = 'https://www.google.com/maps/place/?q=place_id:' + df_places['place_id'][indx]    
        longitude = df_places['location'][indx].split('(')[1].split(' ')[0]
        latitude = df_places['location'][indx].split(' ')[1].split(')')[0]
        location = {'longitude': longitude, 'latitude': latitude}
        if  (trail_name not in trailNamesOld) and (float(latitude)>24.7):
            myCsvRow=f'{trail_id},{trail_search_id},{trail_name},{googleMapUrl},{places_trail_name},{user_ratings_total}\n'
            trailNames = np.delete(trailNames, np.where(trailNames == trail_name)) #把對過的list刪掉
            with open('/home/skai/flask/weatherguide-api/check_trail_lat24.7.csv','a') as fd:
                    fd.write(myCsvRow)
            count+=1
            print(f'---\nloop {count}/{indx_num.max()} times\n---')
    print(f'not matched {len(trailNames)} items: {trailNames}') #當初使用google places搜尋trail_name時沒有結果的位置。
    
    # with open('final_trail_list.json', 'w', encoding='utf-8') as f:
    #     json.dump(trail_list, f,ensure_ascii=False)
match_trail_and_places()