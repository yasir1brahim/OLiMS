odoo.define("web_disable_client_action_group", function(require) {
"use strict";

    var core = require("web.core");
    var Sidebar = require("web.Sidebar");
    var _t = core._t;
    var Model = require("web.Model");
    var session = require("web.session");

    Sidebar.include({
        add_items: function(section_code, items) {
            var self = this;
            var _super = this._super;
            if (session.is_superuser) {
                _super.apply(this, arguments);
            } else {
                var model_res_users = new Model("res.users");
                model_res_users.call("has_group", ["olims.group_clients"]).done(function(is_client) {
                    if (is_client && section_code === "other") {
                        //Leaving this block empty will not create the Action dropdown
                    } else {
                        _super.call(self, section_code, items);
                    }
                });
            }
        },

        add_toolbar: function(toolbar) {

            var self = this;
            var index= 0;
            var item_list = [];
            var self = this;
            var _super = this._super;

            if (session.uid != 1)
            {

                 var model_res_users = new Model("res.users");
                 model_res_users.call("has_group", ["olims.group_cancel_ar_n_sample"]).done(function(has_cancel_rights) {
                    if (has_cancel_rights)
                    {
                        _super.call(self, toolbar);
                    }
            else
            {
                 _.each(['print','action','relate'], function(type) {
                 var items = toolbar[type];

                 if (items)
                 {
                    item_list = [];
                    index = 0;

                    for (var i = 0; i < items.length; i++)
                     {

                            if ((items[i]['model_name'] == 'olims.analysis_request' && (items[i]['name']=='Cancel' )) || (items[i]['model_name'] == 'olims.sample' && items[i]['name']=='Dispose'))
                              continue

                            item_list[index] = {
                                label: items[i]['name'],
                                action: items[i],
                                classname: 'oe_sidebar_' + type
                            };

                        index++;
                    }

                self.add_items(type=='print' ? 'print' : 'other', item_list);
            }
        });

            }

            });
            }

            else
            {
                _super.call(self, toolbar);
            }




    }
    });
});
