from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class WebsiteLeadController(http.Controller):

    # 🏠 Página principal
    # En tu controlador
    @http.route('/marca', type='http', auth='public', website=True)
    def render_formulario_en_homepage(self, **kwargs):
        brands = request.env['car.brand'].sudo().search([])
        # Pasas una variable que indique si mostrar form o gracias
        show_form = True
        if request.httprequest.path == '/thank-you' or request.params.get('success') == '1':
            show_form = False

        return request.render('website.homepage_45cfdd', {
            'brands': brands,
            'show_form': show_form,
        })

    # ✅ Guardar formulario
    @http.route('/website_lead/submit', type='http', auth='public', website=True, csrf=True)
    def website_lead_submit(self, **post):
        brand_id = int(post.get('brand_id', 0))
        model_id = int(post.get('model_id', 0))
        year_id = int(post.get('year_id', 0))
        version_id = int(post.get('version_id', 0))

        customer_name = post.get('customer_name', '').strip()
        phone = post.get('phone', '').strip()
        email = post.get('email', '').strip()

        _logger.info("📩 Nuevo lead recibido con nombre=%s, teléfono=%s, email=%s", customer_name, phone, email)

        request.env['crm.lead'].sudo().create({
            'name': f'Oportunidad de cotización - {customer_name}',
            'contact_name': customer_name,
            'phone': phone,
            'email_from': email,
            'brand_id': brand_id,
            'year_id': year_id,
            'model_id': model_id,
            'version_id': version_id,
        })
        return request.redirect('/thank-you')

    # ✅ Página de gracias
    @http.route('/thank-you', type='http', auth='public', website=True)
    def website_thank_you(self, **kwargs):
        return request.render('website.homepage_45cfdd')    

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

        # Usamos un diccionario para filtrar por nombre (o puedes usar ID si lo prefieres)
        unique_models = {}
        for model in models:
            if model.name not in unique_models:
                unique_models[model.name] = model

        return [{'id': m.id, 'name': m.name} for m in unique_models.values()]
        
    # 🔁 API: Versiones por modelo (usando IDs)
    @http.route('/api/versions', type='json', auth='public', csrf=False)
    def get_versions(self):
        data = request.get_json_data()
        model_name = data.get('model_name')  # Cambiamos a recibir el nombre en lugar del ID
        year_id = data.get('year_id')

        _logger.info("📥 [API] Request a /api/versions con model_name=%s, year_id=%s", model_name, year_id)

        if not (model_name and year_id):
            return {'jsonrpc': '2.0', 'id': None, 'result': []}

        # Buscar versiones donde el nombre del modelo coincida y el año sea el correcto
        versions = request.env['car.version'].sudo().search([
            ('model_id.name', '=', model_name),
            ('year_id', '=', int(year_id))
        ])

        _logger.info("📤 [API] Versiones encontradas: %s", versions)

        return {
            'jsonrpc': '2.0',
            'id': None,
            'result': [{'id': v.id, 'name': v.name} for v in versions]
        }