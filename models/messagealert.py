from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
import datetime

schema = (fields.Char(string='severity'),
    fields.Text(string='message'),
    fields.Many2one(string='Instrument',
        comodel_name='olims.instrument',
         ondelete='cascade'),
          )
def write_message(self, values, sourcemodel):
    if values.get('DownTo'):
        instrument_object = self.env["olims.instrument"].search([('id', \
                                                                  '=', values.get('Instrument') or self.Instrument.id)])
        instrument_obj = self.env["olims.instrument"].browse(instrument_object.id)
        valid_date = datetime.datetime.strptime(values.get('DownTo'), \
                                "%Y-%m-%d %H:%M:%S")
        if sourcemodel == "InstrumentCalibration":
            message = "Instrument in calibration progress"
        elif sourcemodel == "InstrumentValidation":
            message = "Instrument in validation progress"
        elif sourcemodel == "InstrumentCertification":
            message = "Instrument disposed until new calibration tests being done"
            expiry_date = {'ExpiryDate':valid_date,}
            instrument_object.write(expiry_date)
        message_alert_objects = self.env["olims.message_alert"]
        message_alert_obj = message_alert_objects.search([('Instrument', \
                '=', values.get('Instrument') or self.Instrument.id)])
        message_alert_object = message_alert_objects.browse(message_alert_obj.id)
        if valid_date > datetime.datetime.now():
            message_alert_value = {
				'message' : message,
				'severity' :"medium",
				'Instrument' : values.get('Instrument') or self.Instrument.id,
				}
            if message_alert_obj:
                if not message_alert_object.message == "Instrument's calibration certificate expired":
                    message_alert_obj.write(message_alert_value)
                else:
                    #do nothing
                    pass
            else:
                message_alert_obj.create(message_alert_value)
            if sourcemodel == "InstrumentCertification":
                if instrument_obj.DisposeUntilNextCalibrationTest:
                    message_alert_values = {'message' : message,
            		'severity' :"medium",
            		'Instrument' : values.get('Instrument') or self.Instrument.id,
            		}
                    message_alert_obj.write(message_alert_values)
                else:
                    message_alert_obj.unlink()
        else:
            if sourcemodel == "InstrumentCertification":
                alert_message_vals = {
                    'message' : "Instrument's calibration certificate expired",
                    'severity' :"high",
                    'Instrument' : self.Instrument.id or values.get('Instrument'),
                    }
                if message_alert_obj:
                    message_alert_obj.write(alert_message_vals)
                else:
                    message_alert_obj.create(alert_message_vals)
            if not message_alert_object.message == "Instrument's calibration certificate expired":
                message_alert_obj.unlink()


class MessageAlert(models.Model, BaseOLiMSModel): 
    _name='olims.message_alert'
    _inherit = ['ir.needaction_mixin']
    @api.model
    def _needaction_count(self, domain=None):
        return self.search_count([])
    
    @api.model
    def compute_warnning_messages(self):
        certificate_expire = False
        current_date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        message_alert_objects = self.env["olims.message_alert"]
        instruments_certification_objects = self.env["olims.instrument_certification"].search([])
        instruments_calibration_objects = self.env["olims.instrument_calibration"].search([])
        instruments_validation_objects = self.env["olims.instrument_validation"].search([])
        for certificate in instruments_certification_objects:
            if certificate.DownTo:
                validity_date = datetime.datetime.strptime(certificate.DownTo, \
                                "%Y-%m-%d %H:%M:%S")
                if validity_date >= datetime.datetime.now():
                    certificate_expire = True
            if certificate_expire == False:
                certificate_expiry_message = message_alert_objects.search([('Instrument', \
                                                                      '=', certificate.Instrument.id)])
                message_vals = {
                                'message' : "Instrument's calibration certificate expired",
                                'severity' :"high",
                                'Instrument' : certificate.Instrument.id,
                                }
                if certificate_expiry_message:
                    certificate_expiry_message.write(message_vals)
                else:
                    message_alert_objects.create(message_vals)
        for calibration in instruments_calibration_objects:
            if calibration.DownTo:
                validity_date = datetime.datetime.strptime(calibration.DownTo, \
                                "%Y-%m-%d %H:%M:%S")
                if validity_date < datetime.datetime.now():
                    calibiration_progress_message_object = message_alert_objects.search([('Instrument', \
                                                                      '=', calibration.Instrument.id)])
                    instrument_validation_object = self.env["olims.instrument_validation"].search([('Instrument', \
                                                        '=', calibration.Instrument.id), \
                                                        ('DownTo', '>', current_date)])
                    message_vals = {
                                'message' : "Instrument in validation progress",
                                'severity' :"high",
                                'Instrument' : calibration.Instrument.id,
                                }
                    if calibiration_progress_message_object:
                        if not calibiration_progress_message_object.message == "Instrument's calibration certificate expired":
                            if instrument_validation_object:
                                calibiration_progress_message_object.write(message_vals)
                            else:
                                calibiration_progress_message_object.unlink()
                    elif not calibiration_progress_message_object and instrument_validation_object:
                        calibiration_progress_message_object.create(message_vals)
        for validation in instruments_validation_objects:
            if validation.DownTo:
                validity_date = datetime.datetime.strptime(validation.DownTo, \
                                "%Y-%m-%d %H:%M:%S")
                if validity_date < datetime.datetime.now():
                    message_validation_progress_object = message_alert_objects.search([('Instrument', \
                                                                      '=', validation.Instrument.id)])
                    instrument_calibration_object = self.env["olims.instrument_calibration"].search([('Instrument', \
                                                        '=', validation.Instrument.id), \
                                                        ('DownTo', '>', current_date)])
                    message_vals = {
                                'message' : "Instrument in calibration progress",
                                'severity' :"high",
                                'Instrument' : validation.Instrument.id,
                                }
                    if message_validation_progress_object:
                        if instrument_calibration_object:
                            message_validation_progress_object.write(message_vals)
                        else:
                            message_validation_progress_object.unlink()
                    elif not message_validation_progress_object and instrument_calibration_object:
                        message_validation_progress_object.create(message_vals)
        return True

MessageAlert.initialze(schema)