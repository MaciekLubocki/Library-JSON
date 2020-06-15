from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    media = SelectField('Media', choices=[('Book','Book'), ('Audio CD', 'Audio CD'), ('DVD', 'DVD')])
    title = StringField('Item title', validators=[DataRequired()])
    author = StringField('Author')
    year = StringField('Year')
    