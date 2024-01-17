odoo.define('knowsysten.sections', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    function reloadArticlesSearch(jstree_el) {
        var self = jstree_el;
        var refS = self.jstree(true),
            checkedSections = refS.get_checked();
        if (checkedSections.length != 0) {
            var strSections = checkedSections.join(",");
        }
        else {
            var strSections = "";
        }
        var currentSections = getParameterByName('sections');
        if (currentSections != strSections) {
            if (!strSections) {
                strSections = "";
            }
            var newUrl = setParameterByName("sections", strSections);
            window.location = newUrl;
        };
    };
    function reloadArticlesTags(jstree_el) {
        var self = jstree_el;
        var refT = self.jstree(true),
            checkedTags = refT.get_checked();
        if (checkedTags.length != 0) {
            var strTags = checkedTags.join(",");
        }
        else {
            var strTags = "";
        }
        var currentTags = getParameterByName('tags');
        if (currentTags != strTags) {
            if (!strTags) {
                strTags = "";
            }
            var newUrl = setParameterByName("tags", strTags);
            window.location = newUrl;
        };
    };
    function reloadArticlesTypes(jstree_el) {
        var self = jstree_el;
        var refT = self.jstree(true),
            checkedTypes = refT.get_checked();
        if (checkedTypes.length != 0) {
            var strTypes = checkedTypes.join(",");
        }
        else {
            var strTypes = "";
        }
        var currentTypes = getParameterByName('types');
        if (currentTypes != strTypes) {
            if (!strTypes) {
                strTypes = "";
            }
            var newUrl = setParameterByName("types", strTypes);
            window.location = newUrl;
        };
    };
    function getParameterByName(paramName) {
        var url = window.location.href;
        paramName = paramName.replace(/[\[\]]/g, '\\$&');
        var regex = new RegExp('[?&]' + paramName + '(=([^&#]*)|&|#|$)'),
            results = regex.exec(url);
        if (!results) return '';
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
    };
    function setParameterByName(paramName, paramValue) {
        var url = window.location.href;
        var pattern = new RegExp('\\b('+paramName+'=).*?(&|#|$)');
        if (url.search(pattern)>=0) {
            return url.replace(pattern,'$1' + paramValue + '$2');
        };
        url = url.replace(/[?#]$/, '');
        return url + (url.indexOf('?')>0 ? '&' : '?') + paramName + '=' + paramValue;
    };

    function addJSTreeToolTip() {
        $("a.jstree-anchor").on("mouseover", function(event) {
            var knowToolTip = event.currentTarget.getAttribute("kn_tip");
            if (knowToolTip) {
                var anchorID = event.currentTarget.getAttribute("id") + "_tooltip";
                var toolTipdDiv = document.createElement("div");
                toolTipdDiv.setAttribute("id", anchorID);
                event.currentTarget.setAttribute("remove_tool_tip", anchorID);
                toolTipdDiv.innerHTML = knowToolTip;
                toolTipdDiv.setAttribute("class", "knowToolTip");
                event.currentTarget.after(toolTipdDiv);
            }
        });
        $("a.jstree-anchor").on("mouseout", function(event) {
            var relateToolTip = event.currentTarget.getAttribute("remove_tool_tip");
            if (relateToolTip) {
                $("div#"+relateToolTip).remove();
            };
        });
    };

    publicWidget.registry.sectionsHierarchy = publicWidget.Widget.extend({
        selector: '#knowsystem_sections',
        jsLibs: [
            '/knowsystem/static/lib/jstree/jstree.js',
        ],
        cssLibs: [
            '/knowsystem/static/lib/jstree/themes/default/style.css',
        ],
        start: function () {
            $('#knowsystem_sections').each(function (index) {
                var self = $(this);
                var parsedSections = eval(self[0].dataset.id);
                self.jstree('destroy');
                var jsTreeOptions = {
                    'core' : {
                        'themes': {'icons': false},
                        'check_callback' : true,
                        'data': parsedSections,
                        "multiple" : true,
                    },
                    "plugins" : [
                        "checkbox",
                        "state",
                    ],
                    "state" : { "key" : "knowsystem_sections" },
                    "checkbox" : {
                        "three_state" : false,
                        "cascade": "down",
                        "tie_selection" : false,
                    },
                };
                var ref = self.jstree(jsTreeOptions);
                var currentSections = getParameterByName('sections');
                var checkedSectionsIDS = currentSections.split(",");
                self.on("state_ready.jstree", self, function (event, data) {
                   var jsTreeRef = self.jstree(true);
                   jsTreeRef.check_node(checkedSectionsIDS);
                   var allSelected = jsTreeRef.get_checked();
                   var diff = allSelected.filter(x => checkedSectionsIDS.indexOf(x) < 0);
                   jsTreeRef.uncheck_node(diff);
                   self.on("check_node.jstree uncheck_node.jstree", self, function (event, data) {
                        reloadArticlesSearch(self);
                   });
                   addJSTreeToolTip();
                });
            });
        },
    });
    publicWidget.registry.tagsHierarchy = publicWidget.Widget.extend({
        selector: '#knowsystem_tags',
        jsLibs: [
            '/knowsystem/static/lib/jstree/jstree.js',
        ],
        cssLibs: [
            '/knowsystem/static/lib/jstree/themes/default/style.css',
        ],
        start: function () {
            $('#knowsystem_tags').each(function (index) {
                var self = $(this);
                var parsedTags = eval(self[0].dataset.id);
                self.jstree('destroy');
                var jsTreeOptions = {
                    'core' : {
                        'themes': {'icons': false},
                        'check_callback' : true,
                        'data': parsedTags,
                        "multiple" : true,
                    },
                    "plugins" : [
                        "checkbox",
                        "state",
                    ],
                    "state" : { "key" : "knowsystem_tags" },
                    "checkbox" : {
                        "three_state" : false,
                        "cascade": "down",
                        "tie_selection" : false,
                    },
                };
                var refT = self.jstree(jsTreeOptions);
                var currentTags = getParameterByName('tags');
                var checkedTagsIDS = currentTags.split(",");
                self.on("state_ready.jstree", self, function (event, data) {
                   var jsTreeRefT = self.jstree(true);
                   jsTreeRefT.check_node(checkedTagsIDS);
                   var allTSelected = jsTreeRefT.get_checked();
                   var diff = allTSelected.filter(x => checkedTagsIDS.indexOf(x) < 0);
                   jsTreeRefT.uncheck_node(diff);
                   self.on("check_node.jstree uncheck_node.jstree", self, function (event, data) {
                        reloadArticlesTags(self);
                   });
                   addJSTreeToolTip();
                });
            });
        },
    });
    publicWidget.registry.typesHierarchy = publicWidget.Widget.extend({
        selector: '#knowsystem_types',
        jsLibs: [
            '/knowsystem/static/lib/jstree/jstree.js',
        ],
        cssLibs: [
            '/knowsystem/static/lib/jstree/themes/default/style.css',
        ],
        start: function () {
            $('#knowsystem_types').each(function (index) {
                var self = $(this);
                var parsedTypes = eval(self[0].dataset.id);
                self.jstree('destroy');
                var jsTreeOptions = {
                    'core' : {
                        'themes': {'icons': false},
                        'check_callback' : true,
                        'data': parsedTypes,
                        "multiple" : true,
                    },
                    "plugins" : [
                        "checkbox",
                        "state",
                    ],
                    "state" : { "key" : "knowsystem_types" },
                    "checkbox" : {
                        "three_state" : false,
                        "cascade": "down",
                        "tie_selection" : false,
                    },
                };
                var refT = self.jstree(jsTreeOptions);
                var currentTypes = getParameterByName('types');
                var checkedTypesIDS = currentTypes.split(",");
                self.on("state_ready.jstree", self, function (event, data) {
                   var jsTreeRefT = self.jstree(true);
                   jsTreeRefT.check_node(checkedTypesIDS);
                   var allTSelected = jsTreeRefT.get_checked();
                   var diff = allTSelected.filter(x => checkedTypesIDS.indexOf(x) < 0);
                   jsTreeRefT.uncheck_node(diff);
                   self.on("check_node.jstree uncheck_node.jstree", self, function (event, data) {
                        reloadArticlesTypes(self);
                   });
                });
            });
        },
    });


});
