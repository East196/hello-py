#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("food.csv")
df["day"] = df["time"].apply(lambda time: time.split(" ")[0])
df2 = df[df.type == "milk"].groupby(by=["day"])["size"].agg({"size": np.sum}).reindex()

df2.plot()
plt.show()
# raw_input()
