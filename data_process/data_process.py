import pandas as pd
import numpy as np
import re
import random
import matplotlib.pyplot as plt
import seaborn as snsm
import json
import datetime as dt
import os

# 필요한 패키지와 라이브러리를 가져옴
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from IPython.display import set_matplotlib_formats

# 그래프에서 마이너스 폰트 깨지는 문제에 대한 대처
mpl.rcParams['axes.unicode_minus'] = False
print('버전: ', mpl.__version__)
print('설치 위치: ', mpl.__file__)
print('설정 위치: ', mpl.get_configdir())
print('캐시 위치: ', mpl.get_cachedir())
print('설정 파일 위치: ', mpl.matplotlib_fname())
font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')

# ttf 폰트 전체개수
f = [f.name for f in fm.fontManager.ttflist]
font_name = fm.FontProperties(size=50).get_name()
print(font_name)
plt.rc('font', family=font_name)
set_matplotlib_formats('retina')
plt.rcParams['font.family'] = 'AppleGothic'


class InstaTagData():
    def __init__(self, file_path=None, tag='망원동', dir_path='/Users/dhkim/PycharmProjects/instagramScraper/scraped'
                                                           '/hashtag/'):
        print(f'{tag} data process start!')
        self.tag = tag
        self.dir_path = dir_path
        self.records = []
        self.file_paths = []
        self.df = None
        if file_path is not None:
            self.file_path = file_path
            self.file_paths = [file_path]
        else:
            self.file_dir_path = os.path.join(self.dir_path, self.tag)
            for file in os.listdir(self.file_dir_path):
                if not file.startswith('.'):
                    self.file_paths.append(os.path.join(self.file_dir_path, file))

    def read_json(self):
        for _path in self.file_paths:
            for line in open(_path, 'r'):
                self.records.append(json.loads(line))
        self.df = pd.DataFrame.from_records(self.records)
        self.df = self.df.drop_duplicates()
        print(f'{self.tag} total {self.df.shape[0]}s data is collected.\n')

    def preprocess(self):
        self.df['time'] = self.df['taken_at_timestamp'].map(lambda x: dt.datetime.fromtimestamp(x).strftime('%Y-%m-%d '
                                                                                                            '%H:%M:%S'))

        col_reorder = [self.df.columns[-1]] + list(self.df.columns)[:-1]
        self.df = self.df[col_reorder]

    def write_csv(self):
        save_name = os.path.join(os.path.dirname(self.dir_path), self.tag + '.csv')
        self.df.to_csv(save_name, sep='\t')


if __name__ == '__main__':
    tags = ['망원동', '상수', '여의도', '연남동', '영등포', '홍대', '합정']
    for tag in tags:
        instadata = InstaTagData(tag=tag)
        instadata.read_json()
        instadata.preprocess()
        instadata.write_csv()
