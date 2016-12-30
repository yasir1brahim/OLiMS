import sys
from dependencies.dependency import getToolByName
from dependencies.dependency import safe_unicode
from openerp.tools.translate import _
from openerp import fields, models
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.widget.widget import TextAreaWidget, BooleanWidget, StringWidget
from base_olims_model import BaseOLiMSModel
from lims.utils import t
schema = (StringField('SampleType',
              required=1,        
    ),
    TextField('Description',
              widget=TextAreaWidget(
                label=_('Description'),
                description=_('Used in item listings and search results.')),    
    ),
          
    fields.Char(string='Days', required=False),
    fields.Char(string='Hours', required=False),
    fields.Char(string='Minutes', required=False),    
      

    BooleanField('Hazardous',
        default = False,
        widget = BooleanWidget(
            label=_("Hazardous"),
            description=_("Samples of this type should be treated as hazardous"),
        ),
    ),
    fields.Many2one(string='Sample Matrix',
                    comodel_name='olims.sample_matrix',
        required = False,
    ),
    StringField('Prefix',
        required = True,
        widget = StringWidget(
            label=_("Sample Type Prefix"),
        ),
    ),
    StringField('Minimum Volume',
        required = 1,
        widget = StringWidget(
            label=_("Minimum Volume"),
            description=_("The minimum sample volume required for analysis eg. '10 ml' or '1 kg'."),
        ),
    ),
    fields.Many2one(string='Default Container',
        comodel_name='olims.container_type',
        required = False,
        help="The default container type. New sample partitions " + \
                "are automatically assigned a container of this " + \
                "type, unless it has been specified in more details " + \
                "per analysis service",
    ),

    fields.Many2many(string='Sample Points',
        required = False,
        comodel_name = 'olims.sample_point',
        help="The list of sample points from which this sample " + \
                            "type can be collected.  If no sample points are " + \
                            "selected, then all sample points are available."
    ),
    fields.Many2many(string="profile",
        comodel_name="olims.analysis_profile",
        ondelete="set null")

)

class SampleType(models.Model, BaseOLiMSModel):
    _name = 'olims.sample_type'
    _rec_name = 'SampleType'

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def Title(self):
        return safe_unicode(self.getField('title').get(self)).encode('utf-8')

    def getDefaultLifetime(self):
        """ get the default retention period """
        settings = getToolByName(self, 'bika_setup')
        return settings.getDefaultSampleLifetime()

    def SamplePointsVocabulary(self):
        from lims.content.samplepoint import SamplePoints
        return SamplePoints(self, allow_blank=False)

    def setSamplePoints(self, value, **kw):
        """ For the moment, we're manually trimming the sampletype<>samplepoint
            relation to be equal on both sides, here.
            It's done strangely, because it may be required to behave strangely.
        """
        bsc = getToolByName(self, 'bika_setup_catalog')
        ## convert value to objects
        if value and type(value) == str:
            value = [bsc(UID=value)[0].getObject(),]
        elif value and type(value) in (list, tuple) and type(value[0]) == str:
            value = [bsc(UID=uid)[0].getObject() for uid in value if uid]
        ## Find all SamplePoints that were removed
        existing = self.Schema()['SamplePoints'].get(self)
        removed = existing and [s for s in existing if s not in value] or []
        added = value and [s for s in value if s not in existing] or []
        ret = self.Schema()['SamplePoints'].set(self, value)

        for sp in removed:
            sampletypes = sp.getSampleTypes()
            if self in sampletypes:
                sampletypes.remove(self)
                sp.setSampleTypes(sampletypes)

        for sp in added:
            sp.setSampleTypes(list(sp.getSampleTypes()) + [self,])

        return ret

    def getSamplePoints(self, **kw):
        return self.Schema()['SamplePoints'].get(self)

    def SampleMatricesVocabulary(self):
        from lims.content.samplematrix import SampleMatrices
        return SampleMatrices(self, allow_blank=True)

    def ContainerTypesVocabulary(self):
        from lims.content.containertype import ContainerTypes
        return ContainerTypes(self, allow_blank=True)
SampleType.initialze(schema)
