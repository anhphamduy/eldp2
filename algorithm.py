import numpy 
import pandas

def listify(x, none_value=[]):
    """Make a list of the argument if it is not a list."""

    if isinstance(x, list):
        return x
    elif isinstance(x, tuple):
        return list(x)
    elif x is None:
        return none_value
    else:
        return [x]

class BaseAlgorithm(object):
    name = None
    description = None

    def __init__(self, verify_integrity=False, suffixes=('_1', '_2')):
        super(BaseAlgorithm, self).__init__()

        self.suffixes = suffixes
        self.verify_integrity = verify_integrity

    def _make_index_names(self, name1, name2):
        if pandas.notnull(name1) and pandas.notnull(name2) and \
                (name1 == name2):
            return ["{}{}".format(name1, self.suffixes[0]),
                    "{}{}".format(name1, self.suffixes[1])]
        else:
            return [name1, name2]


    def index(self, x, x_link=None):
        x = (x, x_link)
        pairs = self._link_index(*x)
        names = self._make_index_names(x[0].index.name, x[1].index.name)

        pairs.rename(names, inplace=True)

        return pairs

class NaiveAlgorithm(BaseAlgorithm):

    def __init__(self, **kwargs):
        super(NaiveAlgorithm, self).__init__(**kwargs)

    def _link_index(self, df_a, df_b):
        return pandas.MultiIndex.from_product(
            [df_a.index.values, df_b.index.values])


class BlockAlgorithm(BaseAlgorithm):

    def __init__(self, left_on=None, right_on=None, **kwargs):
        on = kwargs.pop('on', None)
        super(BlockAlgorithm, self).__init__(**kwargs)

        # variables to block on
        self.left_on = left_on
        self.right_on = right_on

    def _get_left_and_right_on(self):

        if self.right_on is None:
            return (self.left_on, self.left_on)
        else:
            return (self.left_on, self.right_on)

    def _link_index(self, df_a, df_b):

        left_on, right_on = self._get_left_and_right_on()
        left_on = listify(left_on)
        right_on = listify(right_on)

        blocking_keys = ["blocking_key_%d" % i for i, v in enumerate(left_on)]

        # make a dataset for the data on the left
        # 1. make a dataframe
        # 2. rename columns
        # 3. add index col
        # 4. drop na (last step to presever index)
        data_left = pandas.DataFrame(df_a[left_on], copy=False)
        data_left.columns = blocking_keys
        data_left['index_x'] = numpy.arange(len(df_a))
        data_left.dropna(axis=0, how='any', subset=blocking_keys, inplace=True)
        print(data_left[0:1])

        # make a dataset for the data on the right
        data_right = pandas.DataFrame(df_b[right_on], copy=False)
        data_right.columns = blocking_keys
        data_right['index_y'] = numpy.arange(len(df_b))
        data_right.dropna(
            axis=0, how='any', subset=blocking_keys, inplace=True)
        print(data_right[538:540])
        # merge the dataframes
        pairs_df = data_left.merge(data_right, how='inner', on=blocking_keys)
        
        return pandas.MultiIndex(
            levels=[df_a.index.values, df_b.index.values],
            labels=[pairs_df['index_x'].values, pairs_df['index_y'].values],
            verify_integrity=False)
