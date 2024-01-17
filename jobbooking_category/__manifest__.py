#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': "Job Booking Categories",
    'version': '13.0.1.0.0',
    'summary': """By setting Category for Job types ,can auto fill fields based on it""",
    'description': """By setting Category for Job types ,can auto fill fields based on it.""",
    'category': 'Freight',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['scs_freight','hb_freight_extend','hb_freight_additional','web','base'],
    'data': [
        'views/category.xml',
        'security/ir.model.access.csv',
        'wizard/wizard.xml',
             ],
    'qweb': [],
    'license': "AGPL-3",
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}