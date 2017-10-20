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
	    			

	    			print str(item.request_analysis_id.id)+' ------------------- '+str(worksheet.id)
	    			ar_object = self.env["olims.analysis_request"].search([('id', '=', item.request_analysis_id.id )])
	    			wid = worksheet.id
	    			if wid:
	    				print wid,"WID"
	    				ar_object.write({"ar_worksheets": [(4, worksheet.id)]})
	    			duplicate[worksheet.id] = item.request_analysis_id.id
	    		# print str(item.request_analysis_id.id)+' ==== '+str(worksheet.id)

        return
