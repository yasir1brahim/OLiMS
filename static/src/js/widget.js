openerp.olims = function (instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    var _super_getDir = jscolor.getDir.prototype;
    jscolor.getDir = function () {
        var dir = _super_getDir.constructor();
        if (dir.indexOf('olims') === -1) {
            jscolor.dir = 'olims/static/lib/jscolor/';
        }
        return jscolor.dir;
    };

    // instance.web.form.widgets.add('color', 'instance.web.form.FieldColor');

    // instance.web.search.fields.add('color', 'instance.web.search.CharField');

    local.FieldColor = instance.web.form.AbstractField.extend({
        events: {
        'change input': function (e) {
            if (!this.get('effective_readonly')) {
                this.internal_set_value($(e.currentTarget).val());
            }
        }
    },
    init: function() {
        this._super.apply(this, arguments);
        this.set("value", "");
    },
    start: function() {
        this.on("change:effective_readonly", this, function() {
            this.display_field();
            this.render_value();
        });
        this.display_field();
        return this._super();
    },
    display_field: function() {
        this.$el.html(QWeb.render("FieldColor", {widget: this}));
    },
    render_value: function() {
        if (this.get("effective_readonly")) {
            this.$(".oe_field_color_content").css("background-color", this.get("value") || "#FFFFFF");
        } else {
            this.$("input").val(this.get("value") || "#FFFFFF");
        }
    },
    });
    instance.web.form.widgets.add('color', 'instance.olims.FieldColor');

    /*
     * Init jscolor for each editable mode on view form
     */
    instance.web.FormView.include({
        to_edit_mode: function () {
            this._super();
            jscolor.init(this.$el[0]);
        }
    });
};
odoo.define('web_one2many_selectable.form_widgets', function (require) {
"use strict";
var core = require('web.core');
var Model = require('web.Model');
var _t = core._t;
var QWeb = core.qweb;
var FieldOne2Many = core.form_widget_registry.get('one2many');

var One2ManySelectable = FieldOne2Many.extend({
		multi_selection: true,
		init: function() {
	        this._super.apply(this, arguments);
	    },
	    start: function() 
	    {
	    	this._super.apply(this, arguments);
	    	var self=this;
	    	this.$el.prepend(QWeb.render("One2ManySelectable", {widget: this}));
	        this.$el.find(".ep_button_confirm").click(function(){
	        	self.action_selected_lines();
	        });
	        this.$el.find(".ep_button_verify").click(function(){
	        	self.action_verify_selected_lines();
	        });
	   },

	   action_verify_selected_lines:function()
	   {
		   	var self = this;
		   	var data = self.get_selected_ids_one2many();
			var selected_ids = data[0];
			var selected_state = data[2];
			if (selected_ids.length === 0)
			{
					this.do_warn(_t("You must choose at least one record."));
					return false;
			}
			var model_obj=new Model(this.dataset.model);
			for(var i=0; i<selected_ids.length; i++)
			   {
					if (selected_state[i] != "To be verified")
					{
							this.do_warn(_t("Some selected items are not in valid state to verify."));
							return false;
					}
				}
			model_obj.call('verify_analyses_and_ws',[selected_ids],{context:self.dataset.context})
				.then(function(result){
				location.reload();
				});
	   },
	   action_selected_lines: function()
	   {
		   var self = this;
		   var data = self.get_selected_ids_one2many();
		   var selected_ids = data[0];
		   var selected_results = data[1];
		   if (selected_ids.length === 0)
		   {
		   		this.do_warn(_t("You must choose at least one record."));
		   		return false;
		   }
		   var model_obj=new Model(this.dataset.model);
		   for(var i=0; i<selected_ids.length; i++)
		   {
		   	    if (selected_results[i] == ""){
					self.do_warn(_t("Some selected items are missing results " +
               		"Please add results first before proceeding."));
	   				return false;
	   			}
			   if(isNaN(selected_ids[i]))
			   {
			   		this.do_warn(_t("Some selected items have not been saved! " +
	               		"Please save the record first before proceeding."));
		   			return false;
			   }
		   }
		   var validator_promise = model_obj.query(['id','result','Result'])
		   	.filter([['id','in',selected_ids]])
		   	.all()
		   	.then(function(results){
		   		for(var i=0; i<results.length; i++)
		   		{
		   			var res;
		   			if(results[i].hasOwnProperty('result')){
		   				res = results[i].result;
		   			}
		   			else if(results[i].hasOwnProperty('Result')){
		   				res = results[i].Result;
		   			}
		   			if (res !== selected_results[i]){
		   				self.do_warn(_t("Some selected items are not saved " +
	               		"Please save the record first before proceeding."));
		   				return false;
					}
		   		}
		   		return true
			});
		   validator_promise.then(function(isValid) {
			    if (isValid){
			    	model_obj.call('bulk_verify',[selected_ids],{context:self.dataset.context})
					.then(function(result){
						location.reload();
					});
			    }
			});
	   },
	   get_selected_ids_one2many: function ()
	   {
	       var ids =[];
	       var results = [];
	       var states = [];
	       this.$el.find('th.oe_list_record_selector input:checked')
	               .closest('tr').each(function () {
	               	ids.push(parseInt($(this).context.dataset.id));
	               	results.push($(this).find('[data-field]').filter(function() {
					    return $(this).data('field').toLowerCase() == 'result';
					}).text());
					states.push($(this).find('[data-field]').filter(function() {
					    return $(this).data('field').toLowerCase() == 'state';
					}).text());
	       });
	       return [ids,results,states];
	   },
	});
	core.form_widget_registry.add('one2many_selectable', One2ManySelectable);
	return One2ManySelectable;
});