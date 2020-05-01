# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019

"""
You should only modify code within this file for part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network
        @param lrate: The learning rate for the model.
        @param loss_fn: The loss function
        @param in_size: Dimension of input
        @param out_size: Dimension of output
        The network should have the following architecture (in terms of hidden units):
        in_size -> 128 ->  out_size
        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.net = torch.nn.Sequential(
            torch.nn.Linear(in_size, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, out_size)
        )

        self.optimizer = optim.Adam(self.net.parameters(), lrate)

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return self.net.parameters()


    def forward(self, x):
        """ A forward pass of your autoencoder
        @param x: an (N, in_size) torch tensor
        @return y: an (N, out_size) torch tensor of output from the network
        """
        y_pred = self.net(x)
        return y_pred

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        # Zero gradients, perform a backward pass, and update the weights.
        self.optimizer.zero_grad()

        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        loss.backward()

        self.optimizer.step()

        return loss
def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Fit a neural net.  Use the full batch size.
    @param train_set: an (N, 784) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M, 784) torch tensor
    @param n_iter: int, the number of batches to go through during training (not epoches)
                   when n_iter is small, only part of train_set will be used, which is OK,
                   meant to reduce runtime on autograder.
    @param batch_size: The size of each batch to train on.
    # return all of these:
    @return losses: list of total loss (as type float) after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of approximations to labels for dev_set
    @return net: A NeuralNet object
    # NOTE: This must work for arbitrary M and N
    """
    lrate = 0.0001
    losses = np.zeros((n_iter, ))
    yhats = np.zeros((len(dev_set),))
    loss_fn = torch.nn.CrossEntropyLoss()
    input_size = train_set.shape[1]

    dataset = TensorDataset(train_set, train_labels)
    data_pair = DataLoader(dataset, batch_size = batch_size)


    nn = NeuralNet(lrate, loss_fn, input_size, 5)

    for i in range(n_iter):
        for data in data_pair:
            losses[i] += nn.step(data[0], data[1])

    for index, data in enumerate(dev_set):
        y_pred = nn.forward(data)
        yhats[index] = torch.max(y_pred, 0)[1]
    return losses, yhats, nn

