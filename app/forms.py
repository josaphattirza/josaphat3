from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class FinderForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    # submit = SubmitField('Sign In')

    username = StringField('ID of Books', validators=[DataRequired()])
    submit = SubmitField('Find')