#python3

import flask
import json
from flask import jsonify, request
import pandas as pd
from flask import render_template
import requests
#from datetime import datetime
import datetime
import os
import csv
from pathlib import Path

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

# Weather Data Processing
A01 = {
    "id": 'A01',
    "trail_name": "九五峰",
    "location": "台灣",
    "googleMap": "https://www.google.com/maps/place/?q=place_id:ChIJ0fQKbj6rQjQRiBO2MyIyDJ8",
	"weatherUrl": "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON",
    "weatherRefName":'南港山',
    "location": {
        "longitude": 121.5864575,
        "latitude": 25.0262459
    },
}
A02 = {
    "id": 'A02',
    "trail_name": "五寮尖山",
    "location": "台灣",
    "googleMap": "https://www.google.com/maps/place/?q=place_id:ChIJj7Jp4xkaaDQRjzdJwTP6TQQ",
	"weatherUrl": "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON",
    "weatherRefName":'金面山',
    "location": {
        "longitude": 121.3656277,
        "latitude": 24.8768431
    }
}

A03 = {
    "id": 'A03',
    "trail_name": "玉山主峰",
    "location": "台灣",
    "googleMap": "https://www.google.com/maps/place/?q=place_id:ChIJbSFIQg4hbzQRpLAN3Li_a3o",
	"weatherUrl": "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON",
    "weatherRefName":'玉山',
    "location": {
        "longitude": 120.957455,
        "latitude": 23.47
    }
}

A04 = {
    "id": 'A04',
    "trail_name": "石門水庫楓林步道",
    "location": "台灣",
    "googleMap": "https://www.google.com/maps/place/?q=place_id:ChIJcY4De909aDQRL9aO5TSdNlc",
	"weatherUrl": "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON",
    "weatherRefName":'石牛山',
    "location": {
        "longitude": 121.2384575,
        "latitude": 24.8136421
    }
}

A05 = {
    "id": 'A05',
    "trail_name": "虎山親山步道",
    "location": "台灣",
    "googleMap": "https://www.google.com/maps/place/?q=place_id:ChIJX9SSyAirQjQR9B9f7PKLqJo",
	"weatherUrl": "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON",
    "weatherRefName":'南港山',
    "location": {
        "longitude": 121.587488,
        "latitude": 25.0320167
    }
}

A06 = {
    "id": 'A06',
    "trail_name": "金面山步道",
    "location": "台灣",
    "googleMap": "https://www.google.com/maps/place/?q=place_id:ChIJp6s0vUWsQjQRLocNbrRbuqA",
	"weatherUrl": "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON",
    "weatherRefName":'劍潭山',
    "location": {
        "longitude": 121.5679539,
        "latitude": 25.0886654
    }
}

A07 = {
    "id": 'A07',
    "trail_name": "皇帝殿山登山步道",
    "location": "台灣",
    "googleMap": "https://www.google.com/maps/place/?q=place_id:ChIJ-RZJUqhVXTQRLshk-UIcL0s",
	"weatherUrl": "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON",
    "weatherRefName":'石尖山',
    "location": {
        "longitude": 121.6762249,
        "latitude": 24.9917929
    }
}

A08 = {
    "id": 'A08',
    "trail_name": "象山親山步道",
    "location": "台灣",
    "googleMap": "https://www.google.com/maps/place/?q=place_id:ChIJJa7chrKrQjQRujG6Hz0IazI",
	"weatherUrl": "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON",
    "weatherRefName":'南港山',
    "location": {
        "longitude": 121.570828,
        "latitude": 25.0273924
    }
}

trails = [A01, A02, A03, A04, A05, A06, A07, A08]

