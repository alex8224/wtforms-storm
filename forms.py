# -*- coding:utf-8 -*-

from collections import OrderedDict
from itertools import ifilter

from wtforms import IntegerField, StringField, DateTimeField
from wtforms.validators import input_required
from storm.properties import Property
from storm.locals import Unicode, Int, DateTime

from wtforms_tornado import Form

from models import User


class Singleton(type):

    def __call__(clazz, *args, **kwargs):

        if hasattr(clazz, "_instance"):
            return clazz._instance
        else:
            clazz._instance = super(Singleton, clazz).__call__(*args, **kwargs)
            return clazz._instance

class _ModelFormFactory(object):
    __metaclass__ = Singleton
    
    def __init__(self):

        self.column_field = {
                    Unicode: StringField,
                    Int: IntegerField,
                    DateTime:DateTimeField
                }

    def get_field(self, column):

        if column.__class__ not in self.column_field:
            raise ValueError("%s -> field not found!" % column.__class__)

        field_cls = self.column_field[column.__class__]

        args, field_kwargs = [], {}

        field_kwargs["validators"] = []
        if "allow_none" in column.__dict__:
            allow_none = column.__dict__["allow_none"]
            if not allow_none:
               field_kwargs["validators"].append(input_required())
        
        if "default" in column.__dict__:
            field_kwargs["default"] = column.__dict__["default"]

        return field_cls(*args, **field_kwargs)

    def create_modelform(self, model, **kwargs):

        if "exclude" in kwargs:
            exclude_fields = kwargs.pop("exclude", ())
            props = ifilter(lambda (name, prop):
                            isinstance(prop, Property) and name not in exclude_fields,
                            model.__dict__.iteritems())
        elif "include" in kwargs:
             include_fields = kwargs.pop("include", ())
             props = ifilter(lambda (name, prop):
                            isinstance(prop, Property) and name in include_fields,
                            model.__dict__.iteritems())
        else:
             props = ifilter(lambda (name, prop):
                            isinstance(prop, Property),
                            model.__dict__.iteritems())
 
        attrs = OrderedDict()
        for name, prop in props:
            attrs[name] = self.get_field(prop)
        return attrs


    def __call__(self, model, **kwargs):
        return self.create_modelform(model, **kwargs)

create_modelform = _ModelFormFactory()


class ModelFormFactory(type):

    #TODO cache form_cls
    def __new__(clazz, clsname, bases, clsdict):
        if clsname == "ModelForm":
            return super(ModelFormFactory, clazz).__new__(clazz, clsname, bases, clsdict)

        if "model" not in clsdict:
            raise ValueError("model attribute must be define in Form")

        if "exclude" in clsdict and "include" in clsdict:
            raise ValueError("exclude and include both here are wrong")

        kwargs = {}
        
        if "include" in clsdict:
            kwargs["include"] = clsdict["include"]

        elif "exclude" in clsdict:
            kwargs["exclude"] = clsdict["exclude"]

        form_clsdict = create_modelform(clsdict["model"], **kwargs)
        for field_name, value in clsdict.iteritems():
            form_clsdict[field_name] = value
        return type(clsname , (Form, ), form_clsdict)

class ModelForm(object):
    __metaclass__ = ModelFormFactory


class UserForm(ModelForm):
    '''
    It will produce Class as below:

    class UserForm(Form):
       id = IntegerField()
       username = StringField(validators=[input_required()])
       address = Unicode()
    '''
    model = User

class UserForm1(ModelForm):
    '''
    It will produce Class as below:
    class UserForm(Form):
        id = IntegerField()
        username = StringField(validators=[input_required()])
    '''
    model = User
    exclude = ("address", )


class UserForm2(ModelForm):
    '''
    It will produce Class as below:
    class UserForm(Form):
        id = IntegerField()
        address = StringField()
    '''
    model = User
    include = ("id", "address")

class UserForm3(object):
    '''
    It will product Class as below:
    class UserForm(Form):
        id = IntegerField()
        username = StringField(validators=[input_required()])
        address = StringField()
        postcode = StringField(validators=[input_required()])
 
    '''
    model = User
    postcode = StringField(validators=[input_required()])
