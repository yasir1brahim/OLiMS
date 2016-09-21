from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.reference_field import ReferenceField
from fields.widget.widget import TextAreaWidget
from fields.widget.widget import StringWidget
from fields.file_field import FileField
from fields.widget.widget import FileWidget
from openerp.tools.translate import _
AR_STATES = (
    ('sample_registered','Sample Registered'),
    ('not_requested','Not Requested'),
    ('to_be_sampled','To Be Sampled'),
    ('sampled','Sampled'),
    ('to_be_preserved','To Be Preserved'),
    ('sample_due','Sample Due'),
    ('sample_received','Received'),
    ('attachment_due','Attachment Outstanding'),
    ('to_be_verified','To be verified'),
    ('verified','Verified'),
    ('published','Published'),
    ('invalid','Invalid'),
    )
WORKSHEET_STATES = (
    ('open','open'),
    ('attachment_due','Attachment Outstanding'),
    ('to_be_verified','To be verified'),
    ('verified','Verified'),
    ('rejected','Rejected'),
    )
schema = (StringField(string='Worksheet',compute='_ComputeWorksheetId'),
    fields.Many2one(string='Template',
                   comodel_name='olims.worksheet_template',
                   required=False,

            ),
    fields.Many2one(string='Analyst',
        comodel_name='res.users',
        domain="[('groups_id', 'in', (14,22))]",
        searchable = True,
        required=True
    ),
    # Instruments must be assigned directly to each analysis.
    fields.Many2one(string='Instrument',
        required = 0,
        comodel_name='olims.instrument',
    ),
    fields.Many2one(string='_Analyst',
        comodel_name='res.users',
        domain="[('groups_id', 'in', (14,22))]",
        searchable = True,
        # required=True
    ),
    fields.Many2one(string='_Instrument',
        required = 0,
        comodel_name='olims.instrument',
    ),
    TextField('Remarks',
        searchable = True,
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            macro="bika_widgets/remarks",
            label=_("Remarks"),
            append_only=True,
        ),
    ),
    fields.Many2many(string='AnalysisRequest',
        comodel_name="olims.add_analysis",
        domain="[('state', '=', 'unassigned'),('add_analysis_id.Sample_id.state','!=','disposed'),('add_analysis_id.state','=','sample_received')]"),
    fields.Selection(string='State',
                     selection=WORKSHEET_STATES,
                     default='open',
                     select=True,
                     required=True, readonly=True,
                     copy=False, track_visibility='always'
    ),
    fields.Many2many(string="ManageResult",
        comodel_name="olims.ws_manage_results",
                     ondelete='set null'),
    FileField('AttachmentFile',
        widget = FileWidget(
            label=_("Attachment"),
        ),
    ),
    fields.Many2one(string='AttachmentType',
                    comodel_name='olims.attachment_type',
                    required=False,
                    help='Attachment Type'
        ),

     StringField('AttachmentKeys',
        searchable = True,
        widget = StringWidget(
            label=_("Attachment Keys"),
        ),
    ),
    fields.Many2one(string="Analysis",
        comodel_name="olims.ws_manage_results",
        ondelete='set null'),
    fields.One2many('olims.ws_refrence_contorled_analysis',
        inverse_name='ws_control_reference_id',
        string="Add-Blank-Refrence",ondelete='set null'),
    fields.One2many('olims.ws_refrence_contorled_analysis',
        inverse_name='ws_blank_reference_id',
        string="Add-Control-Refrence",ondelete='set null'),
)



