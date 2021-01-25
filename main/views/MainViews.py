from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import permissions

from google_play_scraper import app, Sort, reviews
from google_play_store import search
from datetime import timedelta, datetime

from app_store_scraper import AppStore

from time import sleep
import urllib.request
from bs4 import BeautifulSoup
from google_play_store import search
from app_store_scraper import AppStore
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class Reviews(APIView):
    """Reviews (TODO)"""

    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        app_id = request.query_params.get('app_id', None)
        to_date_str = request.query_params.get('to_date', None)
        if app_id is None or to_date_str is None:
            return Response(status=400)

        to_date = datetime.fromisoformat(to_date_str)
        reviews = self.reviews_by_date(app_id, to_date)
        result = {
            'reviews': reviews
        }

        return Response(result, status=200)

    @staticmethod
    def reviews_by_date(app_id, to_date=None, **kwargs):
        kwargs.pop("count", None)
        kwargs.pop("continuation_token", None)

        _count = 199
        _continuation_token = None
        result = []

        while True:
            result_, _continuation_token = reviews(
                app_id, lang="ru", count=_count, continuation_token=_continuation_token, sort=Sort.NEWEST, **kwargs
            )

            result += result_

            if _continuation_token.token is None:
                break

            # if sleep_milliseconds:
            #     sleep(sleep_milliseconds / 1000)

            last_data = result_[-1]['at']
            if to_date is not None and to_date > last_data:
                break

        return result


class SearchApps(APIView):
    """
    Поиск по Google Play
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        query = request.query_params.get('query', None)
        if query is None:
            return Response(status=400)

        results = search(query, page=1, hl="ru")
        return Response({'result': results}, status=200)


class FindAppInAppStore(APIView):
    """Поиск аналогичного приложения в AppStore"""

    permission_classes = [permissions.AllowAny]


    def get(self, request: Request):
        app_name = request.query_params.get('app_name', None)
        app_info = self.find_app_in_app_store(app_name)
        data = {
            'contains_in_app_store': app_info is not None,
            'app_info': app_info
        }

        return Response(data, status=200)

    @staticmethod
    def find_app_in_app_store(full_app_name: str, accuracy=90):
        app_name_for_query = FindAppInAppStore._get_first_word(full_app_name)
        names = [i.getText() for i in FindAppInAppStore._search(app_name_for_query)]

        app_store_name, current_accuracy = process.extractOne(full_app_name, names)
        result = None
        if current_accuracy <= accuracy:
            result = AppStore(country="ru", app_name=app_store_name)
        return result

    @staticmethod
    def _get_first_word(app_name):
        i = 0
        while app_name[i].isalpha():
            i += 1

        return app_name[:i]

    @staticmethod
    def _search(query: str) -> list:
        contents = urllib.request.urlopen("https://www.apple.com/ru/search/{}?src=serp".format(query)).read()
        soup = BeautifulSoup(contents, 'lxml')
        tag_names = soup.find_all("h2", {"class": "as-productname"})
        return tag_names

