# 문화재청 위치 정보
# JunHyeon.Kim
"""
Response
01. ccmaName     : 문화재유형
02. crltsnoNm    : 지정호수
03. ccbaMnm1     : 문화재명
04. ccbaMnm2     : 문화재명
05. ccbaCtcdNm
06. ccsiName
07. ccbaAdmin
08. ccbaKdcd
09. ccbaCtcd
10. ccbaAsno
11. ccbaCncl
12. ccbaCpno
"""
# ------------------------------------
import requests as req
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
import json
import os
import sys
# ------------------------------------
class INFO:
    def __init__(self):
        '''
        "18": "국가민속문화재", "31": "문화재자료", "80": "이북5도 무형문화재", "17": "국가무형문화재",
        "24": "시도민속문화재", "22": "시도무형문화재", "21": "시도유형문화재", "23": "시도기념물",
        "16": "천연기념물",
        '''
        self.ccbaKdcd = { # 종목 코드
            "11": "국보",         "12": "보물",
            "13": "사적",         "14": "사적및명승",
            "15": "명승",         "16": "천연기념물",
            "79": "등록문화재",
        }
        self.ccbaCtcd = { # 시도 코드
            '11': "서울" ,'21': "부산",
            '22': "대구" ,'23': "인천",
            '24': "광주" ,'25': "대전",
            '26': "울산" ,'45': "세종",
            '31': "경기" ,'32': "강원",
            '33': "충북" ,'34': "충남",
            '35': "전북" ,'36': "전남",
            '37': "경북" ,'38': "경남",
            '50': "제주" }

class CH_Location_Search:
    def __init__(self):
        self.url = "http://www.gis-heritage.go.kr/openapi/xmlService/spca.do"
        self.params = {"ccbaMnm1":None}

    def urlRequests(self):
        t_param = urlencode(self.params)
        t_url = self.url + "?" + t_param
        t_html = req.get(t_url)
        if t_html.status_code == 200:
            try:
                with open(file="../CONF_CURTURE/ch_{}_localtion.xml".format(self.params["ccbaMnm1"]), mode='w', encoding='utf-8') as f:
                    f.write(t_html.text)
            except:
                if OSError.errno == 22:
                    if "<" in str(self.params["ccbaMnm1"]):
                        self.params["ccbaMnm1"] = str(self.params["ccbaMnm1"]).replace(old="<", new=" ")
                    elif ">" in str(self.params["ccbaMnm1"]):
                        self.params["ccbaMnm1"] = str(self.params["ccbaMnm1"]).replace(old=">", new=" ")
                    elif "," in str(self.params["ccbaMnm1"]):
                        self.params["ccbaMnm1"] = str(self.params["ccbaMnm1"]).replace(old=",", new=" ")
                try:
                    with open(file="../CONF_CURTURE/ch_{}_localtion.xml".format(self.params["ccbaMnm1"]), mode='w',
                              encoding='utf-8') as f:
                        f.write(t_html.text)
                except:
                    sys.exit(1)
                else:
                    f.close()
            else:
                f.close()
class CH:
    node = INFO()                          # 포함관계의 객체
    chlocation_node = CH_Location_Search() # 포함관계의 객체
    # ====================================================
    url = "http://www.cha.go.kr/cha/SearchKindOpenapiList.do"
    params = {"ccbaCtcd":None, "ccbaKdcd":None}  # 시도 코드 :=> 11(서울)
    response_data = None

    @classmethod
    def urlRequests(cls):
        # params encoding
        for k1, v1 in cls.node.ccbaCtcd.items(): # ___ <시도 코드 셋팅>
            cls.params["ccbaCtcd"] = k1
            for k2, v2 in cls.node.ccbaKdcd.items(): # ___ <종목 코드 셋팅>
                cls.params["ccbaKdcd"] = k2
                local_params = urlencode(cls.params)
                local_url    = cls.url + "?" + local_params
                html = req.get(local_url)
                if html.status_code == 200:
                    # print (html.text)
                    with open(file="../CONF/ch_{0}_{1}.xml".format(v1, v2), mode='w', encoding='utf-8') as f:
                        f.write(html.text)
                        f.close()
            print ("{0} {1} 작업 끝".format(v1,v2))

    @classmethod
    def xmlParsingToJson(cls):
        # 디렉토리 이동
        os.chdir("../CONF")
        for f in os.listdir():
            fname, fext = os.path.splitext(f)
            if fext == ".xml":
                tree = ET.parse(f)
                root = tree.getroot()
                for elem in root:
                    for subelem in elem:
                        # if subelem.tag == "ccmaName":   # 문화재 유형
                        #     print (subelem.tag + ":" + subelem.text)
                        if subelem.tag == "ccbaMnm1": # 문화재 명
                            print(subelem.tag + ":" + subelem.text)
                            print ("================================")
                            # parameter 설정
                            cls.chlocation_node.params['ccbaMnm1'] = subelem.text
                            # url requests
                            cls.chlocation_node.urlRequests()
        '''
        json 파일 구조 
        "지역명": "경기" 
        '''
CH.urlRequests()
CH.xmlParsingToJson()
