from src.models.model_meta import ModelMeta
from src.engines.storage_engine import StorageEngine
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from src.models.model import Model

    try:
        from typing import Self
    except ImportError:
        try:
            from typing_extensions import Self
        except ImportError:
            Self = Any


class Model(metaclass=ModelMeta):

    EXCLUDED_TO_DICT_FIELDS = set(["__module__"])

    id = None
    _meta = None
    storage_engine: 'StorageEngine[Self]' = None # type: ignore
    table_name = None


    class Meta:
        pass


    def __init__(self, *args, **kwargs):
        if args:
            raise AttributeError("Please use keyword arguments when instantiating a model.")
        
        # Filter unexpected kwargs
        unexpected_kwargs = set(kwargs) - set(self._meta.field_list)
        if unexpected_kwargs:
            raise AttributeError("Unknown keyword arguments detected: {}".format(', '.join(unexpected_kwargs)))
        
        for key, value  in kwargs.items():
            setattr(self, key, value)


    def save(self):
        self.__class__.storage_engine.create(self)

    def to_dict(self):
        result = {}
        for field in self._meta.field_list:
            if field not in self.EXCLUDED_TO_DICT_FIELDS:
                result[field] = getattr(self, field, None)
        return result

    


class TestModel(Model):
    field_1 = "A"

test_model = TestModel(id="Unique")
letters = "abcdefghijklmnopqrstuvwxyz"

model_list = [TestModel(id=letter) for letter in letters] * 100000

import time
start_time = time.time()

for idx, model in enumerate(model_list):
    model.save()

print("--- %s seconds ---" % (time.time() - start_time))
