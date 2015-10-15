WTForms-Storm
===============

Tools for creating WTForms from Storm models

example
-----------

```python
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
```