#weather_code [陰,雨,晴] 1.安心上路、2.注意前往、3.不建議前往 ， 同weather數字意涵 cloudy, rainy, sunny
weather_type=['cloudy', 'rainy', 'sunny']
trail_guide = { 
    'A01':{
        "weather_code": [2,2,1], 
        'weather': {'cloudy':'山上風強，一定要穿著抵風的外套，以免受涼',  #先寫死，之後要用模型自己抓來取代
                    'rainy' :'有些濕滑，小心即可。',
                    'sunny' :'怕曬傷的話就穿輕薄長袖吧'
                    },
        'equipment':'記得帶水，保持手機的電量、步道某些地方較暗，建議攜帶頭燈、樓梯很多，坡度陡，建議帶登山杖可減輕膝蓋負擔、記得插擦防蚊液防小蟲',
        'parking':'把車放在瑤池宮',
        'toilet':'從虎山步道走上去的上面沒有廁所、沿途設有公共廁所、沿途設施完善，有乾淨的公共廁所',
        'difficulty': '階梯較陡所以要注意安全、上九五峰要有點體力、步道好走，是輕鬆等級的行程、還算輕鬆的市區郊山路線',
        'info': '四月多來可以往虎山下山看油桐花和螢火蟲，沿途很多五色鳥叫聲',
        'trail_info': '海拔375公尺為拇指山最高山頭，位於信義、南港、大安區的交界處，與南港山系數條步道相連，步道縱橫交錯峰峰相連。全步道位於稜線，需先經由其他步道，爬升約350公尺高度始能接至九五峰步道。峰上巨石為絕佳之展望點，可將台北市風光及四周群山景色盡收眼底，夜景與101煙火秀熱門場地，此峰為楊森將軍以九十五歲的高齡登此山因而命名。'
        }, 
    'A02':{
        "weather_code": [2,3,1], 
        'weather': {'cloudy':'主要要注意陽光照不到之陰影產生的青苔處，真的會蠻滑的',
                    'rainy' :'不要在下雨天或下完雨爬山，石頭非常滑',
                    'sunny' :'裸岩曝曬度高，防曬做足、準備充足水分'
                    },        
        'equipment':'最好攜帶手套以免手掌摩擦過多受傷、建議著登山鞋/雨鞋、稜線上無遮蔽，至少要帽子遮陽防曬、水一定要準備2～3公升，更推薦要攜帶小鹽罐，如果真的抽筋，這真的萬靈丹',
        'parking':'停車可以停在玉里商店這條路邊都可以停車，目測應該可以停4.50台',
        'toilet':'上面沒廁所，出發前有一小甘仔店，借廁所自由投錢、來回約4-6小時，都沒有洗手間',
        'difficulty': '注意安全，手戴手套抓好，有懼高症者勿輕易嚐試、安全防護上五寮尖非常的完善，繩子有抓牢都不會有太大的危險，不過體力會大量消耗',
        'info': '有拉繩索攀岩部分，懼高症要斟酌、距離長需要足夠體力、四點以前下山較適宜、五寮尖山，639公尺，總督府圖根補點，北部三大岩場之一',
        'trail_info': '位於新北市三峽區的五寮尖，因山形如同五座像拳頭般高低起伏的岩峰而得名，是北部三大岩場（五寮尖、筆架山、皇帝殿）之一。沿途需手腳併用、拉繩攀岩始能登頂，其中一段牛背岩到傾斜七、八十度、深約三十多公尺的「峭壁雄峰」斷崖（4號至6號登山圖之間的危稜）尤為精彩，可以充份感受「戰戰兢兢，如臨深淵，如履薄冰」之快感。山頂視野開闊，可遠眺來時路、三峽和鶯歌、樹林等地區，下山後還能順遊大豹溪沿岸風景區或三峽老街、祖師廟一帶。'
        }, 
    'A03':{
        "weather_code": [2,2,1],
        'weather': {'cloudy':'天冷時須注意保暖',
                    'rainy' :'大雨造成步道水流成河',
                    'sunny' :'要小心紫外線'
                    },
        'equipment':'多補充高熱量的食物和多喝開水，保暖也很重要',
        'parking':' 有接駁車可搭回上東埔停車場',
        'toilet':'無廁所,要喝水尿尿的人建議在排雲管理站的地方解決',
        'difficulty': '登玉山並不困難，但就是要克服在高山海拔的身體症狀、登山難度不高，適合親子一日遊',
        'info': '單攻建議2點左右出發，天候太糟可考慮擇日再來，但路線不難，坡度適中走起來舒適、最後陡上的200公尺風大較難走，抓好鐵鍊小心安全',
        'trail_info': '玉山主峰位於台灣的中心位置，海拔3952公尺，為台灣群山之首，百岳排名第一，也是東北亞的最高峰。主峰四周有東、南、西、北峰環繞，外圍還有前峰、小南山、南玉山、東小南山、鹿山與北北峰遙相呼應，宛如眾星拱月般，襯托出主峰的王者之尊，壯偉雄奇的山容、絕佳的展望和絢麗的日出景觀，吸引了無數的中外登山客前來攀登，近年來更成為台灣人一生必須完成的三件事之一。'
        },       
    'A04':{
        "weather_code": [1,2,1], 
        'weather': {'cloudy':'天冷時須注意保暖',
                    'rainy' :'雨後易濕滑行走要特別注意',
                    'sunny' :'綠樹成蔭, 太陽也曬不到, 輕鬆健走的好地方、夏天很涼爽'
                    },
        'equipment':'走平坦的道路很讚 不過地上會有點滑 建議穿更止滑的鞋子比較好、風大要記得帶個穩固美麗的帽子、穿雨鞋可輕鬆越過泥地',
        'parking':'過收費站後為單行道，路邊有停車格方便停車、停車需收費80、若想省小客車通行費$80，就停在收費站前兩旁路邊',
        'toilet':'中途有廁所，如走不動沿途皆有休息涼亭、洗手間很多',
        'difficulty': '長約1公里的輕鬆步道、即使是年長者也能輕鬆自在的到此一遊',
        'info': '步道規劃路線輕鬆又方便，可以穿越整個楓林區',
        'trail_info':'楓林步道是石門水庫最著名的賞楓景點之一，由高線收費站進入，循著人行步道前行，映入眼簾是整排高聳的楓香，有如一條繽紛的隧道，約行500公尺處即抵達楓林步道入口，步入小徑立刻被楓樹包圍，山坡上的楓樹都有30年以上的樹齡，每到深秋，紅、黃、綠層層色彩繽紛交織，蝴蝶翩翩飛舞，鳥兒枝頭吟唱，景色美麗如畫，令人讚嘆。沿途有解說平台、賞景平台，登上扶輪亭可俯瞰被紅葉染色的石門水庫，別有一番風情。鄰近的槭林公園步道，有整片的青楓林，可一併遊覽。'
        }, 
    'A05':{
        "weather_code": [1,1,1],
        'weather': {'cloudy':'雨天多蚊子得注意',
                    'rainy' :'老少咸宜，下雨也能前行',
                    'sunny' :'不太會曬到太陽、98%的樹蔭遮避率'
                    },
        'equipment':' 記得一定要穿一雙好穿的登山鞋或球鞋； 帶水跟毛巾，防蚊液、有蚊子咬很癢，是最大的缺點',
        'parking':'登山口就有停車場很方便',
        'toilet':'沿路休息點多，也有公共廁所',
        'difficulty': '虎山的登山步道應該屬於比較輕鬆的，不會一直有很抖的階梯、輕鬆好走、登山等級非常休閒',
        'info': '在四五月期間，晚上有螢火蟲可以觀賞，是相當不錯的生態教學行程~',
        'trail_info': '位於台北市信義區的虎山，與附近的象、豹、獅山並稱四獸山，因為形狀似踞蹲的虎躍狀而得此名。虎山是台北市民假日休閒的好去處，海拔雖只有140公尺，卻展望良好，經常在轉彎之處看到台北101，感覺101是一路陪伴上山的。步道中有多處平台為欣賞台北101及俯瞰台北盆地的好地點，分別為120高地涼亭、復興園、十方禪寺等，也是欣賞101跨年煙火的最佳熱門處，同時亦是攝影愛好者捕捉台北101風貌的搶手地點。除景色寬闊外，生態也十分豐富，由於虎山溪流經，培育了溪谷型生態環境，除多種蕨類外，也是孕育螢火蟲、蛙類及蜻蜓等豐富生態的最佳地點，兼具郊山健行與生態觀察的特色。'
        },     
    'A06':{
        "weather_code": [2,3,1], 
        'weather': {'cloudy':'若前一天下雨，不適合爬',
                    'rainy' :'雨後建議不要過來，砂岩地形仍會危險',
                    'sunny' :'岩石路段遮蔽較少，所以需要注意防曬'
                    },
        'equipment':'怕手刮傷或擦傷的話麻布手套蠻重要的、穿著抓地力及保護腳踝的登山（健行）鞋、注意防曬，戴個登山帽',
        'parking':'強烈建議步行前往，車子請都停在環山路上，入口處沒有停車位會造成阻塞。',
        'toilet':'上面無廁所必須野外求生，不過論劍亭後面有水龍頭可以洗手、只有在竹月寺有廁所',
        'difficulty': '對初學者有挑戰性的步道、距離適中走一圈大約5公里，連照相休息約2個小時，老少咸宜不危險不困難',
        'info': '假日人真的多到有點可怕、若有懼高症或體力不佳的人建議先做好心理準備再上山',
        'trail_info': '金面山為五指山系之西南稜，分金面山與小金面山，這座山地質中的安山砂岩含有石英，因此當太陽照射石遠望山頂閃閃發光，當地人便稱之為金面山。金面山位於內湖金龍產業道路西邊，因從碧山巖方向看過來，山頂巨石形貌有如鳥嘴般尖銳，因此又名剪刀石山，海拔雖僅258公尺卻獨具高山氣勢，山谷曾是清代時期臺北建城時，所用石材的大石之地，巨岩錯落起伏、崢嶸並立，登上半山腰，有一處清代採石場的石堡瞭望台，如今仍留有開採痕跡，置身山頂可以遠眺內湖大埤及台北街景，視野開闊、景致優美。'
        }, 
    'A07':{
        "weather_code": [2,3,1], 
        'weather': {'cloudy':'雨後濕滑 小心行走 需手腳並用',
                    'rainy' :'雨天過後最好別來',
                    'sunny' :'稜線會日曬'
                    },
        'equipment':'有攀繩路段、要記得戴手套',
        'parking':'西峰登山口附近可以停車，東峰登山口沿路也可以停車。假日熱門時段可能要停遠一點。',
        'toilet':'東峰登山口一旁可以先上廁所、碇坪公路→皇帝殿停車場有很多停車位及公廁',
        'difficulty': '刺激的岩稜線，適合愛挑戰的中級登山者、難度中低',
        'info': '午後容易雷陣雨、現已安全許多，岩稜旁已加裝護欄，雨後岩石未乾會濕滑，要小心行走、台北三大岩場之一',
        'trail_info': '位於新北市石碇區的「皇帝殿」海拔不高，但山勢非常陡峭，從很早以前就是台北近郊非常熱門的登山越嶺路線。自東峰到西峰之間約兩公里長的瘦稜幾乎都是由巨大的岩塊構成，早期沒有護繩，常見懼高者以匍匐之姿緩慢挪移前進。近年來部份危險路段加裝了鐵鍊繩索以確保安全，雖然少了一些驚險刺激，卻成為更容易親近的登山步道。 皇帝殿的東峰、西峰和天王峰，皆無三角點，峰頂視野極佳，能遙見大屯山系、淡水河、觀音山系和大台北地區，還能遠眺筆架山連稜的單面山景觀。主要有東峰（小粗坑）、西峰（湳窟）、北峰（大溪漧永定國小）這幾個登山口，沿途指標清楚，登山者可衡量自身的體力，選擇適合的路線攀登，下山後亦可順遊石碇老街、小走一段淡蘭古道或循106縣道至深坑老街逛逛。'
        },       
    'A08':{
        "weather_code": [1,2,1], 
        'weather': {'cloudy':'山上有風而且蠻冷的喔，非夏季上山記得保暖',
                    'rainy' :'下雨的關係步道有點滑',
                    'sunny' :'即使太陽很大，但仍不會有很曬的感覺，沿途幾乎有樹遮蔭，很舒服'
                    },
        'equipment':'防蚊液-穿長褲還被叮爆、左側步道夜間照明不足，要自備手電筒、記得多補充水份、最好帶登山杖比較好走路',
        'parking':'停車位不多，建議搭大眾運輸工具前往、可將車子停放在台北市聯合醫院松德院區旁的收費停車場，1小時$40、開車可停信義公園地下停車場、附近有許多機車停車位，很方便！',
        'toilet':'入口處還貼心提供免費廁所',
        'difficulty': '完全沒在動的耍廢之人走起來會很吃力、全程都是階梯,如果不適合走階梯的朋友 不要來嘗試',
        'info': '上面觀景台可以看101',
        'trail_info': '位於台北市信義區的象山，與附近的虎、豹、獅山並稱四獸山，因為外型似象頭而得此名。山頂雖僅有183公尺，但可清楚俯瞰台北盆地及台北地標101大樓，擁有極佳的視野，是許多攝影愛好者拍攝夜景與跨年煙火的最佳地點。象山與虎山地質相同，主要由砂岩組成，步道中可見黃褐色或赭紅色的岩壁與巨石，十分特殊；除此之外，生態多樣豐富、精采可期，因此為大台北地區享受戶外綠林的好去處。'
        }, 
}

