import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
sw = pd.read_csv("turn_successes_noidx.csv")
nosw = pd.read_csv("turn_successes_nosw_noidx.csv")

df = pd.concat([sw, nosw])
df.to_csv("turn_successes_all.csv")
"""

def roundPercentage(val):
    return np.round(val*100, 2)

def addPercentages(row):
    n = row['turned_val'] + row["not_turned_val"] + row["not_necessary_val"]
    row['turned'] = roundPercentage(row['turned_val']/n)
    row['not turned'] = roundPercentage(row['not_turned_val']/n)
    row['not necessary'] = roundPercentage(row['not_necessary_val']/n)
    return row

def getVal(results):
    turned = 0
    notTurned = 0
    notNecessary = 0
    if "turned" in results.keys():
        turned = results['turned']
    if "not_turned" in results.keys():
        notTurned = results['not_turned']
    if "not_necessary" in results.keys():
        notNecessary = results['not_necessary']
    return turned, notTurned, notNecessary

df = pd.read_csv("turn_successes_all.csv")

density = 0.05
radius = 20

for density in [0.01, 0.05, 0.09]:
    for radius in [5, 10, 20]:
        results = []
        for interval in (50, 100, 150, 200):
            dfInterval = df.loc[(df['interval'] == interval) & (df['density'] == density) & (df['radius'] == radius) , ['i','interval','switchtype','density','radius','initialState','nsm','k','result']]
            intervalResults = dfInterval['result'].value_counts()
            turned, notTurned, notNecessary = getVal(intervalResults)
            results.append([interval, "overall", turned, notTurned, notNecessary])

            dfNosw = df.loc[(df['interval'] == interval) & (df['density'] == density) & (df['radius'] == radius) & (df['switchtype'] == 'nosw') , ['i','interval','switchtype','density','radius','initialState','nsm','k','result']]
            intervalResults = dfNosw['result'].value_counts()
            turned, notTurned, notNecessary = getVal(intervalResults)
            results.append([interval, "nosw", turned, notTurned, notNecessary])

            dfNsmsw = df.loc[(df['interval'] == interval) & (df['density'] == density) & (df['radius'] == radius) & (df['switchtype'] == 'nsmsw') , ['i','interval','switchtype','density','radius','initialState','nsm','k','result']]
            intervalResults = dfNsmsw['result'].value_counts()
            turned, notTurned, notNecessary = getVal(intervalResults)
            results.append([interval, "nsmsw", turned, notTurned, notNecessary])

            dfKsw = df.loc[(df['interval'] == interval) & (df['density'] == density) & (df['radius'] == radius) & (df['switchtype'] == 'ksw') , ['i','interval','switchtype','density','radius','initialState','nsm','k','result']]
            intervalResults = dfKsw['result'].value_counts()
            turned, notTurned, notNecessary = getVal(intervalResults)
            results.append([interval, "ksw", turned, notTurned, notNecessary])



        dfRes = pd.DataFrame(results, columns=['interval', 'switchtype', 'turned', 'not_turned', 'not_necessary'])

        dfRes = dfRes.rename(columns={'turned': 'turned_val', 'not_turned': 'not_turned_val', 'not_necessary': 'not_necessary_val'})

        df2 = dfRes.apply(addPercentages, axis=1)

        print(df2)

        # df2 = df2.replace('nosw', 'switching inactive')
        # df2 = df2.replace('nsmsw', 'neighbour selection mechanism switching')
        # df2 = df2.replace('ksw', 'k switching')


        for interval in [50, 100, 150, 200]:
            dfInterval = df2.loc[(df2['interval'] == interval), ['switchtype', 'turned', 'not turned', 'not necessary']]
            dfInterval = dfInterval.set_index('switchtype')
            dfInterval.plot.bar(ylim=(0,100))
            plt.savefig(f"turn_success_interval={interval}_d={density}_r={radius}.svg")