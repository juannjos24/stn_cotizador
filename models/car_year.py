from odoo import models, fields,api

class CarYear(models.Model):
    _name = 'car.year'
    _description = 'Año'

    name = fields.Char(string='Año', required=True)    