class Worksheet(models.Model, BaseOLiMSModel):
    _name ='olims.worksheet'
    _rec_name = "Worksheet"

    def _ComputeWorksheetId(self):
        for items in self:
            worksheetid = 'WS-0' + str(items.id)
            items.Worksheet = worksheetid

    @api.multi
    def write(self, values):
        data_list = []
        count = 0
        if values.get("AnalysisRequest", None):
            for items in sorted(values["AnalysisRequest"][0][2]):
                count += 1
                values_dict_manage_results = {}
                add_analysis_obj = self.env["olims.add_analysis"].browse(items)
                add_analysis_obj.write({'state':'assigned'})
                cont = False
                for record in self.ManageResult:
                    if record.request_analysis_id.id == add_analysis_obj.add_analysis_id.id and record.analysis.id == add_analysis_obj.analysis.id:
                        cont = True
                if cont:
                    continue

                values_dict_manage_results.update({"request_analysis_id":add_analysis_obj.add_analysis_id.id,
                    "analysis": add_analysis_obj.analysis.id,
                    "client":add_analysis_obj.client.id,
                    "due_date": add_analysis_obj.due_date,
                    "received_date": add_analysis_obj.received_date,
                    "sampling_date": add_analysis_obj.add_analysis_id.SamplingDate,
                    "sample_type": add_analysis_obj.add_analysis_id.SampleType.id,
                    "sample": add_analysis_obj.add_analysis_id.Sample_id.id,
                    "analyst": self.Analyst.id,
                    "instrument": self.Instrument.id,
                    "priority": add_analysis_obj.priority.id,
                    "position": count})
                rec_id = self.env["olims.ws_manage_results"].create(values_dict_manage_results)
                data_list.append([4,rec_id.id])
            values.update({"ManageResult": data_list})
        return super(Worksheet, self).write(values)



    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def Title(self):
        return safe_unicode(self.getId()).encode('utf-8')

    def getFolderContents(self, contentFilter):
        # The bika_listing machine passes contentFilter to all
        # contentsMethod methods.  We ignore it.
        return list(self.getAnalyses())

    #security.declareProtected(EditWorksheet, 'addAnalysis')

    def addAnalysis(self, analysis, position=None):
        """- add the analysis to self.Analyses().
           - position is overruled if a slot for this analysis' parent exists
           - if position is None, next available pos is used.
        """
        workflow = getToolByName(self, 'portal_workflow')

        analysis_uid = analysis.UID()
        parent_uid = analysis.aq_parent.UID()
        analyses = self.getAnalyses()
        layout = self.getLayout()

        # check if this analysis is already in the layout
        if analysis_uid in [l['analysis_uid'] for l in layout]:
            return

        # If the ws has an instrument assigned for which the analysis
        # is allowed, set it
        instr = self.getInstrument()
        if instr and analysis.isInstrumentAllowed(instr):
            # Set the method assigned to the selected instrument
            analysis.setMethod(instr.getMethod())
            analysis.setInstrument(instr)

        self.setAnalyses(analyses + [analysis, ])

        # if our parent has a position, use that one.
        if analysis.aq_parent.UID() in [slot['container_uid'] for slot in layout]:
            position = [int(slot['position']) for slot in layout if
                        slot['container_uid'] == analysis.aq_parent.UID()][0]
        else:
            # prefer supplied position parameter
            if not position:
                used_positions = [0, ] + [int(slot['position']) for slot in layout]
                position = [pos for pos in range(1, max(used_positions) + 2)
                            if pos not in used_positions][0]
        self.setLayout(layout + [{'position': position,
                                  'type': 'a',
                                  'container_uid': parent_uid,
                                  'analysis_uid': analysis.UID()}, ])

        allowed_transitions = [t['id'] for t in workflow.getTransitionsFor(analysis)]
        if 'assign' in allowed_transitions:
            workflow.doActionFor(analysis, 'assign')

        # If a dependency of DryMatter service is added here, we need to
        # make sure that the dry matter analysis itself is also
        # present.  Otherwise WS calculations refer to the DB version
        # of the DM analysis, which is out of sync with the form.
        dms = self.bika_setup.getDryMatterService()
        if dms:
            dmk = dms.getKeyword()
            deps = analysis.getDependents()
            # if dry matter service in my dependents:
            if dmk in [a.getService().getKeyword() for a in deps]:
                # get dry matter analysis from AR
                dma = analysis.aq_parent.getAnalyses(getKeyword=dmk,
                                                     full_objects=True)[0]
                # add it.
                if dma not in self.getAnalyses():
                    self.addAnalysis(dma)

    #security.declareProtected(EditWorksheet, 'removeAnalysis')

    def removeAnalysis(self, analysis):
        """ delete an analyses from the worksheet and un-assign it
        """
        workflow = getToolByName(self, 'portal_workflow')

        # overwrite saved context UID for event subscriber
        self.REQUEST['context_uid'] = self.UID()
        workflow.doActionFor(analysis, 'unassign')
        # Note: subscriber might unassign the AR and/or promote the worksheet

        # remove analysis from context.Analyses *after* unassign,
        # (doActionFor requires worksheet in analysis.getBackReferences)
        Analyses = self.getAnalyses()
        if analysis in Analyses:
            Analyses.remove(analysis)
            self.setAnalyses(Analyses)
        layout = [slot for slot in self.getLayout() if slot['analysis_uid'] != analysis.UID()]
        self.setLayout(layout)

        if analysis.portal_type == "DuplicateAnalysis":
            self._delObject(analysis.id)

    def addReferences(self, position, reference, service_uids):
        """ Add reference analyses to reference, and add to worksheet layout
        """
        workflow = getToolByName(self, 'portal_workflow')
        rc = getToolByName(self, REFERENCE_CATALOG)
        layout = self.getLayout()
        wst = self.getWorksheetTemplate()
        wstlayout = wst and wst.getLayout() or []
        ref_type = reference.getBlank() and 'b' or 'c'
        ref_uid = reference.UID()

        if position == 'new':
            highest_existing_position = len(wstlayout)
            for pos in [int(slot['position']) for slot in layout]:
                if pos > highest_existing_position:
                    highest_existing_position = pos
            position = highest_existing_position + 1

        postfix = 1
        for refa in reference.getReferenceAnalyses():
            grid = refa.getReferenceAnalysesGroupID()
            try:
                cand = int(grid.split('-')[2])
                if cand >= postfix:
                    postfix = cand + 1
            except:
                pass
        postfix = str(postfix).zfill(int(3))
        refgid = '%s-%s' % (reference.id, postfix)
        for service_uid in service_uids:
            # services with dependents don't belong in references
            service = rc.lookupObject(service_uid)
            calc = service.getCalculation()
            if calc and calc.getDependentServices():
                continue
            ref_uid = reference.addReferenceAnalysis(service_uid, ref_type)
            ref_analysis = rc.lookupObject(ref_uid)

            # Set ReferenceAnalysesGroupID (same id for the analyses from
            # the same Reference Sample and same Worksheet)
            # https://github.com/bikalabs/Bika-LIMS/issues/931
            ref_analysis.setReferenceAnalysesGroupID(refgid)
            ref_analysis.reindexObject(idxs=["getReferenceAnalysesGroupID"])

            # copy the interimfields
            if calc:
                ref_analysis.setInterimFields(calc.getInterimFields())

            self.setLayout(
                self.getLayout() + [{'position': position,
                                     'type': ref_type,
                                     'container_uid': reference.UID(),
                                     'analysis_uid': ref_analysis.UID()}])
            self.setAnalyses(
                self.getAnalyses() + [ref_analysis, ])
            workflow.doActionFor(ref_analysis, 'assign')

    #security.declareProtected(EditWorksheet, 'addDuplicateAnalyses')

    def addDuplicateAnalyses(self, src_slot, dest_slot):
        """ add duplicate analyses to worksheet
        """
        rc = getToolByName(self, REFERENCE_CATALOG)
        workflow = getToolByName(self, 'portal_workflow')

        layout = self.getLayout()
        wst = self.getWorksheetTemplate()
        wstlayout = wst and wst.getLayout() or []

        src_ar = [slot['container_uid'] for slot in layout if
                  slot['position'] == src_slot]
        if src_ar:
            src_ar = src_ar[0]

        if not dest_slot or dest_slot == 'new':
            highest_existing_position = len(wstlayout)
            for pos in [int(slot['position']) for slot in layout]:
                if pos > highest_existing_position:
                    highest_existing_position = pos
            dest_slot = highest_existing_position + 1

        src_analyses = [rc.lookupObject(slot['analysis_uid'])
                        for slot in layout if
                        int(slot['position']) == int(src_slot)]
        dest_analyses = [rc.lookupObject(slot['analysis_uid']).getAnalysis().UID()
                        for slot in layout if
                        int(slot['position']) == int(dest_slot)]

        refgid = None
        for analysis in src_analyses:
            if analysis.UID() in dest_analyses:
                continue
            # services with dependents don't belong in duplicates
            service = analysis.getService()
            calc = service.getCalculation()
            if calc and calc.getDependentServices():
                continue
            service = analysis.getService()
            _id = self._findUniqueId(service.getKeyword())
            duplicate = _createObjectByType("DuplicateAnalysis", self, _id)
            duplicate.setAnalysis(analysis)

            # Set ReferenceAnalysesGroupID (same id for the analyses from
            # the same Reference Sample and same Worksheet)
            # https://github.com/bikalabs/Bika-LIMS/issues/931
            if not refgid and not analysis.portal_type == 'ReferenceAnalysis':
                part = analysis.getSamplePartition().id
                dups = [an.getReferenceAnalysesGroupID()
                        for an in self.getAnalyses()
                        if an.portal_type == 'DuplicateAnalysis'
                            and an.getSamplePartition().id == part]
                dups = list(set(dups))
                postfix = dups and len(dups) + 1 or 1
                postfix = str(postfix).zfill(int(2))
                refgid = '%s-D%s' % (part, postfix)
            duplicate.setReferenceAnalysesGroupID(refgid)
            duplicate.reindexObject(idxs=["getReferenceAnalysesGroupID"])

            duplicate.processForm()
            if calc:
                duplicate.setInterimFields(calc.getInterimFields())
            self.setLayout(
                self.getLayout() + [{'position': dest_slot,
                                     'type': 'd',
                                     'container_uid': analysis.aq_parent.UID(),
                                     'analysis_uid': duplicate.UID()}, ]
            )
            self.setAnalyses(self.getAnalyses() + [duplicate, ])
            workflow.doActionFor(duplicate, 'assign')
            # In case there are more than one analyses for an 'analysis_uid'
            # https://jira.bikalabs.com/browse/LIMS-1745
            break

    def applyWorksheetTemplate(self, wst):
        """ Add analyses to worksheet according to wst's layout.
            Will not overwrite slots which are filled already.
            If the selected template has an instrument assigned, it will
            only be applied to those analyses for which the instrument
            is allowed
        """
        rc = getToolByName(self, REFERENCE_CATALOG)
        bac = getToolByName(self, "bika_analysis_catalog")
        bc = getToolByName(self, 'bika_catalog')

        layout = self.getLayout()
        wstlayout = wst.getLayout()
        services = wst.getService()
        wst_service_uids = [s.UID() for s in services]

        analyses = bac(portal_type='Analysis',
                       getServiceUID=wst_service_uids,
                       review_state='sample_received',
                       worksheetanalysis_review_state='unassigned',
                       cancellation_state = 'active')
        sortedans = []
        for an in analyses:
            sortedans.append({'uid': an.UID,
                              'duedate': an.getObject().getDueDate() or (DateTime() + 365),
                              'brain': an});
        sortedans.sort(key=itemgetter('duedate'), reverse=False)
        # collect analyses from the first X ARs.
        ar_analyses = {}  # ar_uid : [analyses]
        ars = []  # for sorting

        wst_slots = [row['pos'] for row in wstlayout if row['type'] == 'a']
        ws_slots = [row['position'] for row in layout if row['type'] == 'a']
        nr_slots = len(wst_slots) - len(ws_slots)
        instr = self.getInstrument() if self.getInstrument() else wst.getInstrument()
        for analysis in sortedans:
            analysis = analysis['brain']
            if instr and analysis.getObject().isInstrumentAllowed(instr) == False:
                # Exclude those analyses for which the ws selected
                # instrument is not allowed
                continue
            ar = analysis.getRequestID
            if ar in ar_analyses:
                ar_analyses[ar].append(analysis.getObject())
            else:
                if len(ar_analyses.keys()) < nr_slots:
                    ars.append(ar)
                    ar_analyses[ar] = [analysis.getObject(), ]

        positions = [pos for pos in wst_slots if pos not in ws_slots]
        for ar in ars:
            for analysis in ar_analyses[ar]:
                self.addAnalysis(analysis, position=positions[ars.index(ar)])

        # find best maching reference samples for Blanks and Controls
        for t in ('b', 'c'):
            form_key = t == 'b' and 'blank_ref' or 'control_ref'
            ws_slots = [row['position'] for row in layout if row['type'] == t]
            for row in [r for r in wstlayout if
                        r['type'] == t and r['pos'] not in ws_slots]:
                reference_definition_uid = row[form_key]
                samples = bc(portal_type='ReferenceSample',
                             review_state='current',
                             inactive_state='active',
                             getReferenceDefinitionUID=reference_definition_uid)
                if not samples:
                    break
                samples = [s.getObject() for s in samples]
                if t == 'b':
                    samples = [s for s in samples if s.getBlank()]
                else:
                    samples = [s for s in samples if not s.getBlank()]
                complete_reference_found = False
                references = {}
                for reference in samples:
                    reference_uid = reference.UID()
                    references[reference_uid] = {}
                    references[reference_uid]['services'] = []
                    references[reference_uid]['count'] = 0
                    specs = reference.getResultsRangeDict()
                    for service_uid in wst_service_uids:
                        if service_uid in specs:
                            references[reference_uid]['services'].append(service_uid)
                            references[reference_uid]['count'] += 1
                    if references[reference_uid]['count'] == len(wst_service_uids):
                        complete_reference_found = True
                        break
                if complete_reference_found:
                    supported_uids = wst_service_uids
                    self.addReferences(int(row['pos']),
                                     reference,
                                     supported_uids)
                else:
                    # find the most complete reference sample instead
                    reference_keys = references.keys()
                    no_of_services = 0
                    reference = None
                    for key in reference_keys:
                        if references[key]['count'] > no_of_services:
                            no_of_services = references[key]['count']
                            reference = key
                    if reference:
                        reference = rc.lookupObject(reference)
                        supported_uids = [s.UID() for s in reference.getServices()
                                          if s.UID() in wst_service_uids]
                        self.addReferences(int(row['pos']),
                                         reference,
                                         supported_uids)

        # fill duplicate positions
        layout = self.getLayout()
        ws_slots = [row['position'] for row in layout if row['type'] == 'd']
        for row in [r for r in wstlayout if
                    r['type'] == 'd' and r['pos'] not in ws_slots]:
            dest_pos = int(row['pos'])
            src_pos = int(row['dup'])
            if src_pos in [int(slot['position']) for slot in layout]:
                self.addDuplicateAnalyses(src_pos, dest_pos)

        # Apply the wst instrument to all analyses and ws
        if instr:
            self.setInstrument(instr, True)

    def exportAnalyses(self, REQUEST=None, RESPONSE=None):
        """ Export analyses from this worksheet """
        # import bika.lims.InstrumentExport as InstrumentExport
        # instrument = REQUEST.form['getInstrument']
        # try:
        #     func = getattr(InstrumentExport, "%s_export" % instrument)
        # except:
        #     return
        # func(self, REQUEST, RESPONSE)
        return

    #security.declarePublic('getWorksheetServices')

    def getWorksheetServices(self):
        """ get list of analysis services present on this worksheet
        """
        services = []
        for analysis in self.getAnalyses():
            service = analysis.getService()
            if service not in services:
                services.append(service)
        return services

    #security.declareProtected(EditWorksheet, 'resequenceWorksheet')

    def resequenceWorksheet(self, REQUEST=None, RESPONSE=None):
        """  Reset the sequence of analyses in the worksheet """
        """ sequence is [{'pos': , 'type': , 'uid', 'key'},] """
        old_seq = self.getLayout()
        new_dict = {}
        new_seq = []
        other_dict = {}
        for seq in old_seq:
            if seq['key'] == '':
                if seq['pos'] not in other_dict:
                    other_dict[seq['pos']] = []
                other_dict[seq['pos']].append(seq)
                continue
            if seq['key'] not in new_dict:
                new_dict[seq['key']] = []
            analyses = new_dict[seq['key']]
            analyses.append(seq)
            new_dict[seq['key']] = analyses
        new_keys = sorted(new_dict.keys())

        rc = getToolByName(self, REFERENCE_CATALOG)
        seqno = 1
        for key in new_keys:
            analyses = {}
            if len(new_dict[key]) == 1:
                new_dict[key][0]['pos'] = seqno
                new_seq.append(new_dict[key][0])
            else:
                for item in new_dict[key]:
                    item['pos'] = seqno
                    analysis = rc.lookupObject(item['uid'])
                    service = analysis.Title()
                    analyses[service] = item
                a_keys = sorted(analyses.keys())
                for a_key in a_keys:
                    new_seq.append(analyses[a_key])
            seqno += 1
        other_keys = other_dict.keys()
        other_keys.sort()
        for other_key in other_keys:
            for item in other_dict[other_key]:
                item['pos'] = seqno
                new_seq.append(item)
            seqno += 1

        self.setLayout(new_seq)
        RESPONSE.redirect('%s/manage_results' % self.absolute_url())

    #security.declarePublic('current_date')

    def current_date(self):
        """ return current date """
        return DateTime()

    @api.onchange('Template')
    def onchange_worksheettemplatevalue(self):
        """Sets the specified instrument to the Analysis from the
            Worksheet Template.
        """
        self.Instrument = self.Template.Instrument.id

    def workflow_script_submit(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids,{'State': 'to_be_verified'},context)
        return True

    def workflow_script_attach(self):
        if skip(self, "attach"):
            return
        self.reindexObject(idxs=["review_state", ])
        # Don't cascade. Shouldn't be attaching WSs for now (if ever).
        return

    def workflow_script_retract(self):
        if skip(self, "retract"):
            return
        workflow = getToolByName(self, 'portal_workflow')
        self.reindexObject(idxs=["review_state", ])
        if not "retract all analyses" in self.REQUEST['workflow_skiplist']:
            # retract all analyses in this self.
            # (NB: don't retract if it's verified)
            analyses = self.getAnalyses()
            for analysis in analyses:
                state = workflow.getInfoFor(analysis, 'review_state', '')
                if state not in ('attachment_due', 'to_be_verified',):
                    continue
                doActionFor(analysis, 'retract')

    def workflow_script_verify(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids,{'State': 'verified'},context)
        return True

    def workflow_script_reject(self):
        """Copy real analyses to RejectAnalysis, with link to real
           create a new worksheet, with the original analyses, and new
           duplicates and references to match the rejected
           worksheet.
        """
        if skip(self, "reject"):
            return
        utils = getToolByName(self, 'plone_utils')
        workflow = self.portal_workflow

        def copy_src_fields_to_dst(src, dst):
            # These will be ignored when copying field values between analyses
            ignore_fields = ['UID',
                             'id',
                             'title',
                             'allowDiscussion',
                             'subject',
                             'description',
                             'location',
                             'contributors',
                             'creators',
                             'effectiveDate',
                             'expirationDate',
                             'language',
                             'rights',
                             'creation_date',
                             'modification_date',
                             'Layout',    # ws
                             'Analyses',  # ws
            ]
            fields = src.Schema().fields()
            for field in fields:
                fieldname = field.getName()
                if fieldname in ignore_fields:
                    continue
                getter = getattr(src, 'get'+fieldname,
                                 src.Schema().getField(fieldname).getAccessor(src))
                setter = getattr(dst, 'set'+fieldname,
                                 dst.Schema().getField(fieldname).getMutator(dst))
                if getter is None or setter is None:
                    # ComputedField
                    continue
                setter(getter())

        analysis_positions = {}
        for item in self.getLayout():
            analysis_positions[item['analysis_uid']] = item['position']
        old_layout = []
        new_layout = []

        # New worksheet
        worksheets = self.aq_parent
        new_ws = _createObjectByType('Worksheet', worksheets, tmpID())
        new_ws.unmarkCreationFlag()
        new_ws_id = renameAfterCreation(new_ws)
        copy_src_fields_to_dst(self, new_ws)
        new_ws.edit(
            Number = new_ws_id,
            Remarks = self.getRemarks()
        )

        # Objects are being created inside other contexts, but we want their
        # workflow handlers to be aware of which worksheet this is occurring in.
        # We save the worksheet in request['context_uid'].
        # We reset it again below....  be very sure that this is set to the
        # UID of the containing worksheet before invoking any transitions on
        # analyses.
        self.REQUEST['context_uid'] = new_ws.UID()

        # loop all analyses
        analyses = self.getAnalyses()
        new_ws_analyses = []
        old_ws_analyses = []
        for analysis in analyses:
            # Skip published or verified analyses
            review_state = workflow.getInfoFor(analysis, 'review_state', '')
            if review_state in ['published', 'verified', 'retracted']:
                old_ws_analyses.append(analysis.UID())
                old_layout.append({'position': position,
                                   'type':'a',
                                   'analysis_uid':analysis.UID(),
                                   'container_uid':analysis.aq_parent.UID()})
                continue
            # Normal analyses:
            # - Create matching RejectAnalysis inside old WS
            # - Link analysis to new WS in same position
            # - Copy all field values
            # - Clear analysis result, and set Retested flag
            if analysis.portal_type == 'Analysis':
                reject = _createObjectByType('RejectAnalysis', self, tmpID())
                reject.unmarkCreationFlag()
                reject_id = renameAfterCreation(reject)
                copy_src_fields_to_dst(analysis, reject)
                reject.setAnalysis(analysis)
                reject.reindexObject()
                analysis.edit(
                    Result = None,
                    Retested = True,
                )
                analysis.reindexObject()
                position = analysis_positions[analysis.UID()]
                old_ws_analyses.append(reject.UID())
                old_layout.append({'position': position,
                                   'type':'r',
                                   'analysis_uid':reject.UID(),
                                   'container_uid':self.UID()})
                new_ws_analyses.append(analysis.UID())
                new_layout.append({'position': position,
                                   'type':'a',
                                   'analysis_uid':analysis.UID(),
                                   'container_uid':analysis.aq_parent.UID()})
            # Reference analyses
            # - Create a new reference analysis in the new worksheet
            # - Transition the original analysis to 'rejected' state
            if analysis.portal_type == 'ReferenceAnalysis':
                service_uid = analysis.getService().UID()
                reference = analysis.aq_parent
                reference_type = analysis.getReferenceType()
                new_analysis_uid = reference.addReferenceAnalysis(service_uid,
                                                                  reference_type)
                position = analysis_positions[analysis.UID()]
                old_ws_analyses.append(analysis.UID())
                old_layout.append({'position': position,
                                   'type':reference_type,
                                   'analysis_uid':analysis.UID(),
                                   'container_uid':reference.UID()})
                new_ws_analyses.append(new_analysis_uid)
                new_layout.append({'position': position,
                                   'type':reference_type,
                                   'analysis_uid':new_analysis_uid,
                                   'container_uid':reference.UID()})
                workflow.doActionFor(analysis, 'reject')
                new_reference = reference.uid_catalog(UID=new_analysis_uid)[0].getObject()
                workflow.doActionFor(new_reference, 'assign')
                analysis.reindexObject()
            # Duplicate analyses
            # - Create a new duplicate inside the new worksheet
            # - Transition the original analysis to 'rejected' state
            if analysis.portal_type == 'DuplicateAnalysis':
                src_analysis = analysis.getAnalysis()
                ar = src_analysis.aq_parent
                service = src_analysis.getService()
                duplicate_id = new_ws.generateUniqueId('DuplicateAnalysis')
                new_duplicate = _createObjectByType('DuplicateAnalysis',
                                                    new_ws, duplicate_id)
                new_duplicate.unmarkCreationFlag()
                copy_src_fields_to_dst(analysis, new_duplicate)
                workflow.doActionFor(new_duplicate, 'assign')
                new_duplicate.reindexObject()
                position = analysis_positions[analysis.UID()]
                old_ws_analyses.append(analysis.UID())
                old_layout.append({'position': position,
                                   'type':'d',
                                   'analysis_uid':analysis.UID(),
                                   'container_uid':self.UID()})
                new_ws_analyses.append(new_duplicate.UID())
                new_layout.append({'position': position,
                                   'type':'d',
                                   'analysis_uid':new_duplicate.UID(),
                                   'container_uid':new_ws.UID()})
                workflow.doActionFor(analysis, 'reject')
                analysis.reindexObject()

        new_ws.setAnalyses(new_ws_analyses)
        new_ws.setLayout(new_layout)
        new_ws.replaces_rejected_worksheet = self.UID()
        for analysis in new_ws.getAnalyses():
            review_state = workflow.getInfoFor(analysis, 'review_state', '')
            if review_state == 'to_be_verified':
                changeWorkflowState(analysis, "bika_analysis_workflow", "sample_received")
        self.REQUEST['context_uid'] = self.UID()
        self.setLayout(old_layout)
        self.setAnalyses(old_ws_analyses)
        self.replaced_by = new_ws.UID()


    def checkUserManage(self):
        """ Checks if the current user has granted access to this worksheet
            and if has also privileges for managing it.
        """
        granted = False
        can_access = self.checkUserAccess()

        if can_access == True:
            pm = getToolByName(self, 'portal_membership')
            edit_allowed = pm.checkPermission(EditWorksheet, self)
            if edit_allowed:
                # Check if the current user is the WS's current analyst
                member = pm.getAuthenticatedMember()
                analyst = self.getAnalyst().strip()
                if analyst != _c(member.getId()):
                    # Has management privileges?
                    if pm.checkPermission(ManageWorksheets, self):
                        granted = True
                else:
                    granted = True

        return granted

    def checkUserAccess(self):
        """ Checks if the current user has granted access to this worksheet.
            Returns False if the user has no access, otherwise returns True
        """
        # Deny access to foreign analysts
        allowed = True
        pm = getToolByName(self, "portal_membership")
        member = pm.getAuthenticatedMember()

        analyst = self.getAnalyst().strip()
        if analyst != _c(member.getId()):
            roles = member.getRoles()
            restrict = 'Manager' not in roles \
                    and 'LabManager' not in roles \
                    and 'LabClerk' not in roles \
                    and 'RegulatoryInspector' not in roles \
                    and self.bika_setup.getRestrictWorksheetUsersAccess()
            allowed = not restrict

        return allowed

    def setAnalyst(self,analyst):
        for analysis in self.getAnalyses():
            analysis.setAnalyst(analyst)
        self.Schema().getField('Analyst').set(self, analyst)

    #security.declarePublic('getPriority')
    def getPriority(self):
        """ get highest priority from all analyses
        """
        analyses = self.getAnalyses()
        priorities = []
        for analysis in analyses:
            if not hasattr(analysis, 'getPriority'):
                continue
            if analysis.getPriority():
                priorities.append(analysis.getPriority())
        priorities = sorted(priorities, key = itemgetter('sortKey'))
        if priorities:
            return priorities[-1]

    @api.multi
    def print_ws_manage_results(self):
        return self.env['report'].get_action(self, 'olims.report_ws_manage_results')

    @api.onchange('Analyst','_Analyst','Instrument', '_Instrument')
    def onchange_worksheettemplatevalue(self):
        if self.Analyst:
            self._Analyst = self.Analyst.id
        elif self._Analyst:
             self.Analyst = self._Analyst.id
        else:
            pass
        if self.Instrument:
            self._Instrument = self.Instrument.id
        elif self._Instrument:
             self.Instrument = self._Instrument.id
        else:
            pass

    def bulk_change_states(self,state,cr,uid,ids,context=None):
        previous_state = ""
        if state == "verified":
            previous_state = "to_be_verified"
        worksheets = self.browse(cr,uid,ids)
        ar_ids = []
        for worksheet in worksheets:
            if worksheet.State != previous_state:
                ids.remove(worksheet.id)
            else:
                records = worksheet.ManageResult
                for record in records:
                    record.write({"state":"verified"})
                    analyses = self.pool.get("olims.manage_analyses").search_read(cr,uid,[
                        "|",("Service","=",record.analysis.id)
                            ,("LabService","=",record.analysis.id),
                        "|",("manage_analysis_id","=",record.request_analysis_id.id),
                            ("lab_manage_analysis_id","=",record.request_analysis_id.id)
                        ])
                    for analysis in analyses:
                        self.pool.get("olims.manage_analyses").write(cr,uid,analysis['id'],{"state":"verified"})
                    if record.request_analysis_id not in ar_ids:
                        ar_ids.append(record.request_analysis_id.id)
        self.browse(cr,uid,ids).signal_workflow('verify')
        # Signaling workflow to verified for ar if all are verified
        for ar_id in ar_ids:
            arecs = self.pool.get("olims.manage_analyses").search_read(cr,uid,[
                "|",("manage_analysis_id","=",ar_id),
                    ("lab_manage_analysis_id","=",ar_id)
                ])
            for arec in arecs:
                if arec['state'] != "verified":
                    ar_ids.remove(ar_id)
                    break
        self.pool.get("olims.analysis_request").browse(cr,uid,ar_ids).signal_workflow('verify')
        return True


