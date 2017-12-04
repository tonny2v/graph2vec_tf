import time,json
from utils import get_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC,LinearSVC
import gensim
from random import randint
import numpy as np
import logging
from scipy.sparse import csr_matrix
from sklearn.model_selection import GridSearchCV

from utils import get_class_labels

logger = logging.getLogger()
logger.setLevel("INFO")

def subgraph2vec_tokenizer (s):
    '''
    Tokenize the string from subgraph2vec sentence (i.e. <target> <context1> <context2> ...). Just target is to be used
    and context strings to be ignored.
    :param s: context of subgraph2vec file.
    :return: List of targets from subgraph2vec file.
    '''
    return [line.split(' ')[0] for line in s.split('\n')]


def linear_svm_classify (X_train, X_test, Y_train, Y_test):
    '''
    Classifier with graph embeddings
    :param X_train: training feature vectors
    :param X_test: testing feature vectors
    :param Y_train: training set labels
    :param Y_test: test set labels
    :return: None
    '''
    params = {'C':[0.01,0.1,1,10,100,1000]}
    classifier = GridSearchCV(LinearSVC(), params, cv=5, scoring='f1',verbose=1)
    classifier.fit(X_train,Y_train)
    logging.info('best classifier model\'s hyperparamters', classifier.best_params_)

    Y_pred = classifier.predict(X_test)

    acc = accuracy_score(Y_test, Y_pred)
    logging.info('Linear SVM accuracy: {}'.format(acc))

    logging.info(classification_report(Y_test, Y_pred))


def perform_classification (corpus_dir, extn, embedding_fname, class_labels_fname):
    '''
    Perform classification from
    :param corpus_dir: folder containing subgraph2vec sentence files
    :param extn: extension of subgraph2vec sentence files
    :param embedding_fname: file containing subgraph vectors in word2vec format (refer Mikolov et al (2013) code)
    :param class_labels_fname: files containing labels of each graph
    :return: None
    '''

    wlk_files = get_files(corpus_dir, extn)

    seed = randint(0, 1000)


    with open(embedding_fname,'r') as fh:
        graph_embedding_dict = json.load(fh)
    X = np.array([graph_embedding_dict[fname] for fname in wlk_files])
    # X = normalizer.fit_transform(X)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=seed)
    logging.info('Train and Test matrix shapes: {}, {}, {}, {} '.format(X_train.shape, X_test.shape,
                                                                        Y_train.shape, Y_test.shape))

    linear_svm_classify(X_train, X_test, Y_train, Y_test)


if __name__ == '__main__':
    pass