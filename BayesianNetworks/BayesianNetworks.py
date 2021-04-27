from functools import reduce

import numpy as np
import pandas as pd


# Function to create a conditional probability table
# Conditional probability is of the form p(x1 | x2, ..., xk)
# varnames: vector of variable names (strings) first variable listed
#           will be x_i, remainder will be parents of x_i, p1, ..., pk
# probs: vector of probabilities for the flattened probability table
# outcomesList: a list containing a vector of outcomes for each variable
# factorTable is in the type of pandas dataframe
# See the example file for examples of how this function works

def readFactorTable(varnames, probs, outcomesList):
    factorTable = pd.DataFrame({'probs': probs})

    totalfactorTableLength = len(probs)
    numVars = len(varnames)

    k = 1
    for i in range(numVars - 1, -1, -1):
        levs = outcomesList[i]
        numLevs = len(levs)
        col = []
        for j in range(0, numLevs):
            col = col + [levs[j]] * k
        factorTable[varnames[i]] = col * int(totalfactorTableLength / (k * numLevs))
        k = k * numLevs

    return factorTable


# Build a factorTable from a data frame using frequencies
# from a data frame of data to generate the probabilities.
# data: data frame read using pandas read_csv
# varnames: specify what variables you want to read from the table
# factorTable is in the type of pandas dataframe
def readFactorTablefromData(data, varnames):
    numVars = len(varnames)
    outcomesList = []

    for i in range(0, numVars):
        name = varnames[i]
        outcomesList = outcomesList + [list(set(data[name]))]

    lengths = list(map(lambda x: len(x), outcomesList))
    m = reduce(lambda x, y: x * y, lengths)

    factorTable = pd.DataFrame({'probs': np.zeros(m)})

    k = 1
    for i in range(numVars - 1, -1, -1):
        levs = outcomesList[i]
        numLevs = len(levs)
        col = []
        for j in range(0, numLevs):
            col = col + [levs[j]] * k
        factorTable[varnames[i]] = col * int(m / (k * numLevs))
        k = k * numLevs

    numLevels = len(outcomesList[0])

    # creates the vector called fact to index probabilities 
    # using matrix multiplication with the data frame
    fact = np.zeros(data.shape[1])
    lastfact = 1
    for i in range(len(varnames) - 1, -1, -1):
        fact = np.where(np.isin(list(data), varnames[i]), lastfact, fact)
        lastfact = lastfact * len(outcomesList[i])

    # Compute unnormalized counts of subjects that satisfy all conditions
    a = (data - 1).dot(fact) + 1
    for i in range(0, m):
        factorTable.at[i, 'probs'] = sum(a == (i + 1))

    # normalize the conditional probabilities
    skip = int(m / numLevels)
    for i in range(0, skip):
        normalizeZ = 0
        for j in range(i, m, skip):
            normalizeZ = normalizeZ + factorTable['probs'][j]
        for j in range(i, m, skip):
            if normalizeZ != 0:
                factorTable.at[j, 'probs'] = factorTable['probs'][j] / normalizeZ

    return factorTable


# Join of two factors
# factor1, factor2: two factor tables
#
# Should return a factor table that is the join of factor 1 and 2.
# You can assume that the join of two factors is a valid operation.
# Hint: You can look up pd.merge for mergin two factors
def joinFactors(factor1, factor2):
    f1 = pd.DataFrame.copy(factor1)
    f2 = pd.DataFrame.copy(factor2)

    joinFactor = None

    # TODO: start your code
    # 找到两个df的相同列，之后用作merge
    c1 = f1.columns.values
    c2 = f2.columns.values
    same = []
    for c in c1:
        if c in c2 and c != 'probs':
            same.append(c)

    if len(same) > 0:
        joinFactor = f1.merge(f2, on=same)
        joinFactor.insert(0, 'probs', joinFactor['probs_x'] * joinFactor['probs_y'])
        joinFactor.drop(['probs_x', 'probs_y'], axis=1, inplace=True)
    else:
        f1['same'], f2['same'] = 0, 0
        joinFactor = f1.merge(f2, on='same')
        joinFactor.insert(0, 'probs', joinFactor['probs_x'] * joinFactor['probs_y'])
        joinFactor.drop(['probs_x', 'probs_y', 'parent'], axis=1, inplace=True)
    # end of your code

    return joinFactor


