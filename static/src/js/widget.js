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
	    	self.on("change:effective_readonly", this, function(){
	    		if(this.get("effective_readonly"))
	    			self.$(".ep_button_confirm").attr("disabled", "");
	    		else
	    			self.$(".ep_button_confirm").removeAttr("disabled", "");
	    	});
	    	this.$el.prepend(QWeb.render("One2ManySelectable", {widget: this}));
	        this.$el.find(".ep_button_confirm").click(function(){
	        	self.action_selected_lines();
	        });
	   },

	   action_selected_lines: function()
	   {
		   var self = this;
		   var selected_ids = self.get_selected_ids_one2many();
		   if (selected_ids.length === 0)
		   {
		   		this.do_warn(_t("You must choose at least one record."));
		   		return false;
		   }
		   for(var i=0; i<selected_ids.length; i++)
		   {
			   if(isNaN(selected_ids[i]))
			   {
			   		this.do_warn(_t("Some selected items have not been saved! " +
	               		"Please save the record first before proceeding."));
		   			return false;
			   }
		   }
/*		   Uncomment the following lines and put your model name and function name to call your python function */
		    console.log("selected_ids:",selected_ids);
			var model_obj=new Model("olims.ws_manage_results");
			model_obj.call('bulk_verify',[selected_ids],{context:self.dataset.context})
			.then(function(result){
				location.reload();
			});
			
	   },
	   get_selected_ids_one2many: function ()
	   {
	       var ids =[];
	       this.$el.find('th.oe_list_record_selector input:checked')
	               .closest('tr').each(function () {
	               	ids.push(parseInt($(this).context.dataset.id));
	       });
	       return ids;
	   },
	});
	core.form_widget_registry.add('one2many_selectable', One2ManySelectable);
	return One2ManySelectable;
});
