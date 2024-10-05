from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class DomainForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(2, 23)])
    purchase_at = DateField("Comprando em")
    expired_at = DateField("Expira em")
    external_id = StringField("ID Externo")
    submit = SubmitField("Enviar")


DNS_RECORD_TYPES = [
    ('A', 'A - Endereço IPv4'),
    ('AAAA', 'AAAA - Endereço IPv6'),
    ('CNAME', 'CNAME - Nome Canônico'),
    ('MX', 'MX - Servidor de E-mail'),
    ('NS', 'NS - Servidor de Nomes'),
    ('PTR', 'PTR - Ponteiro Inverso'),
    ('SOA', 'SOA - Início da Autoridade'),
    ('SPF', 'SPF - Sender Policy Framework'),
    ('SRV', 'SRV - Serviço'),
    ('TXT', 'TXT - Texto'),
]

class RecordSetForm(FlaskForm):
    name = StringField("Nome", description="Use * para deixar vazio")
    record_type = SelectField("Tipo", choices=DNS_RECORD_TYPES)
    value = TextAreaField("Valor")
    submit = SubmitField("Enviar")