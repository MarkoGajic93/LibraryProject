from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length


class NewAuthorForm(FlaskForm):
    name = StringField("Name",
                        validators=[InputRequired("Input is required!"),
                                    DataRequired("Data is required!")])

    biography = TextAreaField("Biography",
                              validators=[Length(max=200, message="Biography must be maximum 00 characters long")])

    submit = SubmitField("Add author")

