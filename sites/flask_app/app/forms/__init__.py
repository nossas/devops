from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


class DomainForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(2, 23)])
    purchase_at = DateField("Comprando em")
    expired_at = DateField("Expira em")
    submit = SubmitField("Enviar")