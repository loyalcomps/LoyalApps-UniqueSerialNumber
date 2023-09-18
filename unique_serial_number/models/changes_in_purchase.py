from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CustomStockMove(models.Model):
    _inherit = 'stock.move.line'

    lot_name = fields.Char('Lot/Serial Number')

    @api.onchange('lot_name')
    def _on_change_lot_name(self):
        if self.lot_name:
            existing_lots = self.env['stock.move.line'].search([
                ('lot_name', '=', self.lot_name),
                ('id', '!=', self._origin.id)  # Exclude the current record
            ])
            if existing_lots:
                product_names = ', '.join(existing_lots.mapped('product_id.display_name'))
                self.lot_name = None  # Clear the entered lot_name to avoid duplication
                return {
                    'warning': {
                        'title': 'Duplicate Serial Number',
                        'message': f'The given Serial number already exists for product(s): {product_names}. Please enter a different serial number.'
                    }
                }
