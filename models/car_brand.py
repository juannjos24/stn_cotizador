from odoo import models, fields, api

class CarBrand(models.Model):
    _name = 'car.brand'
    _description = 'Marca'
    
    active=fields.Boolean(default=True, help="")
    name = fields.Char(string='Nombre de la Marca', required=True)