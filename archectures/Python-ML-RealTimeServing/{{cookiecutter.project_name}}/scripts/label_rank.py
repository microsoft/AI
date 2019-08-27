# Copyright (C) Microsoft Corporation.  All rights reserved.

import numpy as np
import pandas as pd


def score_rank(scores):
    return pd.Series(scores).rank(ascending=False)


def label_index(label, label_order):
    loc = np.where(label == label_order)[0]
    if loc.shape[0] == 0:
        return None
    return loc[0]


def label_rank(label, scores, label_order):
    loc = label_index(label, label_order)
    if loc is None:
        return len(scores) + 1
    return score_rank(scores)[loc]
