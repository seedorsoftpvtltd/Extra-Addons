from py3dbp import Packer, Bin, Item
from odoo import api, fields, models, _, SUPERUSER_ID
import ast



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

        for rec in self:
            locs = []
            locations = self.env['stock.location'].search([('occupied_percent', '<=', 0)])
            # print(locations)
            for loc in locations.x_pallet:
                locnam = {'name': loc.id, 'width': loc.width, 'height': loc.height, 'depth': loc.lngth,
                          'max_weight': loc.pack_weight}
                locs.append(locnam)
            # print(locs,'locs')

            for prod in rec.move_ids_without_package:
                # move_lines = prod.move_id
                print(prod.move_line_ids, '******************************************')

                for ml in prod.move_line_ids:
                    if ml:
                        ml.unlink()
                print(prod.move_line_ids, '%%%%%%%%%%%%55555')
                id = prod.id
                pick_id = prod.picking_id
                packer = Packer()
                print(prod,'###################################################')
                qty = int(prod.product_uom_qty)
                print(qty, 'qtyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')# quanity varanum...................................
                prods = []
                # print(qty,'atyttttttttttttttttttttttttttttt')
                for ompk in range(0, qty):
                    # print(ompk, '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                    products = {'name': prod.id, 'width': prod.x_breadth, 'height': prod.x_height,
                                'depth': prod.x_length,

                                'weight': prod.x_weight}

                    prods.append(products)
                    # print(prods,'prodsssssssssssssssssssssssssssssssss')
                for i in locs:
                    # print('l')
                    packer.add_bin(Bin(i['name'], i['width'], i['height'], i['depth'], i['max_weight']))

                for j in prods:
                    # print(j,'j++++++++++++++++++++++++++++++=')
                    packer.add_item(Item(j['name'], j['width'], j['height'], j['depth'], j['weight']))

                packer.pack(distribute_items=True, bigger_first=False)

                buno = []
                for b in packer.bins:
                    print("--------------------------", b.string())
                    print("FITTED ITEMS:")
                    print(b,'b')
                    print(b.items, 'b.items')
                    if b.items == []:
                        continue
                    textpack = []
                    pack1 = []
                    finalpack = []
                    qty = 0
                    # print("UNFITTED ITEMS:")
                    # for item in b.unfitted_items:
                    #     print("====> ", item.string())

                    for item in b.items:
                        # print("FITTED ITEMS")
                        pallet = b.string().split('(')[0]
                        move = item.string().split('(')[0]
                        qt = 0
                        pack1.append(pallet)
                        pack1.append(move)
                        pack1.append(qt)
                        # print(pack1, 'pack11111111111111111111111')
                        textpack.append(str(pack1))
                        finalpack.append((pack1))
                        pack1 = []
                    # print(textpack,'textpack')
                    # print(set(textpack))
                    j = str(set(textpack)).replace('{', '[').replace('}', ']')
                    # print(j,'jjjjjjjjjjjjjjjjjjjjjjjjjjjj')
                    textpack = ast.literal_eval(j)
                    for i in range(0, len(set(textpack))):
                        for j in range(0, len(finalpack)):
                            # print(str(textpack[i]), 'compare WIth', finalpack[j])
                            if str(textpack[i]) == str(finalpack[j]):
                                # print('in')
                                qty = qty + 1
                        # print(qty)
                        textpack[i] = ast.literal_eval(textpack[i])
                        textpack[i][2] = qty
                        qty = 0
                    # print(textpack)
                    buno = textpack
                print(buno, '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
                mov_line = prod.move_line_ids
                print(mov_line, '(((((((((((((((((((((((((((((((((((((((((((((((99999')

                for i in buno:
                    print(i,'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii', i[1], i[2], i[0])
                    location = self.env['stock.location'].search([('x_pallet', '=', int(i[0]))])[0]
                    vals ={
                        'move_id': int(i[1]),
                        'picking_id': prod.picking_id.id,
                        'product_id': prod.product_id.id,
                        'location_id': prod.location_id.id,
                        'location_dest_id': location.id,
                        'result_package_id':int(i[0]),
                        'product_uom_qty': int(i[2]),
                        'product_uom_id': prod.product_uom.id,
                        'qty_done': int(i[2]),
                        'allocated': True
                    }
                    moveline = self.env['stock.move.line'].create(vals)
                    print(moveline, 'movelineeeeeeeeeeeeeeeeeeeeeeeee')















                # print(len(buno), 'length of items')
                # length = len(buno)
                # print('LLLLLLLLLLLLLLLLLLLLLLLLLLLLL', id, 'id', pick_id, 'picking id')
                # line = self.env['stock.move.line'].search([('move_id', '=', id)])
                # print(len(line), 'length of move lines')
                # helo = len(line)
                # for h in line:
                #     print('hellooooo', h)
                #     if helo <= length:
                #         for l in range(0, length):
                #             if helo != length:
                #                 helo = helo + 1
                #                 h.copy()
                #                 h.update({'move_id', '=', id})
                #                 print(h, 'lineeeeeeee', helo)
                #
                # lines = self.env['stock.move.line'].search([('move_id', '=', id)]).id
                # print(len(lines), lines, 'lines')


                # for b in buno:
                #     # print(b, 'bbbbbbbbbbb', rec)
                #     for bb in b:
                #         print(bb[0], 'bb', bb[1], bb[2])
                #         pack = bb[0]
                #         move = bb[1]
                #         qty = bb[2]

        #         print("====> ", item.string())
            #         pallet = b.string().split('(')[0]
            #         move = item.string().split('(')[0]
            #         pack1.append(pallet)
            #         pack1.append(move)
            #         pack1.append(qty)
            #         textpack.append(pack1)
            #
            #
            # print(textpack)

            # for b in packer.bins:
            #     print("--------------------------", b.string())
            #
            #     print("FITTED ITEMS:")
            #     for item in b.items:
            #         print("====> ", item.string())
            #         pallet = b.string().split('(')[0]
            #         move = item.string().split('(')[0]
            #         print(pallet, 'pallet')
            #         print(move, 'move')
            #         location = self.env['stock.location'].search([('x_pallet', '=', pallet)])
            #         line = self.env['stock.move'].search([('id', '=', move)])
            #         print(line.move_line_ids, 'line.move_line_ids')
            #         for move_lines in line.move_line_ids:
            #             print(pallet, 'vanthyaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            #             move_lines['result_package_id'] = int(pallet)
            #             move_lines['allocated'] = True
            #             # move_lines['location_dest_id'] = location
            #             # move_lines['location_id'] = location
            #             # m = self.env['stock.move.line'].search([('id','=',move_lines.id)])
            #             # print(m.location_dest_id, 'm.location_dest_i')
            #             # m.write({'result_package_id':pallet})
            #             print(move_lines.result_package_id.name, 'move_lines.result_package_id')
            #             # print(move_lines.result_package_id,'move_lines.result_package_id', move_lines.location_dest_id, 'move_lines.location_dest_i')
            #
            #         print(b.string().split('(')[0], item.string().split('(')[0],
            #               '%%%%%555555555555555555555555555555555555555555555555555')
            #
            #     # print("UNFITTED ITEMS:")
            #     # for item in b.unfitted_items:
            #     #     print("====> ", item.string())

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
