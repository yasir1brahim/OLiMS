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
