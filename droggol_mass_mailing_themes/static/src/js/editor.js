odoo.define('droggol_mass_mail_themes.colorpicker.option', function (require) {
'use strict';

var options = require('web_editor.snippets.options');
var ColorpickerDialog = require('web.ColorpickerDialog');

options.registry.colorpicker = options.registry.colorpicker.extend({
    events: _.extend({}, options.registry.colorpicker.prototype.events || {}, {
        'click .d_add_custom_color': '_onCustomColorButtonClick',
    }),
    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.customColors = [];
    },
    start: function () {
        this._renderCustomColors();
        return this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    onFocus: function () {
        this._renderCustomColors();
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------
     /**
     * Renderer all custom colors from the page and add to dropdown.
     *
     * @private
     */
    _renderCustomColors: function () {
        var self = this;
        this.$el.find('.d_custom_color').remove();
        var $editable = window.__EditorMenuBar_$editable || $();
        this.customColors = _.chain($editable.find('.d_custom_snippet_bg')).map(function (el) {
            return el.style.backgroundColor;
        }).uniq().value();
        _.each(this.customColors, function (color) {
            var classes = 'd_custom_color';
            if (self.$target.css('background-color') === color) {
                classes += ' selected';
            }
            var $btn = $('<button/>', {
                class: classes,
                style: 'background-color:' + color + ';',
            });
            $btn.insertBefore(self.$el.find('.d_add_custom_color'));
        });
    },
    /**
     * Called when the Add Custom Color button clicked.
     *
     * @private
     */
    _onCustomColorButtonClick: function () {
        var self = this;
        var colorpicker = new ColorpickerDialog(this, {});
        colorpicker.on('colorpicker:saved', this, function (ev) {
            self.$target
                .removeClass(self.classes)
                .addClass('d_custom_snippet_bg')
                .css('background-color', ev.data.cssColor);
            this.$el.find('.colorpicker button.selected').removeClass('selected');
            self.customColors.push(ev.data.cssColor);
            self._renderCustomColors();
            self.$target.closest('.o_editable').trigger('content_changed');
            self.$target.trigger('background-color-event', false);
        });
        colorpicker.open();
    },
    /**
     * @override
     */
    _onColorButtonEnter: function (ev) {
        if ($(ev.target).hasClass('d_custom_color')) {
            this.$target
                .removeClass(this.classes)
                .css('background-color', ev.currentTarget.style.backgroundColor);
        }
        this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    _onColorButtonLeave: function () {
        var $selected = this.$el.find('.colorpicker button.selected.d_custom_color');
        if ($selected.length) {
            this.$target.removeClass(this.classes);
            this.$target.css('background-color', $selected.css('background-color'));
            this.$target.trigger('background-color-event', 'reset');
        } else {
            this._super.apply(this, arguments);
        }
    },
    /**
     * @override
     */
    _onColorResetButtonClick: function () {
        this.$target.removeClass('d_custom_snippet_bg');
        this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    _onColorButtonClick: function (ev) {
        if ($(ev.target).hasClass('d_custom_color')) {
            this.$target.addClass('d_custom_snippet_bg');
        } else {
            this.$target.removeClass('d_custom_snippet_bg');
        }
        if ($(ev.currentTarget).hasClass('d_add_custom_color')) {
            return;
        }
        this._super.apply(this, arguments);
    },
});
});