uri = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON"

while True:
    try:
        uResponse = requests.get(uri)
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        dailySave=[]
        toDay=""
        break # quit the loop if successful
    except requests.ConnectionError:
        # error handling
        print("Connection Error")
        
#檢查是否有昨天資料
today = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))) #抓今天日期
todaystr = today.strftime('%Y-%m-%d')
deltaDay = datetime.timedelta(days=1)
dateAddOne=today+deltaDay
dateMinusOne=today-deltaDay
#print(dateWanted.strftime('%Y-%m-%d'))
#print(dateWanted)
dateAddOnestr=dateAddOne.strftime('%Y-%m-%d')
dateMinusOnestr=dateMinusOne.strftime('%Y-%m-%d')
#print(dateWantedstr)

fname = Path(dateMinusOnestr+'_result.json')
if fname.is_file():
    with open(fname) as json_file:
        yesterdayData = json.load(json_file)
        print('read file name',fname)
        #print(yesterdayData)
else:
    print(f'file {fname} not exist')

CWBapiNewDate= data["cwbopendata"]["dataset"]["locations"]["location"][0]["weatherElement"][0]["time"][0]["startTime"][:10]

with open('Wx_code.csv', mode='r', encoding='UTF-8-sig') as infile: #BOM編碼問題，修改為encoding='UTF-8-sig'似乎沒有用，乾脆再多加一列重複資料進csv檔案
    reader = csv.reader(infile)
    Wx_code_dict = {rows[0]:rows[1] for rows in reader}
    #print(Wx_code_dict)

