import json
import logging
from odoo import http
from odoo.http import request
from werkzeug.exceptions import Forbidden
from http import HTTPStatus

_logger = logging.getLogger(__name__)

class WhatsAppWebhookDebug(http.Controller):

    @http.route('/whatsapp/webhook/', methods=['POST'], type="json", auth="public")
    def webhookpost(self):
        _logger.info("=== WhatsApp Webhook POST recibido ===")
        _logger.info("Headers: %s", dict(request.httprequest.headers))
        _logger.info("Raw data: %s", request.httprequest.data.decode())

        try:
            data = json.loads(request.httprequest.data)
            _logger.info("Datos JSON parseados: %s", data)
        except Exception as e:
            _logger.error("Error parseando JSON: %s", e)
            return {"error": "Invalid JSON"}

        # Busca la cuenta según id en entrada
        for entry in data.get('entry', []):
            account_id = entry.get('id')
            _logger.info("Procesando entry con account_id: %s", account_id)
            account = request.env['whatsapp.account'].sudo().search([('account_uid', '=', account_id)])

            if not account:
                _logger.warning("No se encontró cuenta whatsapp para account_id: %s", account_id)
                continue

            # Aquí podemos verificar la firma o saltarla para debugging
            signature = request.httprequest.headers.get('X-Hub-Signature-256')
            _logger.info("X-Hub-Signature-256: %s", signature)

            if not self._check_signature(account):
                _logger.warning("Firma no válida para account_id %s", account_id)
                raise Forbidden()

            # Loggear cambios para debugging
            changes = entry.get('changes', [])
            _logger.info("Cambios recibidos: %s", changes)

            # No replicamos lógica completa, solo debug
            # Puedes agregar aquí tu lógica o llamar métodos originales si tienes acceso

        return {"status": "ok", "message": "Webhook recibido y debug logueado"}

    @http.route('/whatsapp/webhook/', methods=['GET'], type="http", auth="public", csrf=False)
    def webhookget(self, **kwargs):
        _logger.info("=== WhatsApp Webhook GET recibido ===")
        _logger.info("Parámetros GET: %s", kwargs)

        token = kwargs.get('hub.verify_token')
        mode = kwargs.get('hub.mode')
        challenge = kwargs.get('hub.challenge')

        if not (token and mode and challenge):
            _logger.warning("Faltan parámetros para verificación")
            return Forbidden()

        wa_account = request.env['whatsapp.account'].sudo().search([('webhook_verify_token', '=', token)])

        if mode == 'subscribe' and wa_account:
            _logger.info("Verificación correcta para webhook, devolviendo challenge")
            response = request.make_response(challenge)
            response.status_code = HTTPStatus.OK
            return response

        _logger.warning("Token inválido o modo incorrecto para webhook")
        response = request.make_response({})
        response.status_code = HTTPStatus.FORBIDDEN
        return response

    def _check_signature(self, business_account):
        """Whatsapp firmará las peticiones, validamos la firma."""

        signature = request.httprequest.headers.get('X-Hub-Signature-256')
        if not signature or not signature.startswith('sha256=') or len(signature) != 71:
            _logger.warning('Encabezado de firma inválido: %r', signature)
            return False

        if not business_account.app_secret:
            _logger.warning('Falta app_secret para la cuenta, no se puede validar firma')
            return False

        import hmac
        import hashlib
        from odoo.tools import consteq

        expected = hmac.new(
            business_account.app_secret.encode(),
            msg=request.httprequest.data,
            digestmod=hashlib.sha256,
        ).hexdigest()

        if consteq(signature[7:], expected):
            _logger.info("Firma validada correctamente")
            return True
        else:
            _logger.warning("Firma no coincide")
            return False
