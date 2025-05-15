from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class WebsiteLeadController(http.Controller):

    @http.route('/marca', type='http', auth='public', website=True)
    def render_formulario_en_homepage(self, **kwargs):
        brands = request.env['car.brand'].sudo().search([])
        return request.render('website.homepage_45cfdd', {
            'brands': brands,
        })

    @http.route('/website_lead/submit', type='http', auth='public', website=True, csrf=True)
    def website_lead_submit(self, **post):
        brand_id = int(post.get('brand_id'))
        _logger.info("📩 Formulario enviado. brand_id=%s", brand_id)

        request.env['crm.lead'].sudo().create({
            'name': 'Solicitud desde sitio web',
            'brand_id': brand_id,
        })
        return request.redirect('/thank-you')

    @http.route('/thank-you', type='http', auth='public', website=True)
    def website_thank_you(self, **kwargs):
        return request.render('stn_cotizador.website_thank_you_template')

    # 🔁 API JSON para modelos por marca
    @http.route('/api/models', type='json', auth='public')
    def get_models_by_brand(self):
        data = request.get_json_data()
        brand_id = data.get('brand_id')
        if not brand_id:
            return []
        models = request.env['car.model'].sudo().search([('brand_id', '=', int(brand_id))])
        return [{'id': m.id, 'name': m.name} for m in models]


    # 🔁 API JSON para año por modelo
    @http.route('/api/years', type='json', auth='public')
    def get_year_by_model(self, **kwargs):
        model_id = kwargs.get('model_id')
        if not model_id:
            return []
        model = request.env['car.model'].sudo().browse(int(model_id))
        if model.year_id:
            return [{'id': model.year_id.id, 'name': model.year_id.name}]
        return []

    # 🔁 API JSON para versiones por modelo
    @http.route('/api/versions', type='json', auth='public')
    def get_versions_by_model(self, **kwargs):
        model_id = kwargs.get('model_id')
        if not model_id:
            return []
        versions = request.env['car.version'].sudo().search([('model_id', '=', int(model_id))])
        return [{'id': v.id, 'name': v.name} for v in versions]
