import pandas as pd
import numpy as np
import random

# 混淆分析資料 (來自 Miller & Nicely 1955 三個 SNR 加總)
# confused: 0=容易混淆, 1=不容易混淆
CONFUSION_DATA = [
    # p
    {'sound': 'p', 'confused': 0, 'target': 'k', 'count': 207},
    {'sound': 'p', 'confused': 0, 'target': 't', 'count': 91},
    {'sound': 'p', 'confused': 0, 'target': 'theta', 'count': 30},
    {'sound': 'p', 'confused': 1, 'target': 'b', 'count': 1},
    {'sound': 'p', 'confused': 1, 'target': 'd', 'count': 1},
    {'sound': 'p', 'confused': 1, 'target': 'v', 'count': 1},
    # t
    {'sound': 't', 'confused': 0, 'target': 'p', 'count': 109},
    {'sound': 't', 'confused': 0, 'target': 'k', 'count': 97},
    {'sound': 't', 'confused': 0, 'target': 'theta', 'count': 9},
    {'sound': 't', 'confused': 1, 'target': 'g', 'count': 1},
    {'sound': 't', 'confused': 1, 'target': 'eth', 'count': 1},
    {'sound': 't', 'confused': 1, 'target': 'z', 'count': 1},
    # k
    {'sound': 'k', 'confused': 0, 'target': 'p', 'count': 190},
    {'sound': 'k', 'confused': 0, 'target': 't', 'count': 127},
    {'sound': 'k', 'confused': 0, 'target': 'f', 'count': 17},
    {'sound': 'k', 'confused': 1, 'target': 'n', 'count': 3},
    {'sound': 'k', 'confused': 1, 'target': 'g', 'count': 1},
    {'sound': 'k', 'confused': 1, 'target': 'z', 'count': 1},
    # f
    {'sound': 'f', 'confused': 0, 'target': 'theta', 'count': 151},
    {'sound': 'f', 'confused': 0, 'target': 'p', 'count': 27},
    {'sound': 'f', 'confused': 0, 'target': 's', 'count': 18},
    {'sound': 'f', 'confused': 1, 'target': 'sh', 'count': 1},
    {'sound': 'f', 'confused': 1, 'target': 'g', 'count': 1},
    {'sound': 'f', 'confused': 1, 'target': 'n', 'count': 1},
    # theta
    {'sound': 'theta', 'confused': 0, 'target': 'f', 'count': 260},
    {'sound': 'theta', 'confused': 0, 'target': 's', 'count': 45},
    {'sound': 'theta', 'confused': 0, 'target': 'p', 'count': 35},
    {'sound': 'theta', 'confused': 1, 'target': 'd', 'count': 4},
    {'sound': 'theta', 'confused': 1, 'target': 'm', 'count': 1},
    {'sound': 'theta', 'confused': 1, 'target': 'n', 'count': 1},
    # s
    {'sound': 's', 'confused': 0, 'target': 'theta', 'count': 84},
    {'sound': 's', 'confused': 0, 'target': 'sh', 'count': 57},
    {'sound': 's', 'confused': 0, 'target': 'f', 'count': 29},
    {'sound': 's', 'confused': 1, 'target': 'zh', 'count': 2},
    {'sound': 's', 'confused': 1, 'target': 'eth', 'count': 1},
    {'sound': 's', 'confused': 1, 'target': 'n', 'count': 1},
    # sh
    {'sound': 'sh', 'confused': 0, 'target': 's', 'count': 56},
    {'sound': 'sh', 'confused': 0, 'target': 'theta', 'count': 9},
    {'sound': 'sh', 'confused': 0, 'target': 't', 'count': 7},
    {'sound': 'sh', 'confused': 1, 'target': 'f', 'count': 4},
    {'sound': 'sh', 'confused': 1, 'target': 'p', 'count': 1},
    {'sound': 'sh', 'confused': 1, 'target': 'm', 'count': 1},
    # b
    {'sound': 'b', 'confused': 0, 'target': 'v', 'count': 81},
    {'sound': 'b', 'confused': 0, 'target': 'eth', 'count': 74},
    {'sound': 'b', 'confused': 0, 'target': 'z', 'count': 19},
    {'sound': 'b', 'confused': 1, 'target': 'n', 'count': 4},
    {'sound': 'b', 'confused': 1, 'target': 'zh', 'count': 3},
    {'sound': 'b', 'confused': 1, 'target': 'p', 'count': 1},
    # d
    {'sound': 'd', 'confused': 0, 'target': 'g', 'count': 107},
    {'sound': 'd', 'confused': 0, 'target': 'zh', 'count': 39},
    {'sound': 'd', 'confused': 0, 'target': 'eth', 'count': 33},
    {'sound': 'd', 'confused': 1, 'target': 'b', 'count': 12},
    {'sound': 'd', 'confused': 1, 'target': 'theta', 'count': 3},
    {'sound': 'd', 'confused': 1, 'target': 'n', 'count': 3},
    # g
    {'sound': 'g', 'confused': 0, 'target': 'v', 'count': 197},
    {'sound': 'g', 'confused': 0, 'target': 'd', 'count': 148},
    {'sound': 'g', 'confused': 0, 'target': 'zh', 'count': 83},
    {'sound': 'g', 'confused': 1, 'target': 's', 'count': 2},
    {'sound': 'g', 'confused': 1, 'target': 'theta', 'count': 1},
    {'sound': 'g', 'confused': 1, 'target': 'm', 'count': 1},
    # v
    {'sound': 'v', 'confused': 0, 'target': 'eth', 'count': 379},
    {'sound': 'v', 'confused': 0, 'target': 'z', 'count': 88},
    {'sound': 'v', 'confused': 0, 'target': 'd', 'count': 81},
    {'sound': 'v', 'confused': 1, 'target': 'm', 'count': 7},
    {'sound': 'v', 'confused': 1, 'target': 'n', 'count': 4},
    {'sound': 'v', 'confused': 1, 'target': 's', 'count': 2},
    # eth
    {'sound': 'eth', 'confused': 0, 'target': 'z', 'count': 255},
    {'sound': 'eth', 'confused': 0, 'target': 'v', 'count': 81},
    {'sound': 'eth', 'confused': 0, 'target': 'zh', 'count': 44},
    {'sound': 'eth', 'confused': 1, 'target': 'f', 'count': 1},
    {'sound': 'eth', 'confused': 1, 'target': 'theta', 'count': 1},
    {'sound': 'eth', 'confused': 1, 'target': 's', 'count': 1},
    # z
    {'sound': 'z', 'confused': 0, 'target': 'zh', 'count': 242},
    {'sound': 'z', 'confused': 0, 'target': 'eth', 'count': 162},
    {'sound': 'z', 'confused': 0, 'target': 'v', 'count': 48},
    {'sound': 'z', 'confused': 1, 'target': 'p', 'count': 1},
    {'sound': 'z', 'confused': 1, 'target': 's', 'count': 1},
    {'sound': 'z', 'confused': 1, 'target': 'sh', 'count': 1},
    # zh
    {'sound': 'zh', 'confused': 0, 'target': 'z', 'count': 451},
    {'sound': 'zh', 'confused': 0, 'target': 'd', 'count': 31},
    {'sound': 'zh', 'confused': 0, 'target': 'g', 'count': 25},
    {'sound': 'zh', 'confused': 1, 'target': 's', 'count': 1},
    {'sound': 'zh', 'confused': 1, 'target': 'sh', 'count': 1},
    {'sound': 'zh', 'confused': 1, 'target': 'b', 'count': 1},
    # m
    {'sound': 'm', 'confused': 0, 'target': 'n', 'count': 54},
    {'sound': 'm', 'confused': 0, 'target': 'b', 'count': 5},
    {'sound': 'm', 'confused': 0, 'target': 's', 'count': 4},
    {'sound': 'm', 'confused': 1, 'target': 'p', 'count': 1},
    {'sound': 'm', 'confused': 1, 'target': 'theta', 'count': 1},
    {'sound': 'm', 'confused': 1, 'target': 'z', 'count': 1},
    # n
    {'sound': 'n', 'confused': 0, 'target': 'm', 'count': 57},
    {'sound': 'n', 'confused': 0, 'target': 'z', 'count': 7},
    {'sound': 'n', 'confused': 0, 'target': 'd', 'count': 5},
    {'sound': 'n', 'confused': 1, 'target': 'b', 'count': 3},
    {'sound': 'n', 'confused': 1, 'target': 'g', 'count': 2},
    {'sound': 'n', 'confused': 1, 'target': 'zh', 'count': 1},
]

def _generate_trials_pool():
    """產生所有 sound + confusable + distinct 組合"""
    df = pd.DataFrame(CONFUSION_DATA)
    confusable = df[df['confused'] == 0]
    distinct = df[df['confused'] == 1]
    sounds = df['sound'].unique()

    trials = []
    idx = 1

    for sound in sounds:
        conf_rows = confusable[confusable['sound'] == sound]
        dist_rows = distinct[distinct['sound'] == sound]

        for _, conf_row in conf_rows.iterrows():
            for _, dist_row in dist_rows.iterrows():
                conf_target = conf_row['target']
                dist_target = dist_row['target']

                if conf_target == dist_target:
                    continue

                trials.append({
                    'id': idx,
                    'sound': sound,
                    'confusable': conf_target,
                    'confusable_count': int(conf_row['count']),
                    'distinct': dist_target,
                    'distinct_count': int(dist_row['count'])
                })
                idx += 1

    return trials


# 完整 trial pool (144 組)
TRIALS_POOL = _generate_trials_pool()

def get_trials(n=24):
    """隨機取 n 組 trial，回傳 list of (sound, confusable, distinct)"""
    selected = random.sample(TRIALS_POOL, n)
    return [[t['sound'], t['confusable'], t['distinct']] for t in selected]

