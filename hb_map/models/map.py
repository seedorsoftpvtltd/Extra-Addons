import urllib
from odoo import fields, models, api, _

try:
    from urlparse import urljoin
    from urllib2 import urlopen
except ImportError:
    # Python 3
    from urllib.parse import urljoin
    from urllib.request import urlopen


# class GetProducts(models.Model):
#     _inherit = 'product.product'
#
#     def get_products(self):
#         pro = self.env['product.product'].search([])
#         products = []
#         for rec in pro:
#             print(rec)
#             print(rec.image_1920)
#             products.append(
#                 [rec.id,
#                  rec.image_1920
#                  ]
#             )
#
#         return products


class map(models.Model):
    _inherit = 'res.users'

    def track_loc(self):
        url = 'http://eiuat.seedors.com:8001/seedor-api/path-history/%s?clientid=%s' % (self.id, self.env.cr.dbname)
#        url = 'http://eiuat.seedors.com:8001/seedor-api/path-history/9?clientid=bookseedorpremiumuat'
        print(url)
        return {
            'type': 'ir.actions.act_url',
            'name': "Track Location",
            'url': url,
            'target': 'self',
            'context': self._context,
        }

#     def map(self):
#         print('hhhhhhhhhhhhhhhh')
#         return """<html>
#
# <head>
# 	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
# 	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
# 	<title>Google Maps - gmplot</title>
# 	<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization"></script>
# 	<script type="text/javascript">
# 		function initialize() {
#         var map = new google.maps.Map(document.getElementById("map_canvas"), {
#             zoom: 14,
#             center: new google.maps.LatLng(8.176365, 77.431527)
#         });
#
#         var marker_icon_FF0000 = {
#             url: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAiCAYAAACwaJKDAAAABmJLR0QA/wD/AP+gvaeTAAACBklEQVRIia3VzUtUURgH4GdG/AiyZZShtWgXUbSIFtGqRYtqWRLhXyBYf0K6MaJQ2gRtayHtijYpleHKSCgIcRHoIiOSKEzLKea0OOeqTfPlzPzg5Qwz9zz3nXPvPTeneo7gNA4gjyI+Ygbva8z9L2cxi9BHOE+4msY+gliz6biayWE0R7GfMEcoEkJJzRH6CbnY+WiaVxEc6yY8KQOVq8eE7tj1WCV4qIswUyeY1QyhK8JDpWAP1m7vEMzqTkTXkrOZkYOEQoNogXAowiPE2wQuDqC9nktZJu0YSE72XRs2phrsMqup2OkG2vLpRB19DXaZJc3vQHv294Um0e3z8yigsNQkmuYXUMie5/npJtE0fz55YLiXsNHELdUbV2B4+4n2Y/Vmg+itCK4m558MdhBe7hCcJnRGdLDS0ox3E17XCb4h7IngeLX1zuFhD2G5BriytY4Tqmx9WXbh3Tnl99KsLkdwAbtrgVmO4/eDCuCkzd3/TL1glru9hF8lYJFwMoKPdgrCXqzfL0GfR7CIo42gcO9YCXopolONgnAC4W0Cv9l8dVxpBoWFGwmdiOC6Glc8X+3HlKeT6cOzOLzAjyaaBBc602ZzOHZ6vVkQ9kl7Qi6ip1qBwpdrEfwjPnFVU8+awuKrOC7hZ6vQlQ9baM3Ui379HsfVVqKf07jcSvRTGhfrOfgvIP3ECS77BDoAAAAASUVORK5CYII=",
#             labelOrigin: new google.maps.Point(10, 11)
#         };
#
#         new google.maps.Marker({
#             position: new google.maps.LatLng(8.176365, 77.431527),
#             title: "Source",
#             icon: marker_icon_FF0000,
#             map: map
#         });
#
#         new google.maps.Marker({
#             position: new google.maps.LatLng(8.176365, 77.431524),
#             title: "Source",
#             icon: marker_icon_FF0000,
#             map: map
#         });
#
#         new google.maps.Polyline({
#             clickable: false,
#             geodesic: true,
#             strokeColor: "#6495ED",
#             strokeOpacity: 1.000000,
#             strokeWeight: 10,
#             map: map,
#             path: [
#                 new google.maps.LatLng(8.176365, 77.431527),
#                 new google.maps.LatLng(8.176364, 77.431523),
#                 new google.maps.LatLng(8.176365, 77.431524),
#                 new google.maps.LatLng(8.176357, 77.431529),
#                 new google.maps.LatLng(8.176365, 77.431527),
#                 new google.maps.LatLng(8.176364, 77.431523),
#                 new google.maps.LatLng(8.176365, 77.431524),
#                 new google.maps.LatLng(8.176357, 77.431529),
#                 new google.maps.LatLng(8.176365, 77.431527),
#                 new google.maps.LatLng(8.176364, 77.431523),
#                 new google.maps.LatLng(8.176365, 77.431524),
#                 new google.maps.LatLng(8.176350, 77.431525),
#                 new google.maps.LatLng(8.176357, 77.431529),
#                 new google.maps.LatLng(8.176365, 77.431527),
#                 new google.maps.LatLng(8.176364, 77.431523),
#                 new google.maps.LatLng(8.176365, 77.431524),
#             ]
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763655, 77.4315269),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763643, 77.4315231),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763647, 77.4315244),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763571, 77.4315294),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763655, 77.4315269),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763643, 77.4315231),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763647, 77.4315244),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763571, 77.4315294),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763655, 77.4315269),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763643, 77.4315231),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763647, 77.4315244),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763496, 77.4315246),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763571, 77.4315294),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763655, 77.4315269),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763643, 77.4315231),
#             radius: 40
#         });
#
#         new google.maps.Circle({
#             strokeColor: '#3B0B39',
#             strokeOpacity: 1.0,
#             strokeWeight: 1,
#             fillColor: '#3B0B39',
#             fillOpacity: 0.3,
#             map: map,
#             center: new google.maps.LatLng(8.1763647, 77.4315244),
#             radius: 40
#         });
#
#     }
# 	</script>
# </head>
#
# <body style="margin:0px; padding:0px;" onload="initialize()">
# 	<div id="map_canvas" style="width: 100%; height: 100%;" />
# </body>
#
# </html>"""
