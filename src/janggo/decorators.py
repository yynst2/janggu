"""Decorators to build neural networks.

This module contains decorators for automatically
appending an input and output layer of a neural network
with the correct dimensions.
There goal is to avoid having to define those layers.
Only the network body needs to be defined.
"""
from functools import wraps

from keras.layers import Dense
from keras.layers import Input


def outputlayer(func):
    """Output layer decorator

    This decorator appends an output layer to the
    network with the correct shape, activation and name.
    """
    @wraps(func)
    def _add(inputs, inshapes, outshapes, params):
        inputs, outputs = func(inputs, inshapes, outshapes, params)
        outputs = [Dense(outshapes[name]['shape'][0],
                         activation=outshapes[name]['activation'],
                         name=name)(outputs) for name in outshapes]
        return inputs, outputs
    return _add


def inputlayer(func):
    """Input layer decorator

    This decorator appends an input layer to the
    network with the correct shape and name.
    """
    @wraps(func)
    def _add(inputs, inshapes, outshapes, params):
        inputs = InputList([Input(inshapes[name]['shape'], name=name)
                            for name in inshapes])
        inputs, outputs = func(inputs, inshapes, outshapes, params)
        return inputs(), outputs
    return _add


class InputList(object):
    """Convenience class for querying inputs.

    This class holds a list of input-tensors
    (e.g. as created by inputlayer) and provides
    simple access methods to obtain a certain
    layer by name.
    """
    input_list = None
    name = None

    def __init__(self, inputs):
        self.input_list = inputs

    def __getitem__(self, name):
        if isinstance(name, str):
            for input_ in self.input_list:
                print(input_.name)
                if name in input_.name:
                    return input_
            raise IndexError("No input with name {} defined. Options are {}".format(name, self.input_list))
        elif isinstance(name, int):
            return self.input_list[name]
        else:
            IndexError("Wrong type {} for indexing".format(type(name)))

    def __call__(self):
        return self.input_list

    def use(self, name):
        """Method selects the layer to be used.

        Parameters
        ----------
        name : str or int
            layer name or integer index to access a particular
            input layer.

        Returns
        -------
        object :
            Returns itself after having set the name attribute.
        """
        self.name = name
        return self

    def __enter__(self):
        return self[self.name]

    def __exit__(self, exctype, excvalue, traceback):
        pass