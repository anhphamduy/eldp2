from constants import *

class Linkage:

    def __init__(self, algorithms=[]):
        self.algorithms = algorithms

    def add_algorithm(self, algorithm):
        self.algorithms.append(algorithm)
        
    def link(self, x, x_link):

        pairs = None
        for cl_alg in self.algorithms:
            pairs_i = cl_alg.index(x, x_link)

            if pairs is None:
                pairs = pairs_i
            else:
                pairs = pairs.union(pairs_i)     
        
        return pairs

import recordlinkage
from recordlinkage.datasets import load_febrl4
import pandas
import recordlinkage

df_a, df_b = pandas.read_csv(GOOGLE_PATH), pandas.read_csv(AMAZON_PATH)
df_b['name'] = df_b['title']

# indexer = recordlinkage.Index()
# indexer.block('surname')

# candidate_links = indexer.index(df_a, df_b)

linkage = Linkage()
from algorithm import NaiveAlgorithm, BlockAlgorithm
linkage.add_algorithm(BlockAlgorithm('name'))
candidate_links = linkage.link(df_a, df_b)
print(candidate_links[1])
print(len(set([c[0] for c in candidate_links])))
print(len(set([c[1] for c in candidate_links])))
# This cell can take some time to compute.
# compare_cl = recordlinkage.Compare()

# compare_cl.exact('given_name', 'given_name', label='given_name')
# compare_cl.string('surname', 'surname', method='cosine', threshold=0.85, label='surname')
# compare_cl.exact('date_of_birth', 'date_of_birth', label='date_of_birth')
# compare_cl.exact('suburb', 'suburb', label='suburb')
# compare_cl.exact('state', 'state', label='state')
# compare_cl.string('address_1', 'address_1', threshold=0.85, label='address_1')
# print("here")
# features = compare_cl.compute(candidate_links, df_a, df_b)
