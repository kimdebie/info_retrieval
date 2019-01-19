import pandas as pd
import csv
import random

# data = pd.read_csv("YandexRelPredChallenge.txt", sep="\t", header=None, names=list(range(0, 16)))
data = "YandexRelPredChallenge.txt"



def learn_model_parameters(data):

    completed_queries = []

    with open(data) as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:

            if row[2] == 'Q':
                try:
                    completed_queries.append(query)
                except:
                    pass
                query = row
                query.append([])
                for i in range(5, 15):
                    query[15].append(query[i])
                    query[i] = False#[query[i], False]

            else:
                for i in range(0, 10):
                    if row[3] == query[15][i]:
                        query[i+5] = True


    headers = ['SessionID', 'TimePassed', 'TypeOfAction', 'QueryID', 'RegionID', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'ResultIDs']

    data = pd.DataFrame(completed_queries, columns=headers)
    print(data.head())




    # EM algorithm for finding optimal alpha and gamma

    # alpha (attractiveness) is defined per query-document pair
    # gamma (examination) is defined per rank

    # Set parameters to random initial values
    alpha = random.uniform(0, 1)
    gamma = random.uniform(0, 1)

    # update rule for alpha parameter
    # search_sess_query_doc: needs all search sessions with a particular query ID and doc ID, plus whether this doc was clicked or not
    #
    # sum_of_clicks_alpha = 0
    # for session in search_sess_query_doc:
    #     click_u =
    #     sum_of_clicks_alpha += click_u + (1-click_u) *
    #      ((1-old_gamma)*old_alpha / 1-old_gamma*old_alpha)
    #
    # alpha = 1/len(search_sess_query_doc) * sum_of_clicks_alpha
    #
    # # update rule for examination
    # # search_sess_all: needs all search sessions, plus whether each doc was clicked or not
    # sum_of_clicks_gamma = 0
    # for session in search_sessions_all:
    #     click_u =
    #     sum_of_clicks_gamma += click_u + (1-click_u) *
    #     (old_gamma*(1-old_alpha) / 1-old_gamma*old_alpha)
    #
    # gamma = 1/len(search_sessions) * sum_of_clicks_gamma

    return alpha, gamma

learn_model_parameters(data)

# def predict_click_probability(ranked_list, alpha, gamma):
#
#     return click_probabilities
#
# def click_documents(document, probability):
#
#     return clicked # boolean