for trail in trails:
    #results.append(trail)
    for trailWeather in data["cwbopendata"]["dataset"]["locations"]["location"]:
        #print(trailWeather)
        if trailWeather["locationName"]==trail["weatherRefName"]:
            
            trail['trailWeatherReference']=trailWeather["locationName"]
            trail_id=trail['id']
            #D1_trail_advice 1.安心上路、2.注意前往、3.不建議前往
            print('D1 weather',trailWeather["weatherElement"][12]["time"][0]["elementValue"][0]["value"])
            if '雨' in trailWeather["weatherElement"][12]["time"][0]["elementValue"][0]["value"]:
                D1_trail_weather_code=2
                D1_trail_advice=trail_guide[trail_id]['weather_code'][D1_trail_weather_code-1]
            elif '陰' in trailWeather["weatherElement"][12]["time"][0]["elementValue"][0]["value"]:
                D1_trail_weather_code=1
                D1_trail_advice=trail_guide[trail_id]['weather_code'][D1_trail_weather_code-1]
            elif '晴' in trailWeather["weatherElement"][12]["time"][0]["elementValue"][0]["value"]:
                D1_trail_weather_code=3
                D1_trail_advice=trail_guide[trail_id]['weather_code'][D1_trail_weather_code-1]
            elif '雲' in trailWeather["weatherElement"][12]["time"][0]["elementValue"][0]["value"]:
                D1_trail_weather_code=3
                D1_trail_advice=trail_guide[trail_id]['weather_code'][D1_trail_weather_code-1]
            
            print('D2 weather',trailWeather["weatherElement"][12]["time"][1]["elementValue"][0]["value"])
            if '雨' in trailWeather["weatherElement"][12]["time"][1]["elementValue"][0]["value"]:
                D2_trail_weather_code=2
                D2_trail_advice=trail_guide[trail_id]['weather_code'][D2_trail_weather_code-1]
            elif '陰' in trailWeather["weatherElement"][12]["time"][1]["elementValue"][0]["value"]:
                D2_trail_weather_code=1
                D2_trail_advice=trail_guide[trail_id]['weather_code'][D2_trail_weather_code-1]
            elif '晴' in trailWeather["weatherElement"][12]["time"][1]["elementValue"][0]["value"]:
                D2_trail_weather_code=3
                D2_trail_advice=trail_guide[trail_id]['weather_code'][D2_trail_weather_code-1]
            elif '雲' in trailWeather["weatherElement"][12]["time"][1]["elementValue"][0]["value"]:
                D2_trail_weather_code=3
                D2_trail_advice=trail_guide[trail_id]['weather_code'][D2_trail_weather_code-1]                
            
            print('D3 weather',trailWeather["weatherElement"][12]["time"][2]["elementValue"][0]["value"])
            if '雨' in trailWeather["weatherElement"][12]["time"][2]["elementValue"][0]["value"]:
                D3_trail_weather_code=2
                D3_trail_advice=trail_guide[trail_id]['weather_code'][D3_trail_weather_code-1]
            elif '陰' in trailWeather["weatherElement"][12]["time"][2]["elementValue"][0]["value"]:
                D3_trail_weather_code=1
                D3_trail_advice=trail_guide[trail_id]['weather_code'][D3_trail_weather_code-1]
            elif '晴' in trailWeather["weatherElement"][12]["time"][2]["elementValue"][0]["value"]:
                D3_trail_weather_code=3
                D3_trail_advice=trail_guide[trail_id]['weather_code'][D3_trail_weather_code-1]
            elif '雲' in trailWeather["weatherElement"][12]["time"][2]["elementValue"][0]["value"]:
                D3_trail_weather_code=3
                D3_trail_advice=trail_guide[trail_id]['weather_code'][D3_trail_weather_code-1]                
            print('D3_trail_advice', D3_trail_advice)
            
            WxpreD1=trailWeather["weatherElement"][12]["time"][0]["elementValue"][0]["value"]
            WxpreD2=trailWeather["weatherElement"][12]["time"][1]["elementValue"][0]["value"]
            WxpreD3=trailWeather["weatherElement"][12]["time"][2]["elementValue"][0]["value"]
            
            #print(trail_guide[trail_id]['equipment'])
            
            preD1={'MeanT': trailWeather["weatherElement"][0]["time"][0]["elementValue"]["value"], 
                'date': trailWeather["weatherElement"][0]["time"][0]["startTime"],
                'MaxT': trailWeather["weatherElement"][3]["time"][0]["elementValue"]["value"],
                'MinT': trailWeather["weatherElement"][4]["time"][0]["elementValue"]["value"],
                'PoP24': trailWeather["weatherElement"][9]["time"][0]["elementValue"]["value"],
                'Wx': trailWeather["weatherElement"][12]["time"][0]["elementValue"][0]["value"],
                'Wx_code': Wx_code_dict[WxpreD1],
                'equipment': trail_guide[trail_id]['equipment'],
                'parking': trail_guide[trail_id]['parking'],
                'toilet': trail_guide[trail_id]['toilet'],
                'difficulty': trail_guide[trail_id]['difficulty'],
                'info': trail_guide[trail_id]['info'],
                'trail_info': trail_guide[trail_id]['trail_info'],
                'advice': D1_trail_advice
                }
            #print('preD1= ',preD1)
            
            preD2={'MeanT': trailWeather["weatherElement"][0]["time"][1]["elementValue"]["value"], 
                'date': trailWeather["weatherElement"][0]["time"][1]["startTime"],
                'MaxT': trailWeather["weatherElement"][3]["time"][1]["elementValue"]["value"],
                'MinT': trailWeather["weatherElement"][4]["time"][1]["elementValue"]["value"],
                'PoP24': trailWeather["weatherElement"][9]["time"][1]["elementValue"]["value"],
                'Wx': trailWeather["weatherElement"][12]["time"][1]["elementValue"][0]["value"],
                'Wx_code': Wx_code_dict[WxpreD2],
                'equipment': trail_guide[trail_id]['equipment'],
                'parking': trail_guide[trail_id]['parking'],
                'toilet': trail_guide[trail_id]['toilet'],
                'difficulty': trail_guide[trail_id]['difficulty'],
                'info': trail_guide[trail_id]['info'],        
                'trail_info': trail_guide[trail_id]['trail_info'],        
                'advice': D2_trail_advice
                }
            preD3={'MeanT': trailWeather["weatherElement"][0]["time"][2]["elementValue"]["value"], 
                'date': trailWeather["weatherElement"][0]["time"][2]["startTime"],
                'MaxT': trailWeather["weatherElement"][3]["time"][2]["elementValue"]["value"], #最高溫度
                'MinT': trailWeather["weatherElement"][4]["time"][2]["elementValue"]["value"], #最低溫度
                'PoP24': trailWeather["weatherElement"][9]["time"][2]["elementValue"]["value"], #24小時降雨機率
                'Wx': trailWeather["weatherElement"][12]["time"][2]["elementValue"][0]["value"],
                'Wx_code': Wx_code_dict[WxpreD3],
                'equipment': trail_guide[trail_id]['equipment'],
                'parking': trail_guide[trail_id]['parking'],
                'toilet': trail_guide[trail_id]['toilet'],
                'difficulty': trail_guide[trail_id]['difficulty'],
                'info': trail_guide[trail_id]['info'],
                'trail_info': trail_guide[trail_id]['trail_info'],
                'advice': D3_trail_advice
                }
            trail['weatherConditoin']={'description': '氣象局：臺灣各育樂區未來1週逐24小時天氣預報'}

            for olddata in yesterdayData:
                if olddata['id']==trail_id:   #前一天資訊
                    WxoldD2=olddata["weatherConditoin"]['D2']['Wx']
                    WxoldD3=olddata["weatherConditoin"]['D3']['Wx']
                    
                    oldD2={
                            'MeanT': olddata["weatherConditoin"]['D2']['MeanT'], 
                            'date': olddata["weatherConditoin"]['D2']['date'],
                            'MaxT': olddata["weatherConditoin"]['D2']['MaxT'],
                            'MinT': olddata["weatherConditoin"]['D2']['MinT'],
                            'PoP24': olddata["weatherConditoin"]['D2']['PoP24'],
                            'Wx': olddata["weatherConditoin"]['D2']['Wx'],
                            'Wx_code': Wx_code_dict[WxoldD2],
                            'equipment': trail_guide[trail_id]['equipment'],
                            'parking': trail_guide[trail_id]['parking'],
                            'toilet': trail_guide[trail_id]['toilet'],
                            'difficulty': trail_guide[trail_id]['difficulty'],
                            'info': trail_guide[trail_id]['info'],
                            'trail_info': trail_guide[trail_id]['trail_info'],                                    
                            'advice': olddata["weatherConditoin"]['D2']['advice']
                            }
                    oldD3={
                            'MeanT': olddata["weatherConditoin"]['D3']['MeanT'], 
                            'date': olddata["weatherConditoin"]['D3']['date'],
                            'MaxT': olddata["weatherConditoin"]['D3']['MaxT'],
                            'MinT': olddata["weatherConditoin"]['D3']['MinT'],
                            'PoP24': olddata["weatherConditoin"]['D3']['PoP24'],
                            'Wx': olddata["weatherConditoin"]['D3']['Wx'],
                            'Wx_code': Wx_code_dict[WxoldD3],
                            'equipment': trail_guide[trail_id]['equipment'],
                            'parking': trail_guide[trail_id]['parking'],
                            'toilet': trail_guide[trail_id]['toilet'],
                            'difficulty': trail_guide[trail_id]['difficulty'],
                            'info': trail_guide[trail_id]['info'],
                            'trail_info': trail_guide[trail_id]['trail_info'],                                     
                            'advice': olddata["weatherConditoin"]['D3']['advice']
                            }
                    
                    if todaystr == preD1['date'][:10]: #當天1830前
                        trail["weatherConditoin"]['D1']=oldD2
                    else: #當天1830後
                        trail["weatherConditoin"]['D1']=oldD3 
                    trail['weatherConditoin']['D2']=preD1 
                    trail['weatherConditoin']['D3']=preD2 

            dailySave.append(trail)

