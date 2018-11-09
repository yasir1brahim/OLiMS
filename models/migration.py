from openerp import fields, models, api

class WorksheetMigration(models.Model): 
	_name='olims.worksheet_migration'


	@api.model
	def migration(self):
		duplicate = {}
		worksheets = self.env["olims.worksheet"].search([('id', '>',0 )])
		for worksheet in worksheets:
			for item in worksheet.ManageResult:
				if worksheet.id not in duplicate.keys() or duplicate[worksheet.id] != item.request_analysis_id.id:
					ar_object = self.env["olims.analysis_request"].search([('id', '=', item.request_analysis_id.id )])
					wid = worksheet.id
					if wid:
						print wid,"WID"
						ar_object.write({"ar_worksheets": [(4, worksheet.id)]})
					duplicate[worksheet.id] = item.request_analysis_id.id
		return True


	@api.model
	def migrationarnumber(self):
		duplicate = {}
		analysis_requests = self.env["olims.analysis_request"].search([('id', '>',0 )])
		for analysis_request in analysis_requests:
			ar_object = self.env["olims.analysis_request"].search([('id', '=', analysis_request.id )])
			ar_object.write({"ar_counter":ar_object.id})
		return

	@api.model
	def migrationarpublish_date(self):
		invoices = self.env["olims.ar_invoice"].search([('id', '>',0 )])
		for invoice in invoices:
			print "------",invoice.id
			invoice_object = self.env["olims.ar_invoice"].search([('id', '=', invoice.id )])
			invoice_object.write({"published_date":invoice.end_date})
		return


	@api.model
	def migration_analysisprofile_name(self):
		profiles = self.env["olims.analysis_profile"].search([('id', '>',0 )])
		for profile in profiles:
			print "--------profile id: ",profile.id
			profile_object = self.env["olims.analysis_profile"].search([('id', '=', profile.id )])
			profile_object.write({"name":profile.Profile})
		return

	@api.model
	def migration_analysisprofile_filed_ar(self):
		analysis_requests = self.env["olims.analysis_request"].search([('id', '>', 0)])
		for request in analysis_requests:
			query = "select " + '"AnalysisProfile",' + '"AnalysisProfile1",' + '"AnalysisProfile2",' + '"AnalysisProfile3"' + "from olims_analysis_request where id = " + "'" + str(
				request.id) + "'"
			self.env.cr.execute(query)
			profiles_list = self.env.cr.fetchall()
			AnalysisProfile, AnalysisProfile1, AnalysisProfile2, AnalysisProfile3 = None, None, None, None
			print '---profiles list', profiles_list[0]
			if profiles_list[0][0]:
				AnalysisProfile = [(6, 0, [profiles_list[0][0]])]
			if profiles_list[0][1]:
				AnalysisProfile1 = [(6, 0, [profiles_list[0][1]])]
			if profiles_list[0][2]:
				AnalysisProfile2 = [(6, 0, [profiles_list[0][2]])]
			if profiles_list[0][3]:
				AnalysisProfile3 = [(6, 0, [profiles_list[0][3]])]
			request.write({'AnalysisProfile': AnalysisProfile, 'AnalysisProfile1': AnalysisProfile1, 'AnalysisProfile2': \
				AnalysisProfile2, 'AnalysisProfile3': AnalysisProfile3})

		return True

	@api.model
	def migration_client_model_login_detail(self):
		clients = self.env["olims.client"].search([('id', '>', 0)])
		for client in clients:
			client_contacts = self.env['olims.contact'].search([('Client_Contact', '=', client.id)])
			for obj in client_contacts:
				if obj.user:
					obj.user.write({'client_id': client.id, 'contact_id' : obj.id})

		return True

	@api.model
	def fill_olims_analysis_request_sample_rel(self, cr, uid, context=None):
		analysis_request = self.pool.get('olims.analysis_request')
		sample_objs = self.pool.get('olims.sample').search_read(cr, uid, [])
		for obj_dict in sample_objs:
			corresponding_ars = analysis_request.search(cr, uid, [('Sample_id', '=', obj_dict.get('id'))])
			if corresponding_ars:
				self.pool.get('olims.sample').write(cr, uid, [obj_dict.get('id')],
													{'Corresponding_ARs': [(6, 0, [corresponding_ars])]})

	@api.model
	def update_position_in_ws_results(self):
		worksheets = self.env['olims.worksheet'].search([('id', '>', 0)])
		for worksheet_obj in worksheets:
			print '\n\n========================= updating results of workssheet:',worksheet_obj.id
			new_position = 0
			worksheet_add_analyses_list = []
			for add_analyses in worksheet_obj.AnalysisRequest:
				worksheet_add_analyses_list.append(add_analyses.id)
			for add_analyses_id in sorted(worksheet_add_analyses_list):
				new_position += 1
				add_analysis_obj = self.env['olims.add_analysis'].browse(add_analyses_id)
				for cate_analysis in add_analysis_obj.add_analysis_id.Analyses:
					if cate_analysis.Category.id == add_analysis_obj.category.id:
						ws_results = self.env['olims.ws_manage_results'].search(['&', ('request_analysis_id', '=', \
																						   add_analysis_obj.add_analysis_id.id),
																				(
																				'category', '=', cate_analysis.Category.id), \
																				])

						for ws_result in ws_results:
							print '\n\n========= Add Analysis id',add_analysis_obj.id,'========== position',new_position
							ws_result.write({'position': new_position})

