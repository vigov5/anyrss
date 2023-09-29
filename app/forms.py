from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms_alchemy import model_form_factory

ModelForm = model_form_factory(Form)


class TestForm(Form):
    url = StringField('URL', [
        DataRequired('Please enter URL'),
    ])
    config = TextAreaField('Config', [
        DataRequired('Please your config in YAML'),
    ])
    submit = SubmitField('Check !')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        return True
    
class DebugForm(Form):
    url = StringField('URL', [
        DataRequired('Please enter URL'),
    ])

    submit = SubmitField('Fetch !')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        return True