# 依燈號，處裡路徑出發建議中的邏輯問題
for singleTrail in dailySave:
    #print(singleTrail)
    D1advice_code=singleTrail['weatherConditoin']['D1']['advice']
    D2advice_code=singleTrail['weatherConditoin']['D2']['advice']
    D3advice_code=singleTrail['weatherConditoin']['D3']['advice']

    # 還沒做對氣象的特別評論：陰天、晴天、雨天 !!
    weather_dict={2:'cloudy',3:'rainy',1:'sunny'}

    # 先給未修改前的初始建議
    D1advice_detail=trail_guide[singleTrail['id']]['weather'][weather_dict[D1advice_code]]
    D2advice_detail=trail_guide[singleTrail['id']]['weather'][weather_dict[D2advice_code]]
    D3advice_detail=trail_guide[singleTrail['id']]['weather'][weather_dict[D3advice_code]]
    
    # 2021.06.11 01:38 實作前一天下雨的邏輯，也設定了雨後危險路徑
    #
    #
    #這邊有問題！
    #
    #
    
    risk_trail = ['A02','A06','A07']

    if (D1advice_code == 3) and (singleTrail['id'] in risk_trail):
        singleTrail['weatherConditoin']['D2'].update({'advice': 2})
        D2advice_detail=trail_guide[singleTrail['id']]['weather'][weather_dict[D2advice_code]]
        D2advice_detail = "雨後隔天，岩石濕滑。" + D2advice_detail

    if (D2advice_code == 3) and (singleTrail['id'] in risk_trail):
        singleTrail['weatherConditoin']['D3'].update({'advice': 2})
        D3advice_detail=trail_guide[singleTrail['id']]['weather'][weather_dict[D3advice_code]]
        D3advice_detail = "雨後隔天，岩石濕滑。" + D3advice_detail
    
    # 修改後重新讀取每天的advice_code
    D1advice_code=singleTrail['weatherConditoin']['D1']['advice']
    D2advice_code=singleTrail['weatherConditoin']['D2']['advice']
    D3advice_code=singleTrail['weatherConditoin']['D3']['advice']
    
    # 放最終版本的advice_code進api
    singleTrail['weatherConditoin']['D1'].update({'advice_detail': D1advice_detail})
    singleTrail['weatherConditoin']['D2'].update({'advice_detail': D2advice_detail})
    singleTrail['weatherConditoin']['D3'].update({'advice_detail': D3advice_detail})

# 把每次處裡好的api資料存檔
if CWBapiNewDate == todaystr:
    with open(todaystr+'_result.json', 'w') as fp:
        json.dump(dailySave, fp)
elif CWBapiNewDate == dateAddOnestr:
    with open(dateAddOnestr+'_result.json', 'w') as fp:
        json.dump(dailySave, fp)


with open("mountain.txt") as json_file:
    data = json.load(json_file)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello Flask!</h1>"

@app.route('/mountain_trail/all', methods=['GET'])
def cities_all():
    return jsonify(data)

@app.route('/api/content', methods=['POST'])
def content_notebook():
    data = request.get_json()
    notebook_path = data['notebook_path']
    base = data['base']
    headers = data['headers']
    content = module.get_content_of_notebook(notebook_path, base, headers)
    return jsonify(content)

#@app.route('/user/<username>/<int:age>', methods=['GET'])
#def username(username,age):
#    return render_template('abc.html')
    #return f'i am {username} and is {age} years old'

@app.route('/mountain_trail', methods=['GET'])
def city_name():
    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No trailName provided. Please specify a trailName."
    results = []
    
    for trail in trails:
        if trail['trail_name']==location:
            results.append(trail)
            return jsonify(results)

@app.route('/mountain_trail/test', methods=['GET'])
def trail_weather():
    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No trailName provided. Please specify a trailName."
    results = []
    
    for trailSingle in trail_test:
        if trailSingle['trail_name']==location:
            results.append(trailSingle)
            return jsonify(results)

uri = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-035?Authorization=CWB-AF41CC67-3954-445C-B335-9268B25B08F9&downloadType=WEB&format=JSON"
try:
    uResponse = requests.get(uri)
except requests.ConnectionError:
    print("Connection Error")
Jresponse = uResponse.text
data3hr = json.loads(Jresponse)

