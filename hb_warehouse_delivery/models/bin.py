from py3dbp import Packer, Bin, Item
from odoo import api, fields, models, _, SUPERUSER_ID


class StockPick(models.Model):
    _inherit = 'stock.picking'

    # def button_validate(self):
    #     res = super(StockPick, self).button_validate()
    #     for rec in self:
    #         if rec.state == 'done':
    #             locations = self.env['stock.location'].search(['occupied','<=',0])
    #             print(locations)
    #     return res

    def bin_alloc(self):
        packer = Packer()
        for rec in self:
            locs = []
            locations = self.env['stock.location'].search([('occupied_percent', '<=', 0)])
            print(locations)
            for loc in locations.x_pallet:
                locnam = {'name': loc.id, 'width': loc.width, 'height': loc.height, 'depth': loc.lngth,
                          'max_weight': loc.pack_weight}
                locs.append(locnam)
            print(locs)
            prods = []
            for prod in rec.move_ids_without_package:
                products = {'name': prod.id, 'width': prod.x_breadth, 'height': prod.x_height, 'depth': prod.x_length,
                            'weight': prod.x_weight}
                prods.append(products)
            print(prods)

            for i in locs:
                print('l')
                packer.add_bin(Bin(i['name'], i['width'], i['height'], i['depth'], i['max_weight']))

            for j in prods:
                packer.add_item(Item(j['name'], j['width'], j['height'], j['depth'], j['weight']))

            packer.pack(distribute_items=True, bigger_first=False)

            for b in packer.bins:
                print("--------------------------", b.string())

                print("FITTED ITEMS:")
                for item in b.items:
                    print("====> ", item.string())
                    pallet = b.string().split('(')[0]
                    move = item.string().split('(')[0]
                    location = self.env['stock.location'].search([('x_pallet', '=', pallet)])
                    line = self.env['stock.move'].search([('id', '=', move)])
                    print(line.move_line_ids, 'line.move_line_ids')
                    for move_lines in line.move_line_ids:
                        print(pallet, 'vanthyaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                        move_lines['result_package_id'] = int(pallet)
                        move_lines['allocated'] = True
                        # move_lines['location_dest_id'] = location
                        # move_lines['location_id'] = location
                        # m = self.env['stock.move.line'].search([('id','=',move_lines.id)])
                        # print(m.location_dest_id, 'm.location_dest_i')
                        # m.write({'result_package_id':pallet})
                        print(move_lines.result_package_id.name, 'move_lines.result_package_id')
                        # print(move_lines.result_package_id,'move_lines.result_package_id', move_lines.location_dest_id, 'move_lines.location_dest_i')

                    print(b.string().split('(')[0], item.string().split('(')[0],
                          '%%%%%555555555555555555555555555555555555555555555555555')

                # print("UNFITTED ITEMS:")
                # for item in b.unfitted_items:
                #     print("====> ", item.string())

#
# bin_data = [{'name': 'small-envelopee', 'width': 203.5, 'height': 12.5, 'depth': 5.5, 'max_weight': 10},
#             {'name': 'small-envelope2', 'width': 15.52, 'height': 1252, 'depth': 2.25, 'max_weight': 100}]
#
# item_data = [{'name': '50g [powder 1]', 'width': 3.9370, 'height': 1.968, 'depth': 1.9685, 'weight': 1},
#              {'name': '50g [powder 2]', 'width': 3.9370, 'height': 1.9685, 'depth': 1.9685, 'weight': 2},
#              {'name': '50g [powder 3]', 'width': 3.9370, 'height': 1.9685, 'depth': 1.9685, 'weight': 3},
#              {'name': '50g [powder 4]', 'width': 3.9370, 'height': 1.9685, 'depth': 1.9685, 'weight': 4},
#              {'name': '50g [powder 5]', 'width': 3.9370, 'height': 1.9685, 'depth': 1.9685, 'weight': 5},
#              {'name': '50g [powder 6]', 'width': 3.9370, 'height': 1.9685, 'depth': 1.9685, 'weight': 6},
#              {'name': '50g [powder 7]', 'width': 3.9370, 'height': 1.9685, 'depth': 1.9685, 'weight': 7},
#              {'name': '50g [powder 8]', 'width': 3.9370, 'height': 1.9685, 'depth': 1.9685, 'weight': 8}]
#
# for i in bin_data:
#     print('l')
#     packer.add_bin(Bin(i['name'], i['width'], i['height'], i['depth'], i['max_weight']))
#
# for j in item_data:
#     packer.add_item(Item(j['name'], j['width'], j['height'], j['depth'], j['weight']))
#
# # packer.add_bin(Bin('large-envelope', 15.0, 12.0, 0.75, 15))
# # packer.add_bin(Bin('small-box', 8.625, 5.375, 1.625, 70.0))
# # packer.add_bin(Bin('medium-box', 11.0, 8.5, 5.5, 70.0))
# # packer.add_bin(Bin('medium-2-box', 13.625, 11.875, 3.375, 70.0))
# # packer.add_bin(Bin('large-box', 12.0, 12.0, 5.5, 70.0))
# # packer.add_bin(Bin('large-2-box', 23.6875, 11.75, 3.0, 70.0))
#
# # packer.add_item(Item('50g [powder 1]', 3.9370, 1.9685, 1.9685, 1))
# # packer.add_item(Item('50g [powder 2]', 3.9370, 1.9685, 1.9685, 2))
# # packer.add_item(Item('50g [powder 3]', 3.9370, 1.9685, 1.9685, 3))
# # packer.add_item(Item('250g [powder 4]', 7.8740, 3.9370, 1.9685, 4))
# # packer.add_item(Item('250g [powder 5]', 7.8740, 3.9370, 1.9685, 5))
# # packer.add_item(Item('250g [powder 6]', 7.8740, 3.9370, 1.9685, 6))
# # packer.add_item(Item('250g [powder 7]', 7.8740, 3.9370, 1.9685, 7))
# # packer.add_item(Item('250g [powder 8]', 7.8740, 3.9370, 1.9685, 8))
# # packer.add_item(Item('250g [powder 9]', 7.8740, 3.9370, 1.9685, 9))
#
# packer.pack(distribute_items=True, bigger_first=False)
#
# for b in packer.bins:
#     print("--------------------------", b.string())
#
#     print("FITTED ITEMS:")
#     for item in b.items:
#         print("====> ", item.string())
#
#     print("UNFITTED ITEMS:")
#     for item in b.unfitted_items:
#         print("====> ", item.string())
