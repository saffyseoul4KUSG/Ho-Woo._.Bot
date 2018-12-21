# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request
import ssl

import multiprocessing as mp
from threading import Thread

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = 'your token'
slack_client_id = "your client id"
slack_client_secret = "your client secret"
slack_verification = "your sverification"
sc = SlackClient(slack_token)

# threading function
def processing_event(queue):
  while True:
      # 큐가 비어있지 않은 경우 로직 실행
      if not queue.empty():
          slack_event = queue.get()

          # Your Processing Code Block gose to here
          channel = slack_event["event"]["channel"]
          text = slack_event["event"]["text"]

          # 챗봇 크롤링 프로세스 로직 함수
          keywords = _crawl_naver_keywords(text)

          # 아래에 슬랙 클라이언트 api를 호출하세요
          sc.api_call(
              "chat.postMessage",
              channel=channel,
              text=keywords
          )

# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    # 여기에 함수를 구현해봅시다.

    text = text[13:].lower()
    ranks = []
    points = []
    keywords = []
    text_split = text.split()

    if text == "epl" or text == 'eng' or '영국' in text or '프리미어' in text:

        url = "https://www.premierleague.com/"

        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        #print("h")
        for rank in soup.find_all('tbody', class_="standingEntriesContainer"):

            for idx, team in enumerate(rank.find_all('td', class_='team')):
                # print('rank :' + str(team.get_text()))
                ranks.append(str(idx + 1) + "위 " + str(team.get_text()))
            for point in rank.find_all('td', class_='points'):
                points.append(" / 승점 :" + str(point.get_text()))

        for i in range(20):
            keywords.append(ranks[i] + points[i])
        return u'\n'.join(keywords)

    elif text == "bundesliga" or text == "ger" or '독일' in text or '분데' in text:

        url = "https://www.bundesliga.com/en/bundesliga/table/"

        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

        for rank in soup.find_all('table', class_="table"):

            for idx, team in enumerate(rank.find_all('td', class_='team')):
                # print(team)
                #print('rank :' + str(team.find('span', class_='d-none d-lg-inline').get_text()))
                ranks.append(str(idx + 1) + "위 " + str(team.find('span', class_='d-none d-lg-inline').get_text()))
            for point in rank.find_all('td', class_='pts'):
                points.append(" / 승점 :" + str(point.get_text()))

        for i in range(18):
            keywords.append(ranks[i] + points[i])
        return u'\n'.join(keywords)

    elif text == "k-league" or text == "kor" or '한국' in text or '케이리그' in text:
        url = "http://www.kleague.com/rank"

        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        test = []
        point_k = []
        for rank in soup.find_all('div', class_="data-body"):
            for idx, team in enumerate(rank.find_all('span', class_='club')):
                ranks.append(str(idx + 1) + "위 " + str(team.get_text()))
            for point in rank.find_all('td'):
                # points.append(" / 승점 :"+str(point.get_text()))
                test.append(point.get_text().split('\n'))
            for i in range(len(test)):
                if i % 10 == 3:
                    point_k.append(" / 승점 :" + str(test[i]).replace("'", '').replace("[", '').replace("]", ''))

        for i in range(12):
            keywords.append(ranks[i] + point_k[i])
        return u'\n'.join(keywords)


    elif text == "serie a" or text == "ita" or '이탈리아' in text or '세리에' in text:

        url = "http://www.legaseriea.it/it/serie-a/classifica"
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

        for rank in soup.find_all('section', class_="competizione-classifica"):

            for idx, team in enumerate(rank.find_all('img')):
                test = str(team).split()[3]
                ranks.append(str(idx + 1) + "위 " + str(test[6:].replace('"', '')))

            for point in rank.find_all('td', class_='blue'):
                points.append(" / 승점 :" + str(point.get_text()))

        for i in range(20):
            keywords.append(ranks[i] + points[i])

        return u'\n'.join(keywords)

    #input twice error ㅡㅡ -----

    elif text == "league 1" or text == "fra" or '프랑스' in text or '리그앙' in text:

        url = "https://www.ligue1.com/"
        context = ssl._create_unverified_context()
        soup = BeautifulSoup(urllib.request.urlopen(url, context=context).read(), "html.parser")

        for rank in soup.find_all('div', id="list_classement_D1"):

            for idx, team in enumerate(rank.find_all('td', class_='club')):
                # print('rank :' + str(team.get_text()))
                ranks.append(str(idx + 1) + "위 " + str(team.get_text().replace('\n', '')[20:-44]))
            for idx_2, point in enumerate(rank.find_all('td', class_='points')):
                if idx_2 % 2 == 1:
                    points.append(" / 승점 :" + str(point.get_text()))

            for i in range(20):
                keywords.append(ranks[i] + points[i])

        return u'\n'.join(keywords)

    elif text == "la liga" or text == "esp" or '스페인' in text or '프리메라' in text or '라리가' in text:

        url = "https://www.laliga.es/en/laliga-santander"
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

        for rank in soup.find_all('section', id="clasificacion"):

            for idx, team in enumerate(rank.find_all('span', class_='nombre-equipo-clasificacion')):
                ranks.append(str(idx + 1) + "위 " + str(team.get_text()))

            for point in rank.find_all('td', class_='contenedor-numero dato-clasificacion totales puntos'):
                points.append(" / 승점 :" + str(point.get_text()))

        for i in range(20):
            keywords.append(ranks[i] + points[i])

        return u'\n'.join(keywords)
    #-----
    elif text == "j-league" or text == "jpn" or '일본' in text or '제이리그' in text:
        url = "https://www.jleague.jp/en/standings/j1"

        context = ssl._create_unverified_context()
        sourcecode = urllib.request.urlopen(url, context=context).read()
        soup = BeautifulSoup(sourcecode, "html.parser")

        ranks = []
        points = []
        keywords = []

        # 팀 리스트 따와서, 팀명이랑 점수 입력하는거
        for rank in soup.find_all('section', class_="sec sec_standingsList"):

            for idx, team in enumerate(rank.find_all('td')):
                if idx % 11 == 2:
                    ranks.append(str((idx // 11) + 1) + "위 " + str(team.get_text()))
                elif idx % 11 == 3:
                    points.append(" / 승점 : " + str(team.get_text()).strip('\n'))

        for i in range(18):
            keywords.append(ranks[i] + points[i])

        # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
        return u'\n'.join(keywords)

    elif "명령어" in text_split or "command" in text_split:
        string = ['리그 별 축구 순위를 알고 싶다면??\n 나라이름(영어시 약어), 리그 이름을 검색해 주세요. (한영 상관 없음)', '"예정!" 입력시 추후 추가할 내용', '\n\n', 'EPL(eng), La Liga(esp), Bundesliga (ger), Serie A(ita), League 1(fra), K-League(kor), J-League(jpn)']
        return u"\n".join(string)

    elif "예정!" in text_split or "예정" in text_split or "업데이트" in text_split:
        string = ['\n', '추가 업데이트 할 내용', '1. 크롤링한 데이터 DB화 - mysql 사용예정, pymysql 라이브러리 사용', '2. 팀명 한글화', '3. 각 리그별 승 / 무 / 패 / 골득실 추가', '4. 리그 팀별 최근 5경기 성적', '5. 리그별 선수 랭킹', '6. 팀명 검색 시 리그이름과 리그 순위', '7. 성적! 입력 후 두 팀 이름 입력하면 상대전적', '8. 선수이름 검색시 리그 스텟 및 사진 추가', '9. 규칙! 입력하면 순위 계산 규칙 설명', '10. 그 외 리그, 2부 3부 등 하위리그 추가', '\n']
        return u"\n".join(string)

    elif "축구봇" in text or "축구봇!" in text:
        return "안녕? 나 불렀어?"

    elif "메시" in text or "messi" in text:
        return "메시는 호날두보다 축구를 못해"

    elif "호날두" in text:
        return "호날두는 축구선수 중에서 세계 최고의 슈퍼스타야"
    else:
        string = ['??? 뭐라고 하는지 모르겠어, 명령어 또는 command 를 입력해줘']
        return u"\n" .join(string)



# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    # print(slack_event["event"])
    #print(slack_event["event"["text"]])
    if event_type == "app_mention":
        """
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]
        print(text)
        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )
        return make_response("App mention message has been sent", 200, )
        """
        event_queue.put(slack_event)
        return make_response("App mention message has been sent", 200, )
    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)
    print(slack_event)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    event_queue = mp.Queue()

    p = Thread(target=processing_event, args=(event_queue,))
    p.start()

    app.run('127.0.0.1', port=7602)
    p.join()