each3hrData=[]
#dateFormatter='%Y-%m-%dT%h:%M:%s+'

with open('Wx_code.csv', mode='r') as infile:
    reader = csv.reader(infile)
    Wx_code_dict = {rows[0]:rows[1] for rows in reader}

for trail in trails:
    for trailWeather in data3hr["cwbopendata"]["dataset"]["locations"]["location"]:
        if trailWeather["locationName"]==trail["weatherRefName"]:
            Wx=[]
            Temp=[]
            dateList=[]
            rHum=[]
            wSpeed=[]
            aTemp=[]
            Wx_code=[]
            apiData={}

            trail['trailWeatherReference']=trailWeather["locationName"]
            trail_id=trail['id']
            
            Temp_description = trailWeather["weatherElement"][0]["description"]
            rHum_description = trailWeather["weatherElement"][2]["description"]
            wSpeed_descriton = trailWeather["weatherElement"][6]["description"]+' '+trailWeather["weatherElement"][6]["time"][0]['elementValue'][0]['measures']
            aTemp_descriton = trailWeather["weatherElement"][8]["description"]
            Wx_description = trailWeather["weatherElement"][9]["description"]
            
            #D1_trail_advice 1.安心上路、2.注意前往、3.不建議前往
            for i in range(0,24,1):
                
                current_date = trailWeather["weatherElement"][0]["time"][i]["dataTime"]
                current_Temp = trailWeather["weatherElement"][0]["time"][i]["elementValue"]["value"]
                current_rHum = trailWeather["weatherElement"][2]["time"][i]["elementValue"]["value"]
                current_wSpeed = trailWeather["weatherElement"][6]["time"][i]["elementValue"][0]["value"]
                current_aTemp = trailWeather["weatherElement"][8]["time"][i]["elementValue"]["value"]
                current_Wx = trailWeather["weatherElement"][9]["time"][i]["elementValue"][0]["value"]
                curent_Wx_code = Wx_code_dict[current_Wx]

                dateList.append(current_date)
                Temp.append(current_Temp)
                rHum.append(current_rHum)
                wSpeed.append(current_wSpeed)
                aTemp.append(current_aTemp)
                Wx.append(current_Wx)
                Wx_code.append(curent_Wx_code)
               
                #抓當下資料
                if (i!=0) & (i!=23):
                    #print(i)
                    pre_datetime = trailWeather["weatherElement"][0]["time"][i-1]["dataTime"]
                    pre_datetime= pd.to_datetime(pre_datetime)
                    current_date= pd.to_datetime(current_date)
                    if pre_datetime < today < current_date:
                        in_Temp = current_Temp
                        in_rHum = current_rHum
                        in_wSpeed = current_wSpeed
                        in_aTemp = current_aTemp 
                        in_Wx = current_Wx
                        in_Wx_code = curent_Wx_code
                        in_date = pre_datetime
                        continue  #找到存好current_in繼續
                elif i==0: #沒找到繼續
                    current_date= pd.to_datetime(current_date)
                    if current_date < today:
                        in_Temp = current_Temp
                        in_rHum = current_rHum
                        in_wSpeed = current_wSpeed
                        in_aTemp = current_aTemp 
                        in_Wx = current_Wx
                        in_Wx_code = curent_Wx_code                        
                        in_date=current_date
                        continue 
                elif i==23:
                    current_date= pd.to_datetime(current_date)
                    if current_date < today:
                        in_Temp = current_Temp
                        in_rHum = current_rHum
                        in_wSpeed = current_wSpeed
                        in_aTemp = current_aTemp 
                        in_Wx = current_Wx
                        in_Wx_code = curent_Wx_code
                        in_date=current_date
                        print('out of 75hrs bound, need renew the CWB 3hr JSON file')
                        continue 

            #print(dateList)
            apiData={
                'trail_name': trail['trail_name'],
                'date': dateList,
                'Temp': {
                    'Temp_description': Temp_description, 
                    'Temp':Temp
                    },
                'rHum': {
                    'rHum_description':rHum_description,
                    'rHum': rHum
                    },
                'wSpeed': {
                    'wSpeed_descriton': wSpeed_descriton,
                    'wSpeed': wSpeed
                    },
                'aTemp': {
                    'aTemp_descriton': aTemp_descriton,
                    'aTemp': aTemp
                    },
                'Wx': {
                    'Wx_description': Wx_description,
                    'Wx_code': Wx_code,
                    'Wx': Wx
                    }
                }
            current={'cuerrent': {
                    'date': in_date.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
                    'Temp':in_Temp ,
                    'rHum': in_rHum,
                    'wSpeed': in_wSpeed,
                    'aTemp': in_aTemp,
                    'Wx': in_Wx,
                    'Wx_code': in_Wx_code
                },}
            apiData.update(current)
            each3hrData.append(apiData)

preFix=dateList[0][:13]

with open(preFix+'_3hr_result.json', 'w') as fp:
        json.dump(each3hrData, fp)

@app.route('/mountain_trail/weather3hr', methods=['GET'])
def weather_3hr():
    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No trailName provided. Please specify a trailName."
    results = []
    
    for trail in each3hrData:
        if trail['trail_name']==location:
            results.append(trail)
            return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=16006)

