import itertools
import numpy as np

n_labels = 2
n_documents = 3

def generate():
    lst = np.empty(shape=(n_labels**n_documents,n_documents), dtype=np.int8)
    for i, ranking in enumerate(lst):
        for j, label in enumerate(::-ranking):
            label = i %




# lst = [[label for label in range(n_labels)] for _ in range(n_documents)]
# # for i in range(n_labels**n_documents):
#
# print(lst)

generate()
