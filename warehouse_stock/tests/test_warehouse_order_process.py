from .common import Testwarehouse


class TestwarehouseOrderProcess(Testwarehouse):

    def test_00_cancel_warehouse_order_flow(self):
        """ Test cancel warehouse order with group user."""

        # In order to test the cancel flow,start it from canceling confirmed warehouse order.
        po_edit_with_user = self.env.ref('warehouse.warehouse_order_5').with_user(self.res_users_warehouse_user)

        # Confirm the warehouse order.
        po_edit_with_user.button_confirm()

        # Check the "Approved" status  after confirmed Booking.
        self.assertEqual(po_edit_with_user.state, 'warehouse', 'warehouse: PO state should be "warehouse')

        # First cancel receptions related to this order if order shipped.
        po_edit_with_user.picking_ids.action_cancel()

        # Able to cancel warehouse order.
        po_edit_with_user.button_cancel()

        # Check that order is cancelled.
        self.assertEqual(po_edit_with_user.state, 'cancel', 'warehouse: PO state should be "Cancel')