# Marginalize a variable from a factor
# table: a factor table in dataframe
# hiddenVar: a string of the hidden variable name to be marginalized
#
# Should return a factor table that marginalizes margVar out of it.
# Assume that hiddenVar is on the left side of the conditional.
# Hint: you can look can pd.groupby
def marginalizeFactor(factorTable, hiddenVar):

    if hiddenVar not in list(factorTable.columns):
        return factorTable

    # TODO: start your code
    if len(list(factorTable.columns)) <= 2:
        return factorTable
    if hiddenVar is None or hiddenVar == []:
        return factorTable
    rest_of_factors = list(factorTable.drop(['probs', hiddenVar], axis = 1).columns)
    factor = factorTable.groupby(rest_of_factors).sum().reset_index()
    factor.drop(hiddenVar, axis=1, inplace=True)
    # end of your code

    return factor


# Marginalize a list of variables
# bayesnet: a list of factor tables and each table in dataframe type
# hiddenVar: a string of the variable name to be marginalized
#
# Should return a Bayesian network containing a list of factor tables that results
# when the list of variables in hiddenVar is marginalized out of bayesnet.
def marginalizeNetworkVariables(bayesNet, hiddenVar):
    if isinstance(hiddenVar, str):
        hiddenVar = [hiddenVar]

    if not bayesNet or not hiddenVar:
        return bayesNet

    marginalizeBayesNet = bayesNet.copy()

    # TODO: start your code
    for i in range(len(bayesNet)):
        for j in range(len(hiddenVar)):
            marginalizeBayesNet[i] = marginalizeFactor(marginalizeBayesNet[i], hiddenVar[j])
    # end of your code

    return marginalizeBayesNet


# Update BayesNet for a set of evidence variables
# bayesNet: a list of factor and factor tables in dataframe format
# evidenceVars: a vector of variable names in the evidence list
# evidenceVals: a vector of values for corresponding variables (in the same order)
#
# Set the values of the evidence variables. Other values for the variables
# should be removed from the tables. You do not need to normalize the factors
def evidenceUpdateNet(bayesNet, evidenceVars, evidenceVals):
    if isinstance(evidenceVars, str):
        evidenceVars = [evidenceVars]
    if isinstance(evidenceVals, str):
        evidenceVals = [evidenceVals]

    updatedBayesNet = bayesNet.copy()
    # TODO: start your code
    if evidenceVars is None or evidenceVars == []:
        return updatedBayesNet
    # 字符串转int
    evidenceVals = [int(i) for i in evidenceVals]
    # 创建一个dataframe放已知的evidence，之后用于跟原始的df作比对（merge）
    df_evi = pd.DataFrame([evidenceVals], columns=evidenceVars)

    for i in range(len(updatedBayesNet)):
        col1 = list(updatedBayesNet[i].columns)
        flag = False
        # 判断表中有没有要删除的factor
        for k in range(len(evidenceVars)):
            if evidenceVars[k] in col1:
                flag = True
                break
        if not flag:
            continue
        df_tmp = updatedBayesNet[i].copy()
        df_tmp = pd.merge(df_tmp, df_evi)
        col2 = list(df_tmp.columns)
        # 去掉多余的columns
        for j in range(len(col2)):
            if not col2[j] in col1:
                df_tmp = df_tmp.drop(col2[j], axis=1)

        updatedBayesNet[i] = df_tmp
    # end of your code

    return updatedBayesNet


# Run inference on a Bayesian network
# bayesNet: a list of factor tables and each table iin dataframe type
# hiddenVar: a string of the variable name to be marginalized
# evidenceVars: a vector of variable names in the evidence list
# evidenceVals: a vector of values for corresponding variables (in the same order)
#
# This function should run variable elimination algorithm by using
# join and marginalization of the sets of variables.
# The order of the elimiation can follow hiddenVar ordering
# It should return a single joint probability table. The
# variables that are hidden should not appear in the table. The variables
# that are evidence variable should appear in the table, but only with the single
# evidence value. The variables that are not marginalized or evidence should
# appear in the table with all of their possible values. The probabilities
# should be normalized to sum to one.
def inference(bayesNet, hiddenVar, evidenceVars, evidenceVals):
    if not bayesNet:
        return bayesNet

    inferenceNet = bayesNet.copy()
    factor = None
    # TODO: start your code
    # evidence
    new_bayesNet = evidenceUpdateNet(inferenceNet, evidenceVars, evidenceVals)
    # join
    join_result = new_bayesNet[0]
    for k in range(1, len(new_bayesNet)):
        join_result = joinFactors(join_result, new_bayesNet[k])
    # join_result = joinFactors(joinFactors(new_bayesNet[0], new_bayesNet[1]), new_bayesNet[2])
    factor = join_result
    # eliminate
    for i in range(len(hiddenVar)):
        factor = marginalizeFactor(factor, hiddenVar[i])
    # 标准化
    sum_f = sum(factor['probs'])
    factor['probs'] = factor['probs'] / sum_f
    # end of your code

    return factor

