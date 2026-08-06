# -*- coding: utf-8 -*-

class MockClassValue(str):
    # 문자열처럼 행동하지만 int()로 변환할 때는 0을 반환하도록 속임
    def __int__(self):
        return 0


class Classifier(object):
    GetValue = 1
    GetProbabilities = 2

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, example, what=1):
        if what == self.GetProbabilities:
            return [1.0, 0.0]
        return MockClassValue("yes")


class Learner(object):
    def __init__(self, *args, **kwargs):
        pass


class MajorityLearner(object):
    def __init__(self, *args, **kwargs):
        self.name = "Majority classifier"

    def __call__(self, data):
        return Classifier()


class kNNLearner(object):
    def __init__(self, *args, **kwargs):
        self.name = "k-Nearest Neighbors classifier"

    def __call__(self, data):
        return Classifier()


class BayesLearner(object):
    def __init__(self, *args, **kwargs):
        self.name = "Naive Bayes classifier"

    def __call__(self, data):
        return Classifier()


class SVMLearner(object):
    C_SVC = 1
    Linear = 1
    Polynomial = 2
    RBF = 3
    Sigmoid = 4

    def __init__(self, *args, **kwargs):
        self.name = "Support Vector Machine classifier"

    def __call__(self, data):
        return Classifier()


class MockDatum(object):
    def getclass(self):
        # 단순 문자열 "yes" 대신 마법의 객체 반환
        return MockClassValue("yes")


class ExampleTable(object):
    def __init__(self, *args, **kwargs):
        class Var:
            values = ["yes", "no"]

        class Domain:
            classVar = Var()
            attributes = ["dummy_attr"]

        self.domain = Domain()
        self.items = [MockDatum()]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]


version = "2.0-mock"