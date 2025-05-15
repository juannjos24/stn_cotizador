from odoo import models, fields,api

class CarVersion(models.Model):
    _name = 'car.version'
    _description = 'Versión'

    name = fields.Char(string='Versión', required=True)
    model_id = fields.Many2one('car.model', string='Modelo', required=True)
    #year_id = fields.Many2one(related='model_id.year_id', comodel_name='car.year', string='Año (del Modelo)', store=True, readonly=True)
    year_id = fields.Many2one('car.year', string='Año(M)', required=True)
