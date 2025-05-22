
from odoo import api, models,fields

class CarBrandYear(models.Model):
    _name = 'car.brand.year'
    _description = 'Relación Marca - Año'

    brand_id = fields.Many2one('car.brand', string='Marca', required=True)
    year_id = fields.Many2one('car.year', string='Año', required=True)