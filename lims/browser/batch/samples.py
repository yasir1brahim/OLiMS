from lims.browser.sample import SamplesView as _SV
from lims.permissions import *
from dependencies.dependency import getToolByName
from dependencies.dependency import implements
from dependencies.dependency import safe_unicode



class SamplesView(_SV):

    def __init__(self, context, request):
        super(SamplesView, self).__init__(context, request)
        self.view_url = self.context.absolute_url() + "/samples"
        if 'path' in self.contentFilter:
            del(self.contentFilter['path'])

    def contentsMethod(self, contentFilter):
        tool = getToolByName(self.context, self.catalog)
        state = [x for x in self.review_states if x['id'] == self.review_state['id']][0]
        for k, v in state['contentFilter'].items():
            self.contentFilter[k] = v
        tool_samples = tool(contentFilter)
        samples = {}
        for sample in (p.getObject() for p in tool_samples):
            for ar in sample.getAnalysisRequests():
                batch = ar.getBatch()
                if batch and ar.getBatch().UID() == self.context.UID():
                        samples[sample.getId()] = sample
        return samples.values()
