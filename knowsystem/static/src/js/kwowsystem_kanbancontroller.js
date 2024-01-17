odoo.define('knowsystem.kwowsystem_kanbancontroller', function (require) {
"use strict";

    var core = require('web.core');
    var session = require('web.session');
    var KanbanController = require('web.KanbanController');
    var dialogs = require('web.view_dialogs');
    var DataExport = require('web.DataExport');

    var qweb = core.qweb;
    var _t = core._t;

    var KnowSystemKanbanController = KanbanController.extend({
        events: _.extend({}, KanbanController.prototype.events, {
            "change #knowsort": "_applyKnowSorting",
            "click .knowreverse_sort": "_applyReverseKnowSorting",
            "click .knowselect_all": "addAll2SelectedArticles",
            "click #add_know_section": "_addRootSection",
            "click #add_know_tag": "_addRootTag",
            "click #add_know_type": "_addRootType",
            "click .clear_sections": "_clearSections",
            "click .clear_tags": "_clearTags",
            "click .clear_types": "_clearTypes",
            "click .clear_selected_articles": "clearAllSelectedArticles",
            "click .knowsystem_article_selected_row": "_removeArticleSelected",
            "click .selected_articles_update": "_massUpdateSelectedArticles",
            "click .selected_articles_pdf": "_onKnowSystemPrint",
            "click .selected_articles_export": "_onKnowSystemExport",
            "click .selected_articles_add_to_tour": "_onAddToTour",
            "click .selected_articles_favourite": "_addSelectedArticles2Favourite",
            "click .selected_articles_follow": "_followSelectedArticles",
            "click .selected_articles_unfollow": "_unFollowSelectedArticles",
            "click .selected_articles_archive": "_archiveSelectedArticles",
            "click .selected_articles_publish": "_archiveSelectedPublish",
            "click .selected_articles_duplicate": "_copySelectedArticles",
            "click #add_new_tour": "_addNewTour",
            "click .play_tour": "_onTourClick",
            "contextmenu .play_tour": "_onTourRightClick",
        }),
        jsLibs: [
            '/knowsystem/static/lib/jstree/jstree.js',
        ],
        cssLibs: [
            '/knowsystem/static/lib/jstree/themes/default/style.css',
        ],
        custom_events: _.extend({}, KanbanController.prototype.custom_events, {
            select_record: '_articleSelected',
        }),
        init: function () {
            this._super.apply(this, arguments);
            this.nonavigation_update = false;
            this.selectedRecords = [];
            this.navigationExist = false;
        },
        start: function () {
            this.$('.o_content').addClass('knowsystem_articles d-flex');
            return this._super.apply(this, arguments);
        },
        _update: function () {
            // Re-write to render left navigation panel
            var self = this;
            var def = $.Deferred();
            this._super.apply(this, arguments).then(function (res) {
                var state = self.model.get(self.handle);
                if (self.navigationExist) {
                    def.resolve(res);
                }
                else {
                    self._renderNavigationPanel().then(function () {
                        def.resolve(res);
                    });
                };
                self.renderer.updateSelection(self.selectedRecords);
            });
            return def
        },
        update: function (params, options) {
            // Re-write to avoid rerendering left navigation panel
            var domain = params.domain || []
            this.nonavigation_update = true;
            params.knowSystemDomain = this._renderArticles();
            return this._super(params, options);
        },
        renderButtons: function ($node) {
            // Re write to add custom buttons to
            var self = this;
            $.when(this._super.apply(this, arguments)).then(function () {
                if (self.is_action_enabled('create') && self.modelName == 'knowsystem.article') {
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_create_from_template',
                        self._onKnowSystemCreateFromTemplate.bind(self)
                    );
                };
            });
        },
        _reloadAfterButtonClick: function (kanbanRecord, params) {
            // Re write to force reload
            var self = this;
            $.when(this._super.apply(this, arguments)).then(function () {
                self.reload();
            });
        },
        _applyKnowSorting: function(event, passed) {
            // The method to re-order articles based on selected key
            event.stopPropagation();
            var self = this;
            var sortKey = event.currentTarget.value;
            var data = this.model.get(this.handle);
            var list = this.model.localData[data.id];
            var asc = true;
            if (passed && passed.reverse) {
                if (list.orderedBy.length != 0 && list.orderedBy[0].name == sortKey) {
                    asc = list.orderedBy[0].asc;
                }
                else {
                    asc = false;
                };
            };
            // To hack default 'desc' instead of 'asc'
            list.orderedBy = [];
            list.orderedBy.push({name: sortKey, asc: asc});
            this.model.setSort(data.id, sortKey).then(function () {
                self.reload({});
            });
        },
        _applyReverseKnowSorting: function(event) {
            // The method to reverse the sorting
            event.stopPropagation();
            this.$("#knowsort").trigger("change", {"reverse": true});
        },
        _renderSections: function () {
            // The method to retrieve sections for a current user
            var self = this;
            self.$('#sections').jstree('destroy');
            var defer = $.Deferred();
            self._rpc({
                model: "knowsystem.section",
                method: 'return_nodes',
                args: [],
            }).then(function (availableSections) {
                var jsTreeOptions = {
                    'core' : {
                        'themes': {'icons': false},
                        'check_callback' : true,
                        'data': availableSections,
                        "multiple" : true,
                        "strings": {"New node": _t('New Section'),}
                    },
                    "plugins" : [
                        "contextmenu",
                        "checkbox",
                        "state",
                        "search",
                    ],
                    "state" : { "key" : "sections" },
                    "checkbox" : {
                        "three_state" : false,
                        "cascade": "down",
                        "tie_selection" : false,
                    },
                    "contextmenu": {
                        "select_node": false,
                        "items": function($node) {
                            var tree = $("#sections").jstree(true);
                            return {
                                "Print": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Print"),
                                    "action": function (obj) {
                                        var resId = parseInt($node.id);
                                        self._printBatch(resId, false);
                                    }
                                },
                            }
                        },
                    },
                }
                if (self.is_action_enabled("create")) {
                    jsTreeOptions.plugins = [
                        "checkbox",
                        "contextmenu",
                        "dnd",
                        "state",
                        "search",
                    ];
                    jsTreeOptions.contextmenu = {
                        "select_node": false,
                        "items": function($node) {
                            var tree = $("#sections").jstree(true);
                            return {
                                "Create": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Create"),
                                    "action": function (obj) {
                                        $node = tree.create_node($node);
                                        tree.edit($node);
                                    }
                                },
                                "Rename": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Rename"),
                                    "action": function (obj) {
                                        tree.edit($node);
                                    }
                                },
                                "Edit": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Edit"),
                                    "action": function (obj) {
                                        var resId = parseInt($node.id);
                                        self._onEditSectionForm(resId);
                                    }
                                },
                                "Print": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Print"),
                                    "action": function (obj) {
                                        var resId = parseInt($node.id);
                                        self._printBatch(resId, false);
                                    }
                                },
                                "Remove": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Archive"),
                                    "action": function (obj) {
                                        tree.delete_node($node);
                                    }
                                },
                            };
                        },
                    };
                };
                var ref = self.$('#sections').jstree(jsTreeOptions);
                if (self.is_action_enabled("create")) {
                    self.$('#sections').on("rename_node.jstree", self, function (event, data) {
                        // This also includes 'create' event. Since each time created, a node is updated then
                        self._updateNode(event, data, 'knowsystem.section', false);
                    });
                    self.$('#sections').on("move_node.jstree", self, function (event, data) {
                        self._updateNode(event, data, 'knowsystem.section', true);
                    });
                    self.$('#sections').on("delete_node.jstree", self, function (event, data) {
                        self._deleteNode(event, data, 'knowsystem.section');
                    });
                    self.$('#sections').on("copy_node.jstree", self, function (event, data) {
                        self._updateNode(event, data, 'knowsystem.section', true);
                    });
                };
                self.$('#sections').on("state_ready.jstree", self, function (event, data) {
                    // We register 'checks' only after restoring the tree to avoid multiple checked events
                    self.$('#sections').on("check_node.jstree uncheck_node.jstree", self, function (event, data) {
                        self.reload();
                    })
                });
                defer.resolve();
            });
            return defer
        },
        _renderTags: function (defer) {
            // The method to retrieve tags for a current user
            var self = this;
            self.$('#tags').jstree('destroy');
            var defer = $.Deferred();
            self._rpc({
                model: "knowsystem.tag",
                method: 'return_nodes',
                args: [],
            }).then(function (availableTags) {
                var jsTreeOptions = {
                    'core' : {
                        'themes': {'icons': false},
                        "multiple" : true,
                        'check_callback' : true,
                        'data': availableTags,
                        "strings": {"New node": _t('New Tag'),}
                    },
                    "plugins" : [
                        "contextmenu",
                        "checkbox",
                        "state",
                        "search",
                    ],
                    "state" : { "key" : "tags" },
                    "checkbox" : {
                        "three_state" : false,
                        "cascade": "down",
                        "tie_selection" : false,
                    },
                    "contextmenu": {
                        "select_node": false,
                        "items": function($node) {
                            var tree = $("#tags").jstree(true);
                            return {
                                "Print": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Print"),
                                    "action": function (obj) {
                                        var resId = parseInt($node.id);
                                        self._printBatch(false, resId);
                                    }
                                },
                            }
                        },
                    },
                };
                if (self.is_action_enabled("create")) {
                    jsTreeOptions.plugins = [
                        "checkbox",
                        "contextmenu",
                        "dnd",
                        "state",
                        "search",
                    ];
                    jsTreeOptions.contextmenu = {
                        "select_node": false,
                        "items": function($node) {
                            var tree = $("#tags").jstree(true);
                            return {
                                "Create": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Create"),
                                    "action": function (obj) {
                                        $node = tree.create_node($node);
                                        tree.edit($node);
                                    }
                                },
                                "Rename": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Rename"),
                                    "action": function (obj) {
                                        tree.edit($node);
                                    }
                                },
                                "Edit": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Edit"),
                                    "action": function (obj) {
                                        var resId = parseInt($node.id);
                                        self._onEditTagForm(resId);
                                    }
                                },
                                "Print": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Print"),
                                    "action": function (obj) {
                                        var resId = parseInt($node.id);
                                        self._printBatch(false, resId);
                                    }
                                },
                                "Remove": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Archive"),
                                    "action": function (obj) {
                                        tree.delete_node($node);
                                    }
                                },
                            };
                        },
                    };
                };
                var ref = self.$('#tags').jstree(jsTreeOptions);
                if (self.is_action_enabled("create")) {
                    self.$('#tags').on("rename_node.jstree", self, function (event, data) {
                        // This also includes 'create' event. Since each time created, a node is updated then
                        self._updateNode(event, data, 'knowsystem.tag', false);
                    });
                    self.$('#tags').on("move_node.jstree", self, function (event, data) {
                        self._updateNode(event, data, 'knowsystem.tag', true);
                    });
                    self.$('#tags').on("delete_node.jstree", self, function (event, data) {
                        self._deleteNode(event, data, 'knowsystem.tag');
                    });
                    self.$('#tags').on("copy_node.jstree", self, function (event, data) {
                        self._updateNode(event, data, 'knowsystem.tag', true);
                    });
                };
                self.$('#tags').on("state_ready.jstree", self, function (event, data) {
                    self.reload({"domain": self.model.get(self.handle).domain});
                    // We register 'checks' only after restoring the tree to avoid multiple checked events
                    self.$('#tags').on("check_node.jstree uncheck_node.jstree", self, function (event, data) {
                        self.reload();
                    });
                });
                defer.resolve();
            });
            return defer
        },
        _renderTypes: function (defer) {
            // The method to retrieve types for a current user
            var self = this;
            self.$('#know_types').jstree('destroy');
            var defer = $.Deferred();
            self._rpc({
                model: "knowsystem.article",
                method: 'action_return_types',
                args: [],
            }).then(function (availableTypes) {
                var jsTreeOptions = {
                    'core' : {
                        'themes': {'icons': false},
                        "multiple" : true,
                        'check_callback' : true,
                        'data': availableTypes,
                    },
                    "plugins" : [
                        "contextmenu",
                        "checkbox",
                        "state",
                        "search",
                    ],
                    "state" : { "key" : "know_types" },
                    "checkbox" : {
                        "three_state" : false,
                        "cascade": "down",
                        "tie_selection" : false,
                    },
                    "contextmenu": {
                        "select_node": false,
                        "items": function($node) {
                            var tree = $("#know_types").jstree(true);
                            return {}
                        },
                    },
                };
                if (self.is_action_enabled("delete")) {
                    jsTreeOptions.plugins = [
                        "checkbox",
                        "contextmenu",
                        "dnd",
                        "state",
                        "search",
                    ];
                    jsTreeOptions.contextmenu = {
                        "select_node": false,
                        "items": function($node) {
                            var tree = $("#know_types").jstree(true);
                            return {
                                "Create": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Create"),
                                    "action": function (obj) {
                                        $node = tree.create_node($node);
                                        tree.edit($node);
                                    }
                                },
                                "Rename": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Rename"),
                                    "action": function (obj) {
                                        tree.edit($node);
                                    }
                                },
                                "Edit": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Edit"),
                                    "action": function (obj) {
                                        var resId = parseInt($node.id);
                                        self._onEditTypeForm(resId);
                                    }
                                },
                                "Remove": {
                                    "separator_before": false,
                                    "separator_after": false,
                                    "label": _t("Archive"),
                                    "action": function (obj) {
                                        tree.delete_node($node);
                                    }
                                },
                            };
                        },
                    };
                };
                var ref = self.$('#know_types').jstree(jsTreeOptions);
                if (self.is_action_enabled("delete")) {
                    self.$('#know_types').on("rename_node.jstree", self, function (event, data) {
                        // This also includes 'create' event. Since each time created, a node is updated then
                        self._updateNode(event, data, 'article.custom.type', false);
                    });
                    self.$('#know_types').on("move_node.jstree", self, function (event, data) {
                        self._updateNode(event, data, 'article.custom.type', true);
                    });
                    self.$('#know_types').on("delete_node.jstree", self, function (event, data) {
                        self._deleteNode(event, data, 'article.custom.type');
                    });
                    self.$('#know_types').on("copy_node.jstree", self, function (event, data) {
                        self._updateNode(event, data, 'article.custom.type', true);
                    });
                };
                self.$('#know_types').on("state_ready.jstree", self, function (event, data) {
                    // We register 'checks' only after restoring the tree to avoid multiple checked events
                    self.$('#know_types').on("check_node.jstree uncheck_node.jstree", self, function (event, data) {
                        self.reload();
                    });
                });
                defer.resolve();
            });
            return defer
        },
        _renderTours: function() {
            // The method to render tours
            var self = this;
            var def = $.Deferred();
            self._rpc({
                model: "knowsystem.tour",
                method: 'return_tours',
                args: [[]],
            }).then(function (availableTours) {
                if (!availableTours) {
                    var tours = qweb.render('KnowSystemTours', {
                        "show_tour": false,
                        "tours": [],
                        "right_for_delete": self.is_action_enabled('delete'),
                    });
                }
                else {
                    var tours = qweb.render('KnowSystemTours', {
                        "show_tour": true,
                        "tours": availableTours,
                        "right_for_delete": self.is_action_enabled('delete'),
                    });
                };
                self.$('#knowtours')[0].innerHTML = tours;
                def.resolve();
            });
            return def
        },
        _renderNavigationPanel: function () {
            // The method to render left navigation panel
            var self = this;
            var scrollTop = self.$('.knowsystem_navigation_panel').scrollTop();
            self.$('.knowsystem_navigation_panel').remove();
            var navigationElements = {
                "right_for_create": self.is_action_enabled('create'),
                "right_for_delete": self.is_action_enabled('delete'),
            };
            var $navigationPanel = $(qweb.render('KnowNavigationPanel', navigationElements));
            self.$('.o_content').prepend($navigationPanel);
            var def = $.Deferred()
            self._renderTours().then(function () {
                self._renderSections().then(function () {
                    self._renderTypes().then(function () {
                        self._renderTags().then(function () {
                            def.resolve();
                        });
                    });
                });
            });
            self.$('.knowsystem_navigation_panel').scrollTop(scrollTop || 0);
            self.navigationExist = true;
            return def
        },
        _renderRightNavigationPanel: function () {
            // The method to render right navigation panel
            var self = this;
            var scrollTop = self.$('.knowsystem_right_navigation_panel').scrollTop();
            self.$('.knowsystem_right_navigation_panel').remove();
            var selectedRecords = this.selectedRecords;
            if (selectedRecords.length) {
                self._rpc({
                    model: "knowsystem.article",
                    method: 'return_selected_articles',
                    args: [this.selectedRecords],
                    context: {},
                }).then(function (articles) {
                    var $navigationPanel = $(qweb.render(
                        'KnowRightNavigationPanel', {
                            "articles": articles[0],
                            "count_art": articles[0].length,
                            "right_for_create": self.is_action_enabled('create'),
                            "right_for_delete": self.is_action_enabled('delete'),
                            "knowsystem_website": articles[1],
                        })
                    );
                    self.$('.o_content').append($navigationPanel);
                    self.$('.knowsystem_right_navigation_panel').scrollTop(scrollTop || 0);
                });
            }
        },
        _renderArticles: function () {
            // The method to prepare new filters and trigger articles rerender
            var self = this;
            var domain = [];
            var refS = self.$('#sections').jstree(true),
                checkedSections = refS.get_checked(),
                checkedSectionsIDS = checkedSections.map(function(item) {
                    return parseInt(item, 10);
                });
            if (checkedSectionsIDS.length != 0) {
                domain.push(['section_id', 'in', checkedSectionsIDS]);
            }
            var refT = self.$('#tags').jstree(true);
            if (refT) {
                var checkedTags = refT.get_checked(),
                tagsLength = checkedTags.length;
                if (tagsLength != 0) {
                    var iterator = 0;
                    while (iterator != tagsLength-1) {
                        domain.push('|');
                        iterator ++;
                    }
                    _.each(checkedTags, function (tag) {
                        if (tag.length) {
                            domain.push(['tag_ids', 'in', parseInt(tag)]);
                        }
                    });
                };
            };
            var refTy = self.$('#know_types').jstree(true);
            if (refTy) {
                var checkedTypes = refTy.get_checked(),
                    checkedTypesIDS = checkedTypes.map(function(item) {
                        return parseInt(item, 10);
                    });
                if (checkedTypesIDS.length != 0) {
                    domain.push(['custom_type_id', 'in', checkedTypesIDS]);
                }
            };
            return domain
        },
        _onEditSectionForm: function(resID) {
            var self = this;
            self._rpc({
                model: "knowsystem.section",
                method: 'return_edit_form',
                args: [[]],
            }).then(function (view_id) {
                var onSaved = function(record) {
                    self._renderSections();
                };
                new dialogs.FormViewDialog(self, {
                    res_model: "knowsystem.section",
                    title: _t("Edit Section"),
                    view_id: view_id,
                    res_id: resID,
                    readonly: false,
                    shouldSaveLocally: false,
                    on_saved: onSaved,
                }).open();
            });
        },
        _onEditTagForm: function(resID) {
            var self = this;
            self._rpc({
                model: "knowsystem.tag",
                method: 'return_edit_form',
                args: [[]],
            }).then(function (view_id) {
                var onSaved = function(record) {
                    self._renderTags();
                };
                new dialogs.FormViewDialog(self, {
                    res_model: "knowsystem.tag",
                    title: _t("Edit Tag"),
                    view_id: view_id,
                    res_id: resID,
                    readonly: false,
                    shouldSaveLocally: false,
                    on_saved: onSaved,
                }).open();
            });
        },
        _onEditTypeForm: function(resID) {
            var self = this;
            self._rpc({
                model: "knowsystem.article",
                method: 'return_type_edit_form',
                args: [[]],
            }).then(function (view_id) {
                if (view_id) {
                    var onSaved = function(record) {
                        self._renderTypes();
                    };
                    new dialogs.FormViewDialog(self, {
                        res_model: "article.custom.type",
                        title: _t("Edit Type"),
                        view_id: view_id,
                        res_id: resID,
                        readonly: false,
                        shouldSaveLocally: false,
                        on_saved: onSaved,
                    }).open();
                };
            });
        },
        _printBatch: function(section, tag) {
            var self = this;
            self._rpc({
                model: "knowsystem.article",
                method: 'print_articles_batch',
                args: [[], section, tag],
            }).then(function (action_id) {
                self.do_action(action_id);
            });
        },
        _updateNode: function (event, data, model, position) {
            // The method to trigger update of jstree node - of section or tag
            var self = this;
            if (position) {
                position = parseInt(data.position);
            }
            if (data.node.id === parseInt(data.node.id).toString()) {
                this._rpc({
                    model: model,
                    method: 'update_node',
                    args: [[parseInt(data.node.id)], data.node, position],
                });
            }
            else {
                var thisElId = data.node.id;
                this._rpc({
                    model: model,
                    method: 'create_node',
                    args: [data.node],
                }).then(function (new_id) {
                    // To apply real ids, not jstree ids
                    if (model == "knowsystem.section") {
                        self._renderSections();
                    };
                    if (model == "knowsystem.tag") {
                        self._renderTags();
                    };
                    if (model == "article.custom.type") {
                        self._renderTypes();
                    };
                });
            };
        },
        _deleteNode: function (event, data, model) {
            // The method to trigger unlink of jstree node - of section or tag
            var self = this;
            this._rpc({
                model: model,
                method: 'delete_node',
                args: [[parseInt(data.node.id)]],
            });
        },
        _addRootSection: function(event) {
            // The method to add a new root section
            var self = this;
            var ref = self.$('#sections').jstree(true),
                sel = ref.get_selected();
            sel = ref.create_node('#');
            if(sel) {
                ref.edit(sel);
            }
        },
        _addRootTag: function(event) {
            // The method to add a new root section
            var self = this;
            var ref = self.$('#tags').jstree(true),
                sel = ref.get_selected();
            sel = ref.create_node('#');
            if(sel) {
                ref.edit(sel);
            }
        },
        _addRootType: function(event) {
            // The method to add a new root section
            var self = this;
            var ref = self.$('#know_types').jstree(true),
                sel = ref.get_selected();
            sel = ref.create_node('#');
            if(sel) {
                ref.edit(sel);
            }
        },
        _clearSections: function(event) {
            // The method clear all checked sections
            var self = this;
            var ref = self.$('#sections').jstree(true);
            ref.uncheck_all();
            ref.save_state()
            self.reload();
        },
        _clearTags: function(event) {
            // The method clear all checked tags
            var self = this;
            var ref = self.$('#tags').jstree(true);
            ref.uncheck_all();
            ref.save_state()
            self.reload();
        },
        _clearTypes: function(event) {
            // The method clear all checked types
            var self = this;
            var ref = self.$('#know_types').jstree(true);
            ref.uncheck_all();
            ref.save_state()
            self.reload();
        },        
        _onKnowSystemCreateFromTemplate: function(event) {
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'select_template',
                args: [[]],
                context: {},
            }).then(function (res) {
                self.do_action(res);
            });
        },
        _articleSelected: function(event) {
            // The method to add a new root section
            event.stopPropagation();
            var eventData = event.data;
            var addToSelection = eventData.selected;
            if (addToSelection) {
                this.selectedRecords.push(eventData.resID);
            }
            else {
                this.selectedRecords = _.without(this.selectedRecords, eventData.resID);
            };
            this._renderRightNavigationPanel();
        },
        addAll2SelectedArticles: function(event) {
            // The method to add all articles found to the selection
            event.stopPropagation();
            var self = this;
            var alreadySelected = this.selectedRecords;
            var data = this.model.get(this.handle);
            var list = this.model.localData[data.id];
            // We can't use res_ids since it only the first page --> so we rpc search
            this._rpc({
                model: "knowsystem.article",
                method: 'rerurn_all_pages_ids',
                args: [alreadySelected, list.domain],
                context: {},
            }).then(function (resIDS) {
                self.selectedRecords = resIDS;
                self.renderer.updateSelection(resIDS);
                self._renderRightNavigationPanel();
            });
        },
        clearAllSelectedArticles: function(event) {
            event.stopPropagation();
            this.selectedRecords = [];
            this.renderer.updateSelection(this.selectedRecords);
            this._renderRightNavigationPanel();
        },
        _removeArticleSelected: function(event) {
            // The method to remove this article from selected
            event.stopPropagation();
            var resID = parseInt(event.currentTarget.id);
            this.selectedRecords = _.without(this.selectedRecords, resID);
            this.renderer.updateSelection(this.selectedRecords);
            this._renderRightNavigationPanel();
        },
        _massUpdateSelectedArticles: function(event) {
            // The method to open mass update wizard
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'return_mass_update_wizard',
                args: [this.selectedRecords],
                context: {},
            }).then(function (view_id) {
                var onSaved = function(record) {
                    self.reload();
                };
                new dialogs.FormViewDialog(self, {
                    res_model: "article.update",
                    context: {'default_articles': self.selectedRecords.join()},
                    title: _t("Update articles"),
                    view_id: view_id,
                    readonly: false,
                    shouldSaveLocally: false,
                    on_saved: onSaved,
                }).open();
            });
        },
        _onAddToTour: function(event) {
            // The method to open adding to tour wizard
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'return_add_to_tour_wizard',
                args: [this.selectedRecords],
                context: {},
            }).then(function (view_id) {
                var onSaved = function(record) {
                    var tourId = record.data.tour_id.res_id;
                    self._rpc({
                        model: "knowsystem.tour",
                        method: 'return_form_view',
                        args: [[tourId]],
                        context: {},
                    }).then(function (action) {
                        self.do_action(action);
                    });
                };
                new dialogs.FormViewDialog(self, {
                    res_model: "add.to.tour",
                    context: {'default_articles': self.selectedRecords.join()},
                    title: _t("Add to tour"),
                    view_id: view_id,
                    readonly: false,
                    shouldSaveLocally: false,
                    on_saved: onSaved,
                }).open();
            });
        },
        _onKnowSystemPrint: function(event) {
            // event.stopPropagation();
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'save_as_pdf',
                args: [this.selectedRecords],
                context: {},
            }).then(function (action_id) {
                self.do_action(action_id);
            });
        },
        _onKnowSystemExport: function(event) {
            // The method to launch standard Odoo export
            var record = this.model.get(this.handle);
            var ExportFields = ["name", "description", "indexed_description", "kanban_description", "section_id", "tag_ids"]
            new DataExport(this, record, ExportFields, this.renderer.state.groupedBy, this.getActiveDomain(), this.selectedRecords).open();
        },
        getActiveDomain: function () {
            // The method is required to construct export popup
            return [["id", "in", this.selectedRecords]];
        },
        _addSelectedArticles2Favourite: function(event) {
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'mass_add_to_favourites',
                args: [this.selectedRecords],
                context: {},
            }).then(function () {
                self.reload();
            });
        },
        _followSelectedArticles: function(event) {
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'mass_follow_articles',
                args: [this.selectedRecords],
                context: {},
            }).then(function () {
                self.reload();
            });
        },
        _unFollowSelectedArticles: function(event) {
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'mass_unfollow_articles',
                args: [this.selectedRecords],
                context: {},
            }).then(function () {
                self.reload();
            });
        },
        _archiveSelectedArticles: function(event) {
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'mass_archive',
                args: [this.selectedRecords],
                context: {},
            }).then(function () {
                self.reload();
            });
        },
        _archiveSelectedPublish: function(event) {
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'mass_publish',
                args: [this.selectedRecords],
                context: {},
            }).then(function () {
                self.reload();
            });
        },
        _copySelectedArticles: function(event) {
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'mass_copy',
                args: [this.selectedRecords],
                context: {},
            }).then(function () {
                self.reload();
            });
        },
        _addNewTour: function(event, data) {
            var self = this;
            var resID = false;
            if (data && data.resID) {
                resID = data.resID;
            };
            self._rpc({
                model: "knowsystem.tour",
                method: 'return_popup_form_view',
                args: [[]],
                context: {},
            }).then(function (view_id) {
                var onSaved = function(record) {
                    self._renderTours();
                };
                new dialogs.FormViewDialog(self, {
                    res_model: "knowsystem.tour",
                    title: _t("New Tour"),
                    view_id: view_id,
                    res_id: resID,
                    readonly: false,
                    shouldSaveLocally: false,
                    on_saved: onSaved,
                }).open();
            });
        },
        _onTourClick: function(event) {
            // The method to process playing the tour
            event.preventDefault();
            event.stopPropagation();
            var self = this;
            var resID = parseInt(event.currentTarget.id);
            self._rpc({
                model: "knowsystem.tour",
                method: 'return_start_page',
                args: [[resID]],
                context: {},
            }).then(function (action) {
                self.do_action(action);
            });
        },
        _onTourRightClick: function(event) {
            // The method to process editing the tour
            event.preventDefault();
            event.stopPropagation();
            if (this.is_action_enabled('delete')) {
                var resID = parseInt(event.currentTarget.id);
                this.$("#add_new_tour").trigger("click", {"resID": resID});
            };
        },

    });


    return KnowSystemKanbanController;

});
