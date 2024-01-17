odoo.define('knowsystem.FieldHtml', function (require) {
'use strict';

    var config = require('web.config');
    var core = require('web.core');
    var fieldRegistry = require('web.field_registry');

    var rpc = require("web.rpc");
    var _t = core._t;

    rpc.query({
        model: 'knowsystem.article',
        method: 'get_backend_editor_widget',
        args: [],
    }).then(function(res) {
        if (res) {
            var AceEditor = require('web.basic_fields').AceEditor;
            var KnowSystemFieldHtml = AceEditor.extend({
                init: function () {
                    this._super.apply(this, arguments);  
                    if (!this.record.data.id && this.mode === 'edit' && this.record.context && this.record.context.default_knowdescription) {
                        this.value = this.record.context.default_knowdescription;
                        this.record.context.default_knowdescription = false;
                    }
                    else {
                        this.record.context.default_knowdescription = false;
                        this.value = this.recordData[this.nodeOptions['inline-field']];
                    };
                },          
                _setValue: function (value, options) {
                    var self = this;
                    return this._super.apply(this, arguments).then(function () {
                        var fieldName = self.nodeOptions['inline-field'];
                        self.trigger_up('field_changed', {
                            dataPointID: self.dataPointID,
                            changes: _.object([fieldName], [self.value])
                        });                        
                    })
                },
            });
        }
        else {
            var FieldHtml = require('web_editor.field.html');
            var convertInline = require('web_editor.convertInline');

            var KnowSystemFieldHtml = FieldHtml.extend({
                custom_events: _.extend({}, FieldHtml.prototype.custom_events, {
                    snippets_loaded: '_onSnippetsLoaded',
                }),
                init: function (parent, name, record, options) {
                    // Overwrite to apply our especially prepared snippets
                    this._super.apply(this, arguments);
                    if (!this.nodeOptions.snippets) {
                        this.nodeOptions.snippets = 'knowsystem.knowsystem_snippets';
                    };
                    this.__extraAssetsForIframe = [{
                        jsLibs: ['/knowsystem/static/src/js/knowsystem_snippets.js'],
                    }];
                },
                commitChanges: function () {
                    // Overwrite to save changes into 'readonly' html field
                    var self = this;
                    if (this.mode === 'readonly' || !this.isRendered) {return this._super();}
                    var fieldName = this.nodeOptions['inline-field'];
                    if (this.$content.find('.o_basic_theme').length) {
                        this.$content.find('*').css('font-family', '');
                    }
                    var $editable = this.wysiwyg.getEditable();
                    return this.wysiwyg.saveCroppedImages(this.$content).then(function () {
                        return self.wysiwyg.save().then(function (result) {
                            self._isDirty = result.isDirty;
                            convertInline.attachmentThumbnailToLinkImg($editable);
                            convertInline.fontToImg($editable);
                            convertInline.classToStyle($editable);
                            self.trigger_up('field_changed', {
                                dataPointID: self.dataPointID,
                                changes: _.object([fieldName], [self._unWrap($editable.html())])
                            });
                            if (self._isDirty && self.mode === 'edit') {return self._doAction();}
                        });
                    });
                },
                getDatarecord: function () {
                    // Overwrite to remove value from url (as iframe)
                    return _.omit(this._super(), ['description', 'description_arch', 'attachment_ids']);
                },
                _editableAreaIsEmpty: function ($layout) {
                    // The method to check whether area is empty
                    $layout = $layout || this.$content.find(".o_layout");
                    var $knowSystemWrapper = $layout.children(".o_knowsystem_wrapper");
                    var $knowSystemWrapperContent = $knowSystemWrapper.find('.o_knowsystem_wrapper_td');
                    if (!$knowSystemWrapperContent.length) {$knowSystemWrapperContent = $knowSystemWrapper;}
                    var value;
                    if ($knowSystemWrapperContent.length > 0) {value = $knowSystemWrapperContent.html();
                    } else if ($layout.length) {value = $layout.html();
                    } else {value = this.wysiwyg.getValue();}
                    var blankEditable = "<p><br></p>";
                    return value === "" || value === blankEditable;
                },
                _renderEdit: function () {
                    // Overwrite to take content from 'readonly' field. In case we get context, we also take it from there
                    this._isFromInline = !this.value;
                    if (!this.record.data.id && this.record.context && this.record.context.default_knowdescription) {
                        this.value = this.record.context.default_knowdescription;
                    }
                    else {this.value = this.recordData[this.nodeOptions['inline-field']]};
                    return this._super.apply(this, arguments);
                },
                _renderReadonly: function () {
                    // Overwrite to take content from 'readonly' field
                    this.value = this.recordData[this.nodeOptions['inline-field']];
                    return this._super.apply(this, arguments);
                },
                _renderTranslateButton: function () {
                    // Purposefuly do not add translation button
                    return $();
                },   
                _onLoadWysiwyg: function () {
                    if (this._isFromInline) {this._fromInline();}
                    if (this.snippetsLoaded) {this._onSnippetsLoaded(this.snippetsLoaded);}
                    this._super();
                },
                _onSnippetsLoaded: function (ev) {
                    var self = this;
                    if (!this.$content) {
                        this.snippetsLoaded = ev;
                        return;
                    }
                    var $snippetsSideBar = ev.data;
                    var $snippets = $snippetsSideBar.find(".oe_snippet");
                    var $snippets_menu = $snippetsSideBar.find("#snippets_menu");
                    if (config.device.isMobile) {
                        $snippetsSideBar.hide();
                        this.$content.attr('style', 'padding-left: 0px !important');
                    }
                },
                _onTranslate: function (ev) {
                    // The method to launch translations
                    this.trigger_up('translate', {
                        fieldName: this.nodeOptions['inline-field'],
                        id: this.dataPointID,
                        isComingFromTranslationAlert: false,
                    });
                },
                _onGetRecordInfo: function (event_data) {
                    // The method to get custom record info to media
                    var recordInfo = event_data.data.recordInfo || {};
                    recordInfo.context = this.record.getContext(this.recordParams);
                    recordInfo.res_model = this.model;
                    recordInfo.res_id = this.res_id;
                    event_data.data.callback(recordInfo);
                },
                _getWysiwygOptions: function () {
                    // Fully re-write to activate editor not only in debug mode
                    var self = this;
                    return Object.assign({}, this.nodeOptions, {
                        recordInfo: {
                            context: this.record.getContext(this.recordParams),
                            res_model: this.model,
                            res_id: this.res_id,
                        },
                        noAttachment: this.nodeOptions['no-attachment'],
                        inIframe: !!this.nodeOptions.cssEdit,
                        iframeCssAssets: this.nodeOptions.cssEdit,
                        snippets: this.nodeOptions.snippets,
                        tabsize: 0,
                        height: 180,
                        generateOptions: function (options) {
                            var toolbar = options.toolbar || options.airPopover || {};
                            var para = _.find(toolbar, function (item) {
                                return item[0] === 'para';
                            });
                            if (para && para[1] && para[1].indexOf('checklist') === -1) {
                                para[1].splice(2, 0, 'checklist');
                            }
                            options.codeview = true;
                            var view = _.find(toolbar, function (item) {
                                return item[0] === 'view';
                            });
                            if (view) {
                                if (!view[1].includes('codeview')) {
                                    view[1].splice(-1, 0, 'codeview');
                                }
                            } else {
                                toolbar.splice(-1, 0, ['view', ['codeview']]);
                            }
                            options.prettifyHtml = true;
                            return options;
                        },
                    });
                },
            });        
        };

        fieldRegistry.add('knowsystem_html_editor', KnowSystemFieldHtml);
        return KnowSystemFieldHtml;

    });
});


// _createWysiwygIntance