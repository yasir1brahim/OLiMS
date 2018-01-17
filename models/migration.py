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
		return


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
