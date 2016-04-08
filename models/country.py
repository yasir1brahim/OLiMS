from openerp import fields, models,osv
from base_olims_model import BaseOLiMSModel

schema = (
          fields.Char(string='name', required=True),
          fields.Char(string='id', required=False),
          fields.Char(string='Area', required=False),
          fields.Char(string='Capital', required=False),
          fields.Char(string='Continent', required=False),
          fields.Char(string='CurrencyCode', required=False),
          fields.Char(string='CurrencyName', required=False),
          fields.Char(string='EquivalentFipsCode', required=False),
          fields.Char(string='ISO-Numeric', required=False),
          fields.Char(string='ISO3', required=False),
          fields.Char(string='Languages', required=False),
          fields.Char(string='Phone', required=False),
          fields.Char(string='Population', required=False),
          fields.Char(string='PostalCodeFormat', required=False),
          fields.Char(string='PostalCodeRegex', required=False),
          fields.Char(string='fips', required=False),
          fields.Char(string='geonameid', required=False),
          fields.Char(string='neighbours', required=False),
          fields.Char(string='tld', required=False),
          )

class Country(models.Model, BaseOLiMSModel):
    _name='olims.country'
    
Country.initialze(schema)
