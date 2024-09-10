import re
from typing import Any, Type
from src.engines.storage_engine import StorageEngine
from src.fields.errors import FieldNotFound


class Meta:
    def __init__(self, model_cls):
        self.id = None

        # Table name will be determined from model class name.
        self._table_name = None

        # Instance of the model class.
        self.model_cls = model_cls

        # List of fields present.
        self.field_list = {}

        # By default add id field into field_list.
        self.field_list["id"] = self.id

    @property
    def table_name(self):
        if self._table_name == None:
            return self._generate_table_name(self.model_cls.__name__)
        
        return self._table_name
    
    @table_name.setter
    def table_name(self, value: str) -> None:
        self._table_name = value

    def add_field(self, field_name: str):
        self.field_list[field_name] = ""
    
    def get_field(self, field_name: str) -> Any:
        if field_name not in self.field_list:
            raise FieldNotFound(f"Field '{field_name}' not found in model '{self.model_cls.__name__}'")
        return self.field_list[field_name]
    
    def _generate_table_name(self, model_name: str) -> str:
        return re.sub('(?!^)([A-Z]+)', r'_\1', model_name).lower()
    

class ModelMeta(type):

    _meta: Meta
    _meta_cls: Type[Meta] = Meta

    def __new__(mcs, name, base, attrs): 
        cls = super().__new__(mcs, name, base, attrs)

        _meta = cls._meta_cls(cls)
        setattr(cls, '_meta', _meta)

        # For all fields, if field is a valid field type record it in metadata.
        # (TODO) Implement something other than just string fields.
        for name, field in cls.__dict__.items():
            if isinstance(field, str):
                cls._meta.add_field(name)

        # Set table name
        setattr(cls, "table_name", cls._meta.table_name)

        # Set storage engine for model class.
        setattr(cls, "storage_engine", StorageEngine())

        return cls
