from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class WebsiteLeadController(http.Controller):

    # 🏠 Página principal
    @http.route('/marca', type='http', auth='public', website=True)
    def render_formulario_en_homepage(self, **kwargs):
        brands = request.env['car.brand'].sudo().search([])
        return request.render('website.homepage_45cfdd', {
            'brands': brands,
        })

    # ✅ Guardar formulario
    @http.route('/website_lead/submit', type='http', auth='public', website=True, csrf=True)
    def website_lead_submit(self, **post):
        brand_id = int(post.get('brand_id', 0))
        model_id = int(post.get('model_id', 0))
        year_id = int(post.get('year_id', 0))
        version_id = int(post.get('version_id', 0))

        _logger.info("📩 Formulario enviado: brand_id=%s, year_id=%s, model_id=%s, version_id=%s",
                     brand_id, year_id, model_id, version_id)

        request.env['crm.lead'].sudo().create({
            'name': 'Solicitud desde sitio web',
            'brand_id': brand_id,
            'year_id': year_id,
            'model_id': model_id,
            'version_id': version_id,
        })

        return request.redirect('/thank-you')

    # ✅ Página de gracias
    @http.route('/thank-you', type='http', auth='public', website=True)
    def website_thank_you(self, **kwargs):
        return request.render('stn_cotizador.website_thank_you_template')

    # 🔁 API: Años disponibles para una marca
    @http.route('/api/brand-years', type='json', auth='public')
    def get_years_by_brand(self):
        data = request.get_json_data()
        brand_id = data.get('brand_id')

        if not brand_id:
            return []

        # Buscar años únicos usados por modelos de esta marca
        models = request.env['car.model'].sudo().search([
            ('brand_id', '=', int(brand_id)),
            ('year_id', '!=', False)
        ])
        year_ids = list(set(models.mapped('year_id.id')))
        years = request.env['car.year'].sudo().browse(year_ids)

        return [{'id': y.id, 'name': y.name} for y in years]

    # 🔁 API: Modelos por marca + año
    @http.route('/api/models-by-brand-year', type='json', auth='public')
    def get_models_by_brand_and_year(self):
        data = request.get_json_data()
        brand_id = data.get('brand_id')
        year_id = data.get('year_id')

        if not (brand_id and year_id):
            return []

        models = request.env['car.model'].sudo().search([
            ('brand_id', '=', int(brand_id)),
            ('year_id', '=', int(year_id))
        ])
        return [{'id': m.id, 'name': m.name} for m in models]

    # 🔁 API: Versiones por modelo
    @http.route('/api/versions', type='json', auth='public')
    def get_versions_by_model(self):
        data = request.get_json_data()
        model_id = data.get('model_id')
        if not model_id:
            return []

        versions = request.env['car.version'].sudo().search([
            ('model_id', '=', int(model_id))
        ])
        return [{'id': v.id, 'name': v.name} for v in versions]
