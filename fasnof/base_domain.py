from datetime import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy import Column,DateTime
from sqlalchemy.ext.declarative import declared_attr
from utils.exceptions import DataNotProvidedException, FilterKeyNotPresent, MultipleRecordFoundError, ValidationError


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    created_at = Column(DateTime,default=datetime.now)
    updated_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)


class BaseModelService:
    def filter(self,**kwargs):
        keys = kwargs.keys()
        queryset = None
        if not keys:
            raise FilterKeyNotPresent("Filters can not be empty.")

        for key in keys:
            if key not in self.table_keys:
                raise FilterKeyNotPresent(message=f"{key} is not a valid key to filter.")

        try:
            queryset = self.db.query(self.model).filter_by(**kwargs)
            queryset.first()
        except Exception as e:
            self.db.rollback()

        return queryset    
    
    def raw_query(self,statement):
        queryset = None
        try:
            queryset = self.db.query(self.model).from_statement(text(statement))
            queryset.count() 
        except:
            self.db.rollback()
        return queryset
    

    def create(self,**kwargs):
        model_obj = self.model()
        keys = kwargs.keys()
        try:
            for key in keys:
                exec("model_obj.{0} = kwargs['{0}']".format(key))
        except Exception as e:
            raise ValidationError("Invalid key mapping found while updating database")
        self.db.add(model_obj) 
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValidationError(e)
        return model_obj


    def update_or_create(self,defaults={},**filters):
        if not filters:
            raise FilterKeyNotPresent("Filters can not be empty.")
        
        if not defaults:
            raise DataNotProvidedException("Defaults data can not be empty.")
        try:
            existing_queryset = self.filter(**filters)
            count = existing_queryset.count()
            if count > 1:
                raise MultipleRecordFoundError()
            
            if count == 0:
                return self.create(**defaults)
            else:
                return self.update(existing_queryset.first(),**defaults)
        except Exception as e:
            self.db.rollback()
            raise ValidationError(e)


    def get(self,**defaults):
        existing_queryset = self.filter(**defaults)
        count = existing_queryset.count()
        if count > 1:
            raise MultipleRecordFoundError()
        return existing_queryset.first()

