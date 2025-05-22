from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    codigo_postal = fields.Char(string="Codigo Postal")
    brand_id = fields.Many2one('car.brand', string='Marca')
    model_id = fields.Many2one('car.model', string='Modelo')
    year_id = fields.Many2one('car.year', string='Año')
    version_id = fields.Many2one('car.version', string='Versión')

    @api.onchange('brand_id')
    def _onchange_brand(self):
        self.model_id = False
        self.year_id = False
        self.version_id = False
        domain_model = [('brand_id', '=', self.brand_id.id)] if self.brand_id else []
        print(f"🔁 Marca seleccionada: {self.brand_id.name if self.brand_id else 'None'}")
        print(f"📦 Dominio modelos: {domain_model}")
        return {
            'domain': {
                'model_id': domain_model,
                'year_id': [],  # Año depende del modelo ahora
                'version_id': [],
            }
        }

    @api.onchange('model_id')
    def _onchange_model(self):
        self.year_id = self.model_id.year_id.id if self.model_id else False
        self.version_id = False
        domain = [('id', '=', self.model_id.year_id.id)] if self.model_id and self.model_id.year_id else []
        print(f"🔁 Modelo seleccionado: {self.model_id.name if self.model_id else 'None'}")
        print(f"📦 Dominio años: {domain}")
        return {'domain': {'year_id': domain}}

    @api.onchange('year_id')
    def _onchange_year(self):
        self.version_id = False
        domain_version = [('model_id', '=', self.model_id.id)] if self.model_id else []
        print(f"🔁 Año seleccionado: {self.year_id.name if self.year_id else 'None'}")
        print(f"📦 Dominio versiones: {domain_version}")
        return {
            'domain': {
                'version_id': domain_version
            }
        }