#crontab usage: https://crontab.guru/every-3-hours
#triggered 2021-06-10 18:53:01
#triggered 2021-06-10 18:54:01
#triggered 2021-06-10 18:55:01
#triggered 2021-06-10 18:56:01
#triggered 2021-06-10 18:57:01
#triggered 2021-06-10 18:58:01
#triggered 2021-06-10 18:59:01
#triggered 2021-06-10 21:00:01
#triggered 2021-06-10 21:01:01
#triggered 2021-06-10 21:02:01
#triggered 2021-06-10 21:03:01
#triggered 2021-06-10 21:04:01
#triggered 2021-06-10 21:05:01
#triggered 2021-06-10 21:06:01
#triggered 2021-06-10 21:07:01
#triggered 2021-06-10 21:08:01
#triggered 2021-06-10 21:09:01
#triggered 2021-06-10 21:10:01
#triggered 2021-06-10 21:11:01
#triggered 2021-06-10 21:12:01
#triggered 2021-06-10 21:13:01
#triggered 2021-06-10 21:14:01
#triggered 2021-06-10 21:15:01
#triggered 2021-06-10 21:16:01
#triggered 2021-06-10 21:17:01
#triggered 2021-06-10 21:18:01
#triggered 2021-06-10 21:19:01
#triggered 2021-06-10 21:20:01
#triggered 2021-06-10 21:21:01
#triggered 2021-06-10 21:22:01
#triggered 2021-06-10 21:23:01
#triggered 2021-06-10 21:24:01
#triggered 2021-06-10 21:25:01
#triggered 2021-06-10 21:26:01
#triggered 2021-06-10 21:27:01
#triggered 2021-06-10 21:28:01
#triggered 2021-06-10 21:29:01
#triggered 2021-06-10 21:30:01
#triggered 2021-06-10 21:31:01
#triggered 2021-06-10 21:32:01
#triggered 2021-06-10 21:33:01
#triggered 2021-06-10 21:34:01
#triggered 2021-06-10 21:35:01
#triggered 2021-06-10 21:36:01
#triggered 2021-06-10 21:37:01
#triggered 2021-06-10 21:38:01
#triggered 2021-06-10 21:39:01
#triggered 2021-06-10 21:40:01
#triggered 2021-06-10 21:41:01
#triggered 2021-06-10 21:42:01
#triggered 2021-06-10 21:43:01
#triggered 2021-06-10 21:44:01
#triggered 2021-06-10 21:45:01
#triggered 2021-06-10 21:46:01
#triggered 2021-06-10 21:47:01
#triggered 2021-06-10 21:48:01
#triggered 2021-06-10 21:49:01
#triggered 2021-06-10 21:50:01
#triggered 2021-06-10 21:51:01
#triggered 2021-06-10 21:52:01
#triggered 2021-06-10 21:53:01
#triggered 2021-06-10 21:54:01
#triggered 2021-06-10 21:55:01
#triggered 2021-06-10 21:56:01
#triggered 2021-06-10 21:57:01
#triggered 2021-06-10 21:58:01
#triggered 2021-06-10 21:59:01
#triggered 2021-06-11 00:00:01
#triggered 2021-06-11 00:01:01
#triggered 2021-06-11 00:02:01
#triggered 2021-06-11 03:05:01
#triggered 2021-06-11 06:05:01
#triggered 2021-06-11 09:05:01
#triggered 2021-06-11 12:05:01
#triggered 2021-06-11 15:05:01
#triggered 2021-06-11 18:05:01
#triggered 2021-06-11 21:05:01
#triggered 2021-06-12 00:05:01
#triggered 2021-06-12 03:05:01
#triggered 2021-06-12 06:05:01
#triggered 2021-06-12 09:05:01
#triggered 2021-06-12 12:05:01
#triggered 2021-06-12 15:05:01
#triggered 2021-06-12 18:05:01
#triggered 2021-06-12 21:05:01
#triggered 2021-06-13 00:05:01
#triggered 2021-06-13 03:05:01
#triggered 2021-06-13 06:05:01
#triggered 2021-06-13 09:05:01
#triggered 2021-06-13 12:05:01
#triggered 2021-06-13 15:05:01
#triggered 2021-06-13 18:05:01
#triggered 2021-06-13 21:05:01
#triggered 2021-06-14 00:05:01
#triggered 2021-06-14 03:05:01
#triggered 2021-06-14 06:05:01
#triggered 2021-06-14 09:05:01
#triggered 2021-06-14 12:05:01
#triggered 2021-06-14 15:05:01
#triggered 2021-06-14 18:05:01
#triggered 2021-06-14 21:05:01
#triggered 2021-06-15 00:05:01
#triggered 2021-06-15 03:05:01
#triggered 2021-06-15 06:05:01
#triggered 2021-06-15 09:05:01
#triggered 2021-06-15 12:05:01
#triggered 2021-06-15 15:05:01
#triggered 2021-06-15 18:05:01
#triggered 2021-06-15 21:05:01
#triggered 2021-06-16 00:05:01
#triggered 2021-06-16 03:05:01
#triggered 2021-06-16 06:05:01
#triggered 2021-06-16 09:05:01
#triggered 2021-06-16 12:05:01
#triggered 2021-06-16 15:05:01
#triggered 2021-06-16 18:05:01
#triggered 2021-06-16 21:05:01
#triggered 2021-06-17 00:05:01
#triggered 2021-06-17 03:05:01
#triggered 2021-06-17 06:05:01
#triggered 2021-06-17 09:05:01
#triggered 2021-06-17 12:05:01
#triggered 2021-06-17 15:05:01
#triggered 2021-06-17 18:05:01
#triggered 2021-06-17 21:05:01
#triggered 2021-06-18 00:05:01
#triggered 2021-06-18 03:05:01
#triggered 2021-06-18 06:05:01
#triggered 2021-06-18 09:05:01
#triggered 2021-06-18 12:05:01
#triggered 2021-06-18 15:05:01
#triggered 2021-06-18 18:05:01
#triggered 2021-06-18 21:05:01
#triggered 2021-06-19 00:05:01
#triggered 2021-06-19 03:05:01
#triggered 2021-06-19 06:05:01
#triggered 2021-06-19 09:05:01
#triggered 2021-06-19 12:05:01
#triggered 2021-06-19 15:05:01
#triggered 2021-06-19 18:05:01
#triggered 2021-06-19 21:05:01
#triggered 2021-06-20 00:05:01
#triggered 2021-06-20 03:05:01
#triggered 2021-06-20 06:05:01
#triggered 2021-06-20 09:05:01
#triggered 2021-06-20 12:05:01
#triggered 2021-06-20 15:05:01
#triggered 2021-06-20 18:05:01
#triggered 2021-06-20 21:05:01
#triggered 2021-06-21 00:05:01
#triggered 2021-06-21 03:05:01
#triggered 2021-06-21 06:05:01
#triggered 2021-06-21 09:05:01
#triggered 2021-06-21 12:05:01
#triggered 2021-06-21 15:05:01
#triggered 2021-06-21 18:05:01
#triggered 2021-06-21 21:05:01
#triggered 2021-06-22 00:05:01
#triggered 2021-06-22 03:05:01
#triggered 2021-06-22 06:05:01
#triggered 2021-06-22 09:05:01
#triggered 2021-06-22 12:05:01
#triggered 2021-06-22 15:05:01
#triggered 2021-06-22 18:05:01
#triggered 2021-06-22 21:05:01
#triggered 2021-06-23 00:05:01
#triggered 2021-06-23 03:05:01
#triggered 2021-06-23 06:05:01
#triggered 2021-06-23 09:05:01
#triggered 2021-06-23 12:05:01
#triggered 2021-06-23 15:05:01
#triggered 2021-06-23 18:05:01
#triggered 2021-06-23 21:05:01
#triggered 2021-06-24 00:05:01
#triggered 2021-06-24 03:05:01
#triggered 2021-06-24 06:05:01
#triggered 2021-06-24 09:05:01
#triggered 2021-06-24 12:05:01
#triggered 2021-06-24 15:05:02
#triggered 2021-06-24 18:05:01
#triggered 2021-06-24 21:05:01
#triggered 2021-06-25 00:05:01
#triggered 2021-06-25 03:05:01
#triggered 2021-06-25 06:05:01
#triggered 2021-06-25 09:05:01
#triggered 2021-06-25 12:05:01
#triggered 2021-06-25 15:05:01
#triggered 2021-06-25 18:05:01
#triggered 2021-06-25 21:05:01
#triggered 2021-06-26 00:05:01
#triggered 2021-06-26 03:05:01
#triggered 2021-06-26 06:05:01
#triggered 2021-06-26 09:05:01
#triggered 2021-06-26 12:05:01
#triggered 2021-06-26 15:05:01
#triggered 2021-06-26 18:05:01
#triggered 2021-06-26 21:05:01
#triggered 2021-06-27 00:05:01
#triggered 2021-06-27 03:05:01
#triggered 2021-06-27 06:05:01
#triggered 2021-06-27 09:05:01
#triggered 2021-06-27 12:05:01
#triggered 2021-06-27 15:05:01
#triggered 2021-06-27 18:05:01
#triggered 2021-06-27 21:05:01
#triggered 2021-06-28 00:05:01
#triggered 2021-06-28 03:05:01
#triggered 2021-06-28 06:05:01
#triggered 2021-06-28 09:05:01
#triggered 2021-06-28 12:05:01
#triggered 2021-06-28 15:05:01
#triggered 2021-06-28 18:05:01
#triggered 2021-06-28 21:05:01
#triggered 2021-06-29 00:05:01
#triggered 2021-06-29 03:05:01
#triggered 2021-06-29 06:05:01
#triggered 2021-06-29 09:05:01
#triggered 2021-06-29 12:05:01
#triggered 2021-06-29 15:05:01
#triggered 2021-06-29 18:05:01
#triggered 2021-06-29 21:05:01
#triggered 2021-06-30 00:05:01
#triggered 2021-06-30 03:05:01
#triggered 2021-06-30 06:05:01
#triggered 2021-06-30 09:05:01
#triggered 2021-06-30 12:05:01
#triggered 2021-06-30 15:05:01
#triggered 2021-06-30 18:05:01
#triggered 2021-06-30 21:05:01
#triggered 2021-07-01 00:05:01
#triggered 2021-07-01 03:05:01
#triggered 2021-07-01 06:05:01
#triggered 2021-07-01 09:05:01
#triggered 2021-07-01 12:05:01
#triggered 2021-07-01 15:05:01
#triggered 2021-07-01 18:05:01
#triggered 2021-07-01 21:05:01
#triggered 2021-07-02 00:05:01
#triggered 2021-07-02 03:05:01
#triggered 2021-07-02 06:05:01
#triggered 2021-07-02 09:05:01
#triggered 2021-07-02 12:05:01
#triggered 2021-07-02 15:05:01
#triggered 2021-07-02 18:05:01
#triggered 2021-07-02 21:05:01
#triggered 2021-07-03 00:05:01
#triggered 2021-07-03 03:05:01
#triggered 2021-07-03 06:05:01
#triggered 2021-07-03 09:05:01
#triggered 2021-07-03 12:05:01
#triggered 2021-07-03 15:05:01
#triggered 2021-07-03 18:05:01
#triggered 2021-07-03 21:05:01
#triggered 2021-07-04 00:05:01
#triggered 2021-07-04 03:05:01
#triggered 2021-07-04 06:05:01
#triggered 2021-07-04 09:05:01
#triggered 2021-07-04 12:05:01
#triggered 2021-07-04 15:05:01
#triggered 2021-07-04 18:05:01
#triggered 2021-07-04 21:05:01
#triggered 2021-07-05 00:05:01
#triggered 2021-07-05 03:05:01
#triggered 2021-07-05 06:05:01
#triggered 2021-07-05 09:05:01
#triggered 2021-07-05 12:05:01
#triggered 2021-07-05 15:05:01
#triggered 2021-07-05 18:05:01
#triggered 2021-07-05 21:05:01
#triggered 2021-07-06 00:05:01
#triggered 2021-07-06 03:05:01
#triggered 2021-07-06 06:05:01
#triggered 2021-07-06 09:05:01
#triggered 2021-07-06 12:05:01
#triggered 2021-07-06 15:05:01
#triggered 2021-07-06 18:05:01
#triggered 2021-07-06 21:05:01
#triggered 2021-07-07 00:05:01
#triggered 2021-07-07 03:05:02
#triggered 2021-07-07 06:05:01
#triggered 2021-07-07 09:05:01
#triggered 2021-07-07 12:05:02
#triggered 2021-07-07 15:05:01
#triggered 2021-07-07 18:05:01
#triggered 2021-07-07 21:05:01
#triggered 2021-07-08 00:05:01
#triggered 2021-07-08 03:05:01
#triggered 2021-07-08 06:05:01
#triggered 2021-07-08 09:05:01
#triggered 2021-07-08 12:05:01
#triggered 2021-07-08 15:05:01
#triggered 2021-07-08 18:05:01
#triggered 2021-07-08 21:05:01
#triggered 2021-07-09 00:05:01
#triggered 2021-07-09 03:05:01
#triggered 2021-07-09 06:05:01
#triggered 2021-07-09 09:05:01
#triggered 2021-07-09 12:05:01
#triggered 2021-07-09 15:05:01
#triggered 2021-07-09 18:05:02
#triggered 2021-07-09 21:05:01
#triggered 2021-07-10 00:05:01
#triggered 2021-07-10 03:05:01
#triggered 2021-07-10 06:05:01
#triggered 2021-07-10 09:05:01
#triggered 2021-07-10 12:05:01
#triggered 2021-07-10 15:05:01
#triggered 2021-07-10 18:05:01
#triggered 2021-07-10 21:05:01
#triggered 2021-07-11 00:05:02
#triggered 2021-07-11 03:05:01
#triggered 2021-07-11 06:05:01
#triggered 2021-07-11 09:05:01
#triggered 2021-07-11 12:05:01
#triggered 2021-07-11 15:05:01
#triggered 2021-07-11 18:05:01
#triggered 2021-07-11 21:05:01
#triggered 2021-07-12 00:05:01
#triggered 2021-07-12 03:05:01
#triggered 2021-07-12 06:05:01
#triggered 2021-07-12 09:05:02
#triggered 2021-07-12 12:05:01
#triggered 2021-07-12 15:05:01
#triggered 2021-07-12 18:05:01
#triggered 2021-07-12 21:05:01
#triggered 2021-07-13 00:05:01
#triggered 2021-07-13 03:05:01
#triggered 2021-07-13 06:05:01
#triggered 2021-07-13 09:05:01
#triggered 2021-07-13 12:05:01
