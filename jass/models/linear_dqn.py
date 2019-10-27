from typing import Any, Type

from torch import nn

from jass.agents.state import State

_ls = (128, 256, 128)


class LinearDQN(nn.Module):
    @staticmethod
    def for_state(state: Type[State], layers_size=_ls):
        return LinearDQN(state.tensor_size, state.action_type.tensor_size, layers_size)

    def __init__(self, in_size, out_size, layers_size=_ls):
        super().__init__()
        inputs = [in_size] + list(layers_size[:-1])
        outputs = list(layers_size)

        self.net = nn.ModuleList()
        for in_layer, out_layer in zip(inputs, outputs):
            self.net.extend([
                nn.Linear(in_layer, out_layer),
                # nn.BatchNorm1d(out_layer),
                nn.ReLU()
            ])

        # last layer has not BN nor ReLU
        self.net.append(nn.Linear(layers_size[-1], out_size))

    # Called with either one element to determine next action, or a batch
    # during optimization.
    def forward(self, x):  # ModuleList can act as an iterable, or be indexed using ints
        return nn.Sequential(*list(self.net))(x.float())
