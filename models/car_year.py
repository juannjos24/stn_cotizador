from odoo import models, fields,api

class CarYear(models.Model):
    _name = 'car.year'
    _description = 'Año'

    name = fields.Char(string='Año', required=True)
    #brand_id = fields.Many2one('car.brand', string="Marca", required=True)  # 👈 NECESARIO para el dominio