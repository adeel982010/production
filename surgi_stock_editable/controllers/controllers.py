# -*- coding: utf-8 -*-
# from odoo import http


# class SurgiStockEditable(http.Controller):
#     @http.route('/surgi_stock_editable/surgi_stock_editable/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_stock_editable/surgi_stock_editable/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_stock_editable.listing', {
#             'root': '/surgi_stock_editable/surgi_stock_editable',
#             'objects': http.request.env['surgi_stock_editable.surgi_stock_editable'].search([]),
#         })

#     @http.route('/surgi_stock_editable/surgi_stock_editable/objects/<model("surgi_stock_editable.surgi_stock_editable"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_stock_editable.object', {
#             'object': obj
#         })
