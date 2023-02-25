import torch


class ATOM():
    def __init__(self, model, optimizer, dropout, hid_dim, learning_rate=0.001, weight_decay=0.001, momentum=0,
                 epochs=20, delta_loss_cap=0.01, short_delta_loss_cap=0.01):

        self.model = model
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.optimizer = optimizer
        self.dropout = dropout
        self.hid_dim = hid_dim
        self.weight_decay = weight_decay
        self.momentum = momentum
        self.delta_loss_cap = delta_loss_cap
        self.short_delta_loss_cap = short_delta_loss_cap
        self.FIRST_RUN = True

        if self.optimizer == 'adam':
            self.optimizer = {"type": torch.optim.Adam, "lr": self.learning_rate, "weight_decay": self.weight_decay}
        elif self.optimizer == 'sgd':
            self.optimizer = {"type": torch.optim.SGD, "lr": self.learning_rate, "weight_decay": self.weight_decay,
                              "momentum": self.momentum}
        else:
            raise ValueError("Optimizer not supported")

        self.atom = {'lr': self.learning_rate, 'epochs': self.epochs, 'optimizer': self.optimizer,
                     'dropout': self.dropout, 'hid_dim': self.hid_dim}
        # {epoch_num: {'train_loss': [], 'val_loss': []}
        self.e_log = {}

        # all epochs
        self.delta_val_loss = 0
        self.delta_train_loss = 0

        # 4 epochs
        self.delta_count = 0
        self.short_delta_val_loss = 0
        self.short_delta_train_loss = 0


    def update_loss_delta(self):
        for e in range(1, len(self.e_log)):
            self.delta_val_loss = self.e_log[e]['val_loss'] - self.e_log[e - 1]['val_loss']
            self.delta_train_loss = self.e_log[e]['train_loss'] - self.e_log[e - 1]['train_loss']

            if self.delta_count == 4:
                self.delta_count = 0
                self.short_delta_val_loss = 0
                self.short_delta_train_loss = 0

            self.short_delta_val_loss = self.e_log[e]['val_loss'] - self.e_log[e - 4]['val_loss']
            self.short_delta_train_loss = self.e_log[e]['train_loss'] - self.e_log[e - 4]['train_loss']

    def analyze_run(self):
        # Check if loss is decreasing, check if it is below the cap
        self.update_loss_delta()

        if len(self.e_log) > 5:
            if self.short_delta_val_loss < self.short_delta_loss_cap:
                print("Loss is decreasing, but below the cap")


    def return_run_values(self):
        return self.atom

    def log(self, epoch: int, train_loss: float, val_loss: float):
        self.e_log[epoch] = {'train_loss': train_loss, 'val_loss': val_loss}
        if len(self.e_log) > 1:
            self.analyze_run()




    def run_experiment(self):

        if self.FIRST_RUN:  # TEST: 01 does not require optimization
            self.FIRST_RUN = False
            self.return_run_values()

        # return updated atom

        self.return_run_values()


2 - 1
3 - 2
4 - 3
5 - 4
6 - 5
7 - 6
8 - 7
9 - 8
10 - 9
11 - 10
