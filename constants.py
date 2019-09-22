import os

dir_path = os.path.dirname(os.path.realpath(__file__))

GOOGLE_PATH = os.path.join(dir_path, 'google.csv')
AMAZON_PATH = os.path.join(dir_path, 'amazon.csv')

GOOGLE_SMALL_PATH = os.path.join(dir_path, 'google_small.csv')
AMAZON_SMALL_PATH = os.path.join(dir_path, 'amazon_small.csv')
GOOGLE_AMAZON_SMALL_TRUTH_PATH = os.path.join(dir_path, 'amazon_google_truth_small.csv')

GOOGLE_AMAZON_SMALL_LABEL_PATH = os.path.join(
    dir_path, 'amazon_google_truth_small.csv')
GOOGLE_AMAZON_LABEL_PATH = os.path.join(
    dir_path, 'amazon_google_truth.csv')

YEAST_PATH = os.path.join(dir_path, 'all_yeast.csv')
