# from odoo import http


# class UtilityPyments(http.Controller):
#     @http.route('/utility_pyments/utility_pyments', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/utility_pyments/utility_pyments/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('utility_pyments.listing', {
#             'root': '/utility_pyments/utility_pyments',
#             'objects': http.request.env['utility_pyments.utility_pyments'].search([]),
#         })

#     @http.route('/utility_pyments/utility_pyments/objects/<model("utility_pyments.utility_pyments"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('utility_pyments.object', {
#             'object': obj
#         })
