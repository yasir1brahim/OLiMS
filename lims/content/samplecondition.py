from OLiMS.dependencies.dependency import ClassSecurityInfo
from OLiMS.dependencies.dependency import BaseFolder
from OLiMS.dependencies.dependency import DisplayList
from OLiMS.dependencies.dependency import Schema
from OLiMS.dependencies.dependency import registerType
from OLiMS.dependencies.dependency import getToolByName
from OLiMS.lims.config import PROJECTNAME
from OLiMS.lims.content.bikaschema import BikaSchema

schema = BikaSchema.copy() + Schema((

))

schema['description'].schemata = 'default'
schema['description'].widget.visible = True


class SampleCondition(BaseFolder):
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from OLiMS.lims.idserver import renameAfterCreation
        renameAfterCreation(self)

registerType(SampleCondition, PROJECTNAME)


def SampleConditions(self, instance=None, allow_blank=False):
    instance = instance or self
    bsc = getToolByName(instance, 'bika_setup_catalog')
    items = []
    for sm in bsc(portal_type='SampleCondition',
                  inactive_state='active',
                  sort_on='sortable_title'):
        items.append((sm.UID, sm.Title))
    items = allow_blank and [['', '']] + list(items) or list(items)
    return DisplayList(items)