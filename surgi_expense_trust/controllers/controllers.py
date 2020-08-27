# -*- coding: utf-8 -*-
# from odoo import http


# class SurgiExpenseTrust(http.Controller):
#     @http.route('/surgi_expense_trust/surgi_expense_trust/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_expense_trust/surgi_expense_trust/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_expense_trust.listing', {
#             'root': '/surgi_expense_trust/surgi_expense_trust',
#             'objects': http.request.env['surgi_expense_trust.surgi_expense_trust'].search([]),
#         })

#     @http.route('/surgi_expense_trust/surgi_expense_trust/objects/<model("surgi_expense_trust.surgi_expense_trust"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_expense_trust.object', {
#             'object': obj
#         })
