from dependencies.dependency import ClassSecurityInfo
from dependencies.dependency import InitializeClass
from dependencies.dependency import ManagePortal
from dependencies.dependency import getToolByName
from dependencies.dependency import CatalogTool
from dependencies.dependency import ZCatalog
from lims.interfaces import IBikaCatalog
from lims.interfaces import IBikaAnalysisCatalog
from lims.interfaces import IBikaSetupCatalog
from dependencies.dependency import implements


def getCatalog(instance, field='UID'):
    """ Return the catalog which indexes objects of instance's type.
    If an object is indexed by more than one catalog, the first match
    will be returned.
    """
    uid = instance.UID()
    if 'workflow_skiplist' in instance.REQUEST and \
        [x for x in instance.REQUEST['workflow_skiplist']
         if x.find(uid) > -1]:
        return None
    else:
        # grab the first catalog we are indexed in.
        # we're only indexed in one.
        at = getToolByName(instance, 'archetype_tool')
        plone = instance.portal_url.getPortalObject()
        catalog_name = instance.portal_type in at.catalog_map \
            and at.catalog_map[instance.portal_type][0] or 'portal_catalog'
        catalog = getToolByName(plone, catalog_name)
        return catalog


class BikaCatalog(CatalogTool):

    """Catalog for various transactional types"""

    implements(IBikaCatalog)

    security = ClassSecurityInfo()
    _properties = ({'id': 'title', 'type': 'string', 'mode': 'w'},)

    title = 'Bika Catalog'
    id = 'bika_catalog'
    portal_type = meta_type = 'BikaCatalog'
    plone_tool = 1

    def __init__(self):
        ZCatalog.__init__(self, self.id)

    security.declareProtected(ManagePortal, 'clearFindAndRebuild')

    def clearFindAndRebuild(self):
        """
        """

        def indexObject(obj, path):
            self.reindexObject(obj)

        at = getToolByName(self, 'archetype_tool')
        types = [k for k, v in at.catalog_map.items()
                 if self.id in v]

        self.manage_catalogClear()
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal.ZopeFindAndApply(portal,
                                obj_metatypes=types,
                                search_sub=True,
                                apply_func=indexObject)

InitializeClass(BikaCatalog)


class BikaAnalysisCatalog(CatalogTool):

    """Catalog for analysis types"""

    implements(IBikaAnalysisCatalog)

    security = ClassSecurityInfo()
    _properties = ({'id': 'title', 'type': 'string', 'mode': 'w'},)

    title = 'Bika Analysis Catalog'
    id = 'bika_analysis_catalog'
    portal_type = meta_type = 'BikaAnalysisCatalog'
    plone_tool = 1

    def __init__(self):
        ZCatalog.__init__(self, self.id)

    security.declareProtected(ManagePortal, 'clearFindAndRebuild')

    def clearFindAndRebuild(self):
        """
        """

        def indexObject(obj, path):
            self.reindexObject(obj)

        at = getToolByName(self, 'archetype_tool')
        types = [k for k, v in at.catalog_map.items()
                 if self.id in v]

        self.manage_catalogClear()
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal.ZopeFindAndApply(portal,
                                obj_metatypes=types,
                                search_sub=True,
                                apply_func=indexObject)

InitializeClass(BikaAnalysisCatalog)


class BikaSetupCatalog(CatalogTool):

    """Catalog for all bika_setup objects"""

    implements(IBikaSetupCatalog)

    security = ClassSecurityInfo()
    _properties = ({'id': 'title', 'type': 'string', 'mode': 'w'},)

    title = 'Bika Setup Catalog'
    id = 'bika_setup_catalog'
    portal_type = meta_type = 'BikaSetupCatalog'
    plone_tool = 1

    def __init__(self):
        ZCatalog.__init__(self, self.id)

    security.declareProtected(ManagePortal, 'clearFindAndRebuild')

    def clearFindAndRebuild(self):
        """
        """

        def indexObject(obj, path):
            self.reindexObject(obj)

        at = getToolByName(self, 'archetype_tool')
        types = [k for k, v in at.catalog_map.items()
                 if self.id in v]

        self.manage_catalogClear()
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal.ZopeFindAndApply(portal,
                                obj_metatypes=types,
                                search_sub=True,
                                apply_func=indexObject)

InitializeClass(BikaSetupCatalog)
