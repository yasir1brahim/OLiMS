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
        }
    });
});
