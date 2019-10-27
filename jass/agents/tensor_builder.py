from typing import Union, Type

import torch
from torch.nn import functional as F

from jass.logic.card import Suit, Card


class TensorBuilder:
    @classmethod
    def bow(cls, *objects: Union[Suit, Card]) -> torch.Tensor:
        obj_type = type(objects[0])
        vector = cls.empty(obj_type=obj_type)
        for o in objects:
            assert obj_type == type(o), \
                f'cannot create a vector with objects of different type ({obj_type} != {type(o)})'
            vector[o.order_value] += 1
        return vector

    @classmethod
    def one_hot(cls, *objects: Union[Suit, Card]) -> torch.Tensor:
        obj_type = type(objects[0])
        obj_values = []
        for o in objects:
            assert obj_type == type(o), \
                f'cannot create a vector with objects of different type ({obj_type} != {type(o)})'
            obj_values.append(o.order_value)
        return F.one_hot(torch.tensor(obj_values), num_classes=len(obj_type))

    @classmethod
    def empty(cls, *size: int, obj_type: Type[Union[Suit, Card]]) -> torch.Tensor:
        return torch.zeros(*size, len(obj_type), dtype=torch.long)
