from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

from ..extensions import bonde_api


class DomainForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(2, 23)])
    purchase_at = DateField("Comprando em")
    expired_at = DateField("Expira em")
    has_manage_dns = BooleanField("Tem gerenciamento de DNS?", default=True)


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


class EtcdKeyValueForm(FlaskForm):
    key = StringField("Chave")
    value = StringField("Valor")
    submit = SubmitField("Enviar")


class SiteForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(2, 23)])
    community_id = SelectField("Comunidade")

    def __init__(self):
        super().__init__()

        self.community_id.choices = bonde_api.get_communities()