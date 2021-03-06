import pytest
import math
import random
from utils import open_data
from learning import *


random.seed("aima-python")


def test_euclidean():
    distance = euclidean_distance([1, 2], [3, 4])
    assert round(distance, 2) == 2.83

    distance = euclidean_distance([1, 2, 3], [4, 5, 6])
    assert round(distance, 2) == 5.2

    distance = euclidean_distance([0, 0, 0], [0, 0, 0])
    assert distance == 0


def test_rms_error():
    assert rms_error([2, 2], [2, 2]) == 0
    assert rms_error((0, 0), (0, 1)) == math.sqrt(0.5)
    assert rms_error((1, 0), (0, 1)) ==  1
    assert rms_error((0, 0), (0, -1)) ==  math.sqrt(0.5)
    assert rms_error((0, 0.5), (0, -0.5)) ==  math.sqrt(0.5)


def test_manhattan_distance():
    assert manhattan_distance([2, 2], [2, 2]) == 0
    assert manhattan_distance([0, 0], [0, 1]) == 1
    assert manhattan_distance([1, 0], [0, 1]) ==  2
    assert manhattan_distance([0, 0], [0, -1]) ==  1
    assert manhattan_distance([0, 0.5], [0, -0.5]) == 1


def test_mean_boolean_error():
    assert mean_boolean_error([1, 1], [0, 0]) == 1
    assert mean_boolean_error([0, 1], [1, 0]) == 1
    assert mean_boolean_error([1, 1], [0, 1]) == 0.5
    assert mean_boolean_error([0, 0], [0, 0]) == 0
    assert mean_boolean_error([1, 1], [1, 1]) == 0


def test_mean_error():
    assert mean_error([2, 2], [2, 2]) == 0
    assert mean_error([0, 0], [0, 1]) == 0.5
    assert mean_error([1, 0], [0, 1]) ==  1
    assert mean_error([0, 0], [0, -1]) ==  0.5
    assert mean_error([0, 0.5], [0, -0.5]) == 0.5


def test_exclude():
    iris = DataSet(name='iris', exclude=[3])
    assert iris.inputs == [0, 1, 2]


def test_parse_csv():
    Iris = open_data('iris.csv').read()
    assert parse_csv(Iris)[0] == [5.1, 3.5, 1.4, 0.2, 'setosa']


def test_weighted_mode():
    assert weighted_mode('abbaa', [1, 2, 3, 1, 2]) == 'b'


def test_weighted_replicate():
    assert weighted_replicate('ABC', [1, 2, 1], 4) == ['A', 'B', 'B', 'C']


def test_means_and_deviation():
    iris = DataSet(name="iris")

    means, deviations = iris.find_means_and_deviations()

    assert round(means["setosa"][0], 3) == 5.006
    assert round(means["versicolor"][0], 3) == 5.936
    assert round(means["virginica"][0], 3) == 6.588

    assert round(deviations["setosa"][0], 3) == 0.352
    assert round(deviations["versicolor"][0], 3) == 0.516
    assert round(deviations["virginica"][0], 3) == 0.636


def test_plurality_learner():
    zoo = DataSet(name="zoo")

    pL = PluralityLearner(zoo)
    assert pL([1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 1]) == "mammal"


def test_naive_bayes():
    iris = DataSet(name="iris")

    # Discrete
    nBD = NaiveBayesLearner(iris, continuous=False)
    assert nBD([5, 3, 1, 0.1]) == "setosa"
    assert nBD([6, 3, 4, 1.1]) == "versicolor"
    assert nBD([7.7, 3, 6, 2]) == "virginica"

    # Continuous
    nBC = NaiveBayesLearner(iris, continuous=True)
    assert nBC([5, 3, 1, 0.1]) == "setosa"
    assert nBC([6, 5, 3, 1.5]) == "versicolor"
    assert nBC([7, 3, 6.5, 2]) == "virginica"


def test_k_nearest_neighbors():
    iris = DataSet(name="iris")
    kNN = NearestNeighborLearner(iris,k=3)
    assert kNN([5, 3, 1, 0.1]) == "setosa"
    assert kNN([5, 3, 1, 0.1]) == "setosa"
    assert kNN([6, 5, 3, 1.5]) == "versicolor"
    assert kNN([7.5, 4, 6, 2]) == "virginica"


def test_decision_tree_learner():
    iris = DataSet(name="iris")
    dTL = DecisionTreeLearner(iris)
    assert dTL([5, 3, 1, 0.1]) == "setosa"
    assert dTL([6, 5, 3, 1.5]) == "versicolor"
    assert dTL([7.5, 4, 6, 2]) == "virginica"


def test_neural_network_learner():
    iris = DataSet(name="iris")
    classes = ["setosa", "versicolor", "virginica"]
    iris.classes_to_numbers(classes)
    nNL = NeuralNetLearner(iris, [5], 0.15, 75)
    tests = [([5, 3, 1, 0.1], 0),
             ([5, 3.5, 1, 0], 0),
             ([6, 3, 4, 1.1], 1),
             ([6, 2, 3.5, 1], 1),
             ([7.5, 4, 6, 2], 2),
             ([7, 3, 6, 2.5], 2)]
    assert grade_learner(nNL, tests) >= 2/3
    assert err_ratio(nNL, iris) < 0.25


def test_perceptron():
    iris = DataSet(name="iris")
    iris.classes_to_numbers()
    classes_number = len(iris.values[iris.target])
    perceptron = PerceptronLearner(iris)
    tests = [([5, 3, 1, 0.1], 0),
             ([5, 3.5, 1, 0], 0),
             ([6, 3, 4, 1.1], 1),
             ([6, 2, 3.5, 1], 1),
             ([7.5, 4, 6, 2], 2),
             ([7, 3, 6, 2.5], 2)]
    assert grade_learner(perceptron, tests) > 1/2
    assert err_ratio(perceptron, iris) < 0.4


def test_random_weights():
    min_value = -0.5
    max_value = 0.5
    num_weights = 10
    test_weights = random_weights(min_value, max_value, num_weights)
    assert len(test_weights) == num_weights
    for weight in test_weights:
        assert weight >= min_value and weight <= max_value
