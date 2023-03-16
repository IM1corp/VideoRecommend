import os

import requests


class Sender:
    secret = os.environ['YUMMY_SECRET']
    host = os.environ['YUMMY_API_URL']
    def __init__(self):
        self.session = requests.session()

    def get_data(self) -> 'list[dict]':
        ratings = self.session.get(f'{self.host}/get-user-all-ratings.php', params={'secret': self.secret}).json()
        self._check_error(ratings)
        ratings = ratings['ratings']
        return ratings
    def send_animes(self, answer: 'dict[int, list[int]]'):
        ans = self.session.post(f'{self.host}/set-recommends.php', params={'secret': self.secret}, json=answer).json()
        self._check_error(ans)
        return True
    def send_users(self, user_recommends: 'dict[list[int]]'):
        ans = self.session.post(f'{self.host}/set-recommends-users.php', params={'secret': self.secret}, json=user_recommends).json()
        self._check_error(ans)

    @staticmethod
    def _check_error(ans: dict):
        if ans.get('error'): raise ServerError(ans.get('error'))
        return False



class ServerError(Exception):
    pass

