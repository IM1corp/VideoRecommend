from dotenv import load_dotenv; load_dotenv()
import os
import pathlib
import sys
import traceback
from time import strftime, gmtime
import implicit
from implicit.gpu.als import AlternatingLeastSquares
from scipy.sparse import csr_matrix

from data_getter import Sender

sender = Sender()

def pprint(*data, ignore_time=False):
    with open(pathlib.Path(__file__).parent/'log.txt', 'a', encoding='utf-8') as file:
        if not ignore_time:
            file.write(f'[{strftime("%Y-%m-%d %H:%M:%S", gmtime())}] ')
        file.write(''.join(map(str, data)))
        file.write('\n')
    print(*data)
def build_matrix(ratings: 'list[dict]'):
    n_rows = int(max((i['user_id'] for i in ratings), key=int)) + 1
    n_cols = int(max(ratings, key=lambda i: int(i['anime_id']))['anime_id']) + 1
    data = []
    row_indices = []
    col_indices = []

    for i in ratings:
        user_id = int(i['user_id'])
        item_id = int(i['anime_id'])
        rating = int(i['rating'])
        data.append(rating)
        row_indices.append(user_id)
        col_indices.append(item_id)
    csr_mat = csr_matrix((data, (row_indices, col_indices)), shape=(n_rows, n_cols), )  # dtype=np.float32)
    return csr_mat
def work_with_model(model: 'AlternatingLeastSquares', ratings: 'list[dict]'):
    pprint(f'Getting results...')
    anime_ids = set(i['anime_id'] for i in ratings)
    recommends = {}
    for anime_id in anime_ids:
        perdict = model.similar_items(anime_id, 21)
        arr = perdict[0][1:]
        recommends[anime_id] = list(map(int, arr))
    pprint(f'Sending data...')
    sender.send_data(recommends)

    # recommend items for me
    # recommendations = model.recommend(1, data[1])

def work():
    """This function:
    1) Download data from server
    2) build matrix from data
    3) train model
    4) predict similar items for animes
    5) upload data to server
    """
    # Get ratings from server
    pprint(f'Start work.')
    pprint('Downloading data...')
    ratings = sender.get_data()
    # Build a matrix from ratings
    pprint(f'Building matrix...')
    csr_mat = build_matrix(ratings)

    pprint(f'Building model...')
    # initialize a model
    model = implicit.als.AlternatingLeastSquares(factors=int(os.environ.get('TRAIN_FACTORS', 50)))

    pprint(f'Training model...')
    # train the model on a sparse matrix of user/item/confidence weights
    model.fit(csr_mat)

    # do something with model
    work_with_model(model, ratings)
    pprint('Work ended.')
    pprint('__________________\n\n', ignore_time=True)


if __name__ == '__main__':
    try:
        work()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        pprint(str(e))
