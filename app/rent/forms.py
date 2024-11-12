from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField


class CheckoutForm(FlaskForm):
    submit = SubmitField("Checkout")

class RestoreBasketForm(FlaskForm):
    submit = SubmitField("Clear basket")