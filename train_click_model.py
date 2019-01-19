import pandas as pd
import csv
import random

# data = pd.read_csv("YandexRelPredChallenge.txt", sep="\t", header=None, names=list(range(0, 16)))
data = "YandexRelPredChallenge.txt"



def learn_model_parameters(data):

    # Cleaning data

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
                for i in range(5, 8):
                    query[15].append(query[i])
                    query[i] = False

            else:
                for i in range(0, 3):
                    if row[3] == query[15][i]:
                        query[i+5] = True

    headers = ['SessionID', 'TimePassed', 'TypeOfAction', 'QueryID', 'RegionID', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'ResultIDs']
    data = pd.DataFrame(completed_queries, columns=headers)
    #print(data.head())

    query_doc_pairs = [] #[queryID-docID, rank, clicked]
    for index, query in data.iterrows():
        for i, doc in enumerate(query['ResultIDs']):
            row = [str(query['QueryID']) + '-' + str(doc), i, query[i]]
            query_doc_pairs.append(row)

    headers2 = ["QueryDocPair", "Rank", "Clicked"]
    qd_pairs = pd.DataFrame(query_doc_pairs, columns=headers2)


    ## EM algorithm for finding optimal alpha and gamma ##

    # Set parameters to initial values

    # alpha (attractiveness) is defined per unique query-document pair
    alphas = {}
    for index in qd_pairs["QueryDocPair"].unique():
        alphas[index] = 0.5
    print("Total alphas to be trained: " + str(len(alphas)))

    # gamma (examination) is defined per rank
    gammas = [0.2, 0.2, 0.2]


    # Expectation step
    for i in range(0, 100):
        print(i)

        # update rule for alpha parameters
        # print("Update alphas")
        for index in qd_pairs["QueryDocPair"].unique(): # update one alpha for each QD pair
            sess_qd = qd_pairs[qd_pairs["QueryDocPair"] == index]
            old_alpha = alphas[index]

            sum_of_clicks_alpha = 0
            for i, session in sess_qd.iterrows(): # for each session of a QD pair

                click_u = session["Clicked"]
                old_gamma = gammas[session["Rank"]]

                sum_of_clicks_alpha += click_u + (1-click_u) * \
                 ((1-old_gamma)*old_alpha / 1-old_gamma*old_alpha)

            alphas[index] = 1/sess_qd.shape[0] * sum_of_clicks_alpha


        # update rule for examination
        print("Update gammas")
        for rank, gamma in enumerate(gammas):

            sess_rank = qd_pairs[qd_pairs["Rank"] == rank]
            old_gamma = gammas[rank]

            sum_of_clicks_gamma = 0
            for i, session in sess_rank.iterrows():
                click_u = session["Clicked"]
                old_alpha = alphas[session["QueryDocPair"]]

                sum_of_clicks_gamma += click_u + (1-click_u) * \
                (old_gamma*(1-old_alpha) / 1-old_gamma*old_alpha)

            gammas[rank] = 1/len(sess_rank) * sum_of_clicks_gamma
        print(gammas)

    return alphas, gammas

learn_model_parameters(data)

# def predict_click_probability(ranked_list, alpha, gamma):
#
#     return click_probabilities
#
# def click_documents(document, probability):
#
#     return clicked # boolean
