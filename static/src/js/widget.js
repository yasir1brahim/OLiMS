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
			   if(isNaN(selected_ids[i]))
			   {
			   		this.do_warn(_t("Some selected items have not been saved! " +
	               		"Please save the record first before proceeding."));
		   			return false;
			   }
		   }
		   var validator_promise = model_obj.query(['id','result_string','Result_string'])
		   	.filter([['id','in',selected_ids]])
		   	.all()
		   	.then(function(results){
		   		for(var i=0; i<results.length; i++)
		   		{
		   			var res;
					if(results[i].hasOwnProperty('result_string')){
					res = results[i].result_string;
		   			}
					else if(results[i].hasOwnProperty('Result_string')){
					res = results[i].Result_string;
		   			}
					//res = res.toFixed(2)
		   			var results_val = (selected_results[i].result).replace(/,/g , "");
		   			if (res !== results_val){
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
					states.push($(this).find('[data-field]').filter(function() {
					    return $(this).data('field').toLowerCase() == 'state';
					}).text());
					results.push({id:parseInt($(this).context.dataset.id), result:$(this).find('[data-field]').filter(function() {
					    return $(this).data('field').toLowerCase() == 'result_string';
					}).text()});

	       });
	       results.sort(function(a, b) {
    			return a.id - b.id;
				});
	       return [ids,results,states];
	   },
	});
	core.form_widget_registry.add('one2many_selectable', One2ManySelectable);
	return One2ManySelectable;
});


odoo.define('web_many2many_selectable.form_widgets', function (require) {
"use strict";
var core = require('web.core');
var Model = require('web.Model');
var _t = core._t;
var QWeb = core.qweb;
var FieldMany2Many = core.form_widget_registry.get('many2many');

function RemoveSelectedRows() {
  if($('.oe_list_record_selector')[0].checked == true)
        {
        $('.oe_list_record_selector')[0].checked = false
        }
        $('.oe_form_button_save').click()
}

var Many2ManySelectable = FieldMany2Many.extend({
		multi_selection: true,
		init: function() {
	        this._super.apply(this, arguments);
	    },
	    start: function()
	    {
	    	this._super.apply(this, arguments);
	    	var self=this;
	    	this.$el.prepend(QWeb.render("Many2ManySelectable", {widget: this}));
	        this.$el.find(".ep_button_confirm").click(function(){
	        	self.action_selected_lines();
	        });
	   },


	   action_selected_lines: function()
	   {
		var self = this;
		var selected_ids = self.get_selected_ids_many2many();
		if (selected_ids.length === 0)
		{
		    this.do_warn(_t("You must choose at least one record."));
		    return false;
		}
		else if (selected_ids.length > 0){
		var model_obj=new Model(this.dataset.model); //you can hardcode model name as: new Model("module.model_name");
                if (!(confirm(_t("Do you really want to remove these records?")))) {
                return;
                }
		//you can change the function name below
		var FunctionToBeCalled =''
		if (model_obj.name == 'olims.analysis_profile')
		 { FunctionToBeCalled = 'delete_client_analysis_profile'  }

		else if (model_obj.name == 'olims.add_analysis')
		 { FunctionToBeCalled = 'delete_ars_for_worksheet'  }

		 var context = JSON.stringify(self.dataset.context)
		 var active_id_index = context.search("active_id")+11
		 var active_id_string = context.substr(active_id_index,context.length-1)
		 var active_record_id = active_id_string.substr(0,active_id_string.search(",")-0)

		model_obj.call(FunctionToBeCalled,{active_id :active_record_id,selected_ids:selected_ids})
		.then(function(result){
		RemoveSelectedRows();
		});
        }
	   },
	   get_selected_ids_many2many: function ()
	   {
	       var ids =[];
	       this.$el.find('th.oe_list_record_selector input:checked')
	               .closest('tr').each(function () {
	               	ids.push(parseInt($(this).context.dataset.id));
	       });
	       return ids;
	   },
	});
	core.form_widget_registry.add('many2many_selectable', Many2ManySelectable);
	return Many2ManySelectable;
});


odoo.define('web.DuplicateVisibility',function (require) {
    "use strict";

    var core = require('web.core');
    var Sidebar = require('web.Sidebar');
    var FormView = require('web.FormView');

    var _t = core._t;

    var DuplicateVisibility = FormView.include({
        /**
         * Instantiate and render the sidebar if a sidebar is requested
         * Sets this.sidebar
         * @param {jQuery} [$node] a jQuery node where the sidebar should be inserted
         * $node may be undefined, in which case the FormView inserts the sidebar in a
         * div of its template
         **/
        render_sidebar: function($node) {
            var res = this._super.apply(this, arguments);
            if (this.sidebar) {
                if(!this.is_action_enabled('duplicate') &&
                   this.sidebar.items.hasOwnProperty('other')){
                    this.sidebar.items.other = this.sidebar.items.other.filter(
                        function(item){
                            return item.label !== _t("Duplicate");
                        }
                    );
                    this.sidebar.redraw();
                }
            }
            return res;
        },
    });

});

odoo.define('web.FreezeTableHeader',function (require) {
    "use strict";

    var core = require('web.core');
    var ListView = require('web.ListView');

    var _t = core._t;

    var FreezeTableHeader = ListView.include({
        load_list: function () {
            var self = this;
            self._super.apply(this, arguments);
            setTimeout(function(){
                var scrollArea = self.$el.parents('.oe-view-manager.oe_view_manager_current').find('.oe-view-manager-content .oe-view-manager-view-list')[0];
                if(scrollArea){
                    self.$el.find('table.oe_list_content').each(function(){
                        $(this).stickyTableHeaders({scrollableArea: scrollArea, leftOffset: scrollArea, "fixedOffset": 1 })
                    });
                }
         }, 1000);

        },
    });

});
