from typing import Generic, TypeVar, TYPE_CHECKING, Any
import json
from src.settings import TEXTDB_ROOT_DIRECTORY
from pathlib import Path


if TYPE_CHECKING:
    from src.models.model import Model

    try:
        from typing import Self
    except ImportError:
        try:
            from typing_extensions import Self
        except ImportError:
            Self = Any


ModelType = TypeVar('ModelType', bound='Model')


class StorageEngine(Generic[ModelType]):
    def create(self, model_cls):
        output_file = Path(f"{TEXTDB_ROOT_DIRECTORY}/{model_cls.table_name}.json")
        output_file.parent.mkdir(exist_ok=True, parents=True)
        
        with open(output_file, "a") as file:
            file.write(json.dumps(model_cls.to_dict()) + '\n')