class AddAnalysis(models.Model):
    _name = "olims.add_analysis"

    category = fields.Many2one('olims.analysis_category',string='Category',
        ondelete='set null')
    analysis = fields.Many2one(string='Analysis',
        comodel_name="olims.analysis_service", ondelete='set null')
    client = fields.Many2one('olims.client',
        ondelete='set null', string="Client")
    order = fields.Char('Order', readonly="True")
    priority = fields.Many2one('olims.ar_priority',
        ondelete='set null', string="Priority")
    due_date = fields.Datetime('Due Date', readonly="True")
    received_date = fields.Datetime('Date Received', readonly="True")
    add_analysis_id = fields.Many2one("olims.analysis_request",
        ondelete='set null', string="Request ID",
        domain="[('state', '=', 'sample_received')]")
    sample_type = fields.Many2one(string="Sample Type",
        comodel_name="olims.sample_type",ondelete='set null')
    state = fields.Selection(string='State',
                     selection=[
                     ('assigned', 'Assigned'),
                     ('unassigned', 'Unassigned')],
                     default='unassigned',
                     select=True,
                     readonly=True,
                     copy=False, track_visibility='always'
    )

    @api.model
    def create(self, values):
        res = super(AddAnalysis, self).create(values)
        return res

class WorkSheetManageResults(models.Model):
    _name = "olims.ws_manage_results"
    _rec_name = "analysis"

    analysis = fields.Many2one(string='Analysis',
        comodel_name="olims.analysis_service", ondelete='set null')
    client = fields.Many2one('olims.client',
        ondelete='set null', string="Client")
    request_analysis_id = fields.Many2one("olims.analysis_request",
        ondelete='set null', string="Request ID")
    due_date = fields.Datetime("Due Date")
    sample_type = fields.Many2one(string="Sample Type",
        comodel_name="olims.sample_type")
    sample = fields.Many2one(string="Sample",
        comodel_name="olims.sample")
    sampling_date = fields.Datetime("Sampling Date")
    received_date = fields.Datetime("Received Date")
    result = fields.Char("Results")
    position = fields.Integer(string="Position")
    analyst = fields.Many2one(string='Analyst',
        comodel_name='res.users',
        domain="[('groups_id', 'in', (14,22))]",
    )
    instrument = fields.Many2one(string='Instrument',
        required = 0,
        comodel_name='olims.instrument',
    )
    priority = fields.Many2one('olims.ar_priority',
        ondelete='set null', string="Priority")
    captured = fields.Boolean("+-")
    state = fields.Selection(string='State',
                     selection=AR_STATES,
                     default='sample_received',
                     select=True,
                     readonly=True,
                     copy=False, track_visibility='always'
    )

    @api.multi
    def bulk_verify(self):
        ar_ids = []
        for record in self:
            if not record.result or record.state == "verified":
                continue
            record.write({"state":"to_be_verified"})
            analyses = self.env["olims.manage_analyses"].search([
                "|",("Service","=",record.analysis.id)
                    ,("LabService","=",record.analysis.id),
                "|",("manage_analysis_id","=",record.request_analysis_id.id),
                    ("lab_manage_analysis_id","=",record.request_analysis_id.id)
                ])
            for analysis in analyses:
                analysis.write({"state":"to_be_verified","Result":record.result})
            arecs = self.env["olims.manage_analyses"].search([
                "|",("manage_analysis_id","=",record.request_analysis_id.id),
                    ("lab_manage_analysis_id","=",record.request_analysis_id.id)
                ])
            all_submitted = True
            for arec in arecs:
                if arec.state != "to_be_verified" and arec.state != "verified":
                    all_submitted = False
                    break
            if all_submitted:
                ar_ids.append(record.request_analysis_id.id)                    
        self.env["olims.analysis_request"].browse(ar_ids).signal_workflow("submit")
        worksheet = self.env['olims.worksheet'].search([("ManageResult","=",self[0].id)])
        ws_all_submitted = True
        for ws_result in worksheet.ManageResult:
            if ws_result.state != "to_be_verified" and ws_result.state != "verified":
                ws_all_submitted = False
                break
        if ws_all_submitted:
            self.env["olims.worksheet"].browse(worksheet.id).signal_workflow("submit")
        return True

    @api.multi
    def verify_analyses_and_ws(self):
        ar_ids = []
        for record in self:
            if not record.state != "verified":
                continue
            record.write({"state":"verified"})
            analyses = self.env["olims.manage_analyses"].search([
                "|",("Service","=",record.analysis.id)
                    ,("LabService","=",record.analysis.id),
                "|",("manage_analysis_id","=",record.request_analysis_id.id),
                    ("lab_manage_analysis_id","=",record.request_analysis_id.id)
                ])
            for analysis in analyses:
                analysis.write({"state":"verified"})
            arecs = self.env["olims.manage_analyses"].search([
                "|",("manage_analysis_id","=",record.request_analysis_id.id),
                    ("lab_manage_analysis_id","=",record.request_analysis_id.id)
                ])
            all_verified = True
            for arec in arecs:
                if arec.state != "verified":
                    all_verified = False
                    break
            if all_verified:
                ar_ids.append(record.request_analysis_id.id)
        self.env["olims.analysis_request"].browse(ar_ids).signal_workflow("verify")
        worksheet = self.env['olims.worksheet'].search([("ManageResult","=",self[0].id)])
        ws_all_verified = True
        for ws_result in worksheet.ManageResult:
            if ws_result.state != "verified":
                ws_all_verified = False
                break
        if ws_all_verified:
            self.env["olims.worksheet"].browse(worksheet.id).signal_workflow("verify")
        return True

class WorkSheetAddRefreceAnalysis(models.Model):
    _name = "olims.ws_refrence_contorled_analysis"

    category = fields.Many2one('olims.analysis_category',string='Category',
        ondelete='set null')
    analysis = fields.Many2one(string='Service',
        comodel_name="olims.analysis_service",
        ondelete='set null', domain="[('category', '=', category)]")
    ws_control_reference_id = fields.Many2one('olims.worksheet',ondelete='set null')
    ws_blank_reference_id = fields.Many2one('olims.worksheet',ondelete='set null')

Worksheet.initialze(schema)

