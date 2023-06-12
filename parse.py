#### 네이버 API를 사용하여 뉴스 수집

import xml.etree.ElementTree as ET
import datetime
import re
import requests


class NAVER():
    def __init__(self):
        self.url = 'https://openapi.naver.com/v1/search/news.xml'
        self.client_id = '' ###시크릿아이디 입력
        self.client_secret = '' ###시크릿키 입력
        self.headers = {
            'Host': 'openapi.naver.com',
            'User-Agent': 'curl/7.49.1',
            'Accept': '*/*',
            'X-Naver-Client-Id': self.client_id,
            'X-Naver-Client-Secret': self.client_secret
        }
        self.g   = None
        self.Log = None
        self.API = None

    def create_params(self, keyword ):
        params = {
            'query': keyword,
            'display': 10,
            'start': 1,
            'sort': 'date'
        }
        return params

    def insert(self, insert_data ):
        import mysql.connector
        # MySQL 서버에 연결
        cnx = mysql.connector.connect(
            user='jiwoo',
            password='1234',
            host='localhost',
            database='ex'
        )

        # 데이터베이스 커서 생성
        cursor = cnx.cursor()

        # INSERT 쿼리 작성
        query = "INSERT INTO news (title, link , date_ymd, keyword) VALUES (%s, %s, %s, %s)"

        # INSERT할 데이터
        data = insert_data

        try:
            # 쿼리 실행
            cursor.execute(query, data)

            # 변경사항을 커밋
            cnx.commit()

            print("데이터가 성공적으로 삽입되었습니다.")

        except mysql.connector.Error as err:
            print(f"데이터 삽입 중 오류가 발생하였습니다: {err}")

        # 연결 및 커서 종료
        cursor.close()
        cnx.close()

    def parse(self, keyword):

        params = self.create_params ( keyword ) ## 요청 파라미터를 만듬
        response = requests.get(self.url, params=params, headers=self.headers)
        status = response.status_code
        if response.status_code in range(200, 210):
            response.raise_for_status()  # 오류 발생 시 예외 발생
            xml_data = response.content  # 응답 결과 데이터 (XML 형식)

            root = ET.fromstring(xml_data).find("channel")  # XML 데이터 파싱


            for item in root.findall('item'):
                print('item: {}'.format(item))     # item 태그를 찾아서 반복문 수행
                insert_data = []
                title = item.find("title").text
                title = re.sub('<b>', '', title)  # "<b>" 제거
                title = re.sub('</b>', '', title)  # "<b>" 제거
                title = re.sub('&apos;', '', title)  # "&apos;" 제거
                link = item.find("link").text  # 링크
                date_ymd = item.find("pubDate").text # 날짜
                date_object = datetime.datetime.strptime(date_ymd, "%a, %d %b %Y %H:%M:%S %z")
                formatted_date = date_object.strftime("%Y-%m-%d")
                insert_data.append( title )
                insert_data.append( link )
                insert_data.append( formatted_date )
                insert_data.append ( keyword )
                print('insert_data: {}'.format(insert_data))

                self.insert( insert_data )