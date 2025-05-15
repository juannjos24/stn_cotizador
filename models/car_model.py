from odoo import models, fields, api

class CarModel(models.Model):
    _name = 'car.model'
    _description = 'Modelo'

    name = fields.Char(string='Modelo', required=True)
    brand_id = fields.Many2one('car.brand', string='Marca', required=True)
    year_id = fields.Many2one('car.year', string='Año', required=True)

    # En car.model
    def name_get(self):
        result = []
        for record in self:
            year = record.year_id.name or ''
            name_display = f"{record.name} ({year})"
            result.append((record.id, name_display))
        return result
