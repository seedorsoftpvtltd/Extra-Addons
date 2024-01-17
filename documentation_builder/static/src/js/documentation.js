odoo.define('documentation_builder.documentation', function(require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');

    // Helper methods 
    function convertToSlug(articleHeader) {
        // The method to make title as url anchor
        // According to https://stackoverflow.com/questions/1053902/how-to-convert-a-title-to-a-url-slug-in-jquery
        return articleHeader
            .toLowerCase()
            .replace(/[^\w ]+/g,'')
            .replace(/ +/g,'-')
            ;        
    };
    // Documentation sections overview
    publicWidget.registry.docSectionPreview = publicWidget.Widget.extend({
        selector: '#doc_sections_content',
        events: {
            "click .doc_section_short": "_onOpenDocumentation",
        },
        _onOpenDocumentation: function (event) {
            event.preventDefault();
            event.stopPropagation();            
            window.open(event.currentTarget.id, "_self"); 
        },
    });
    // Documentation page
    publicWidget.registry.docNavigation = publicWidget.Widget.extend({
        selector: '#documentation_main_container',
        events: {
            "click .anchor_entry": "_onNavLinkClick",
            "click #hide_docu_navigation": "_onHideNavigationPanel",
            "click #scroll_top": "_onScrollTop",
            "click #docu_do_search": "_onSearch",
            "keyup #docu_search_key": "_onKeySearch",
            "click #clear_docu_search": "_onDocuClearSearch",
            "click #next_docu_search": "_onNextSearchResult",
            "click #previous_docu_search": "_onPreviousSearchResult",
        },
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                var navbarDiv = self.$("#nav_sticky"),
                    searchBarSection = self.$("#docu_searchbar_section");
                // Re-write to update article headers with anchors and to add header in toc
                var allArticles = self.$("#documentation_content .article_content_section"),
                    allHeadersParsed = $.Deferred(),
                    readyForScroll = $.Deferred();
                self.safeContent = self.$("#documentation_content")[0].innerHTML.replace(/&nbsp;/g,'<span> </span>');
                // anchor offset is the editor menu height + affixed menu height  
                self.activeSearchKey = -1;
                if (searchBarSection && searchBarSection.length) {
                    self.stickySearchBarHeight = searchBarSection.outerHeight();
                    self.stickySearchBar = searchBarSection;
                    self.stickySearchBarTop = searchBarSection.offset().top;
                    self.documentationContentHeight = self.$("#documentation_content")[0].offsetHeight;
                };
                self._defineAnchorOffset();
                var uniqueNum = 0;
                _.each(allArticles, function (article) {
                    uniqueNum ++;
                    var maxLevelElem = self.$("#nav_header_depth");
                    if (maxLevelElem && maxLevelElem.length > 0) {
                        self.maxLevel = maxLevelElem[0].innerHTML;
                    };
                    self._addArticleAnchors(article, uniqueNum).then(function (toc) {
                        if (navbarDiv && navbarDiv.length) {
                            var articleID = article.id.toString();
                            var articleEntry = self.$("#article_entry_"+articleID);
                            if (articleEntry && articleEntry.length) {
                                articleEntry.after(toc)
                            };
                        };
                    });
                    if (uniqueNum == allArticles.length) {
                        allHeadersParsed.resolve();
                    }
                });
                // Add collapse / expand icons for all nav headers
                if (navbarDiv && navbarDiv.length) {
                    allHeadersParsed.then(function () {
                        var allNavLinks = self.$(".anchor_entry");
                        var navBarIcons = '<div class="nav_collapse_icons pull-right"> \
                                                <i class="fa fa-chevron-up nav_anchor_icon nav_anchor_collapse"></i> \
                                                <i class="fa fa-chevron-down nav_anchor_icon nav_anchor_expand"></i> \
                                           </div>'
                        var kitera = 0;
                        _.each(allNavLinks, function (navLink) {
                            var aHref = navLink.getAttribute("href");
                            var childIds = self.$("[parent_id='" + aHref +"']");
                            if (childIds && childIds.length) {
                                var aElement = self.$("a[href='" + aHref +"']"); 
                                aElement.prepend(navBarIcons);
                            };
                            kitera ++;
                            if (kitera == allNavLinks.length) {
                                readyForScroll.resolve();
                            }
                        });              
                    });
                    // Re-write to add scrolling events for navbar
                    self.stickyNavigation = navbarDiv;
                    self.documentationContentHeight = self.$("#documentation_content")[0].offsetHeight;
                    self.stickyNavigationTop = navbarDiv.offset().top;
                    self.scrollTopIcon = self.$("#scroll_top");
                    self.windowHeight = $(window).height();
                    self.documentHeight = $(document).height();
                }
                else {
                    readyForScroll.resolve();
                };
                // manage scroll events
                window.addEventListener("scroll", function (event) {
                    self._onScrollPage(event);
                });
                window.addEventListener("resize", function (event) {
                    self.windowHeight = $(window).height();
                    self.documentHeight = $(document).height();
                    self.documentationContentHeight = self.$("#documentation_content")[0].offsetHeight;
                    if (self.stickySearchBar) {
                        self.stickySearchBarHeight = searchBarSection.outerHeight();
                    };
                    self._onScrollPage(event);
                });
                // simulate scrolling to stick toc & open target anchor
                readyForScroll.then(function () {                       
                    self.safeContent = self.$("#documentation_content")[0].innerHTML.replace(/&nbsp;/g,'<span> </span>');
                    var url = window.location.hash, idx = url.indexOf("#");
                    var urlAnchor = idx != -1 ? url.substring(idx+1) : "";
                    if (urlAnchor) {
                        self._onAnchorNavigate("#"+urlAnchor);
                    }
                    else{
                        $("html,body").animate({scrollTop: 1}, 400);                       
                    };
                });
            });
        }, 
        /*   
              EVENT HANDLERS
        */
        _onScrollPage: function(event) {
            // The method to catch scrolling event and adapt toc correspondingly
            var self = this;
            self._defineAnchorOffset();
            clearTimeout(this.scrollDebounceTimer);
            this.scrollDebounceTimer= setTimeout(function(){
                if (self.stickySearchBar) {
                    self._stickSearchBar();
                };
                if (self.stickyNavigation) {
                    self._stickToc();
                    self._activateCurrentHeader();
                };
            }, 10);            
        },
        _onNavLinkClick: function(event) {
            // Event processing to the method to animate to anchor
            var targetAnchorHref = event.currentTarget.getAttribute("href");
            this._onAnchorNavigate(targetAnchorHref);
        },
        _onHideNavigationPanel: function(event) {
            // The method to hide / show navigation panel
            var navigationPanel = this.$("#documentation_navigation");
            var docuContent = this.$("#documentation_content");
            var ulNavigation = this.$("#navigation_ul");
            var hideIcon = this.$("#hide_docu_navigation");
            if (ulNavigation.hasClass("knowsystem_hidden")) {
                navigationPanel.removeClass("navigation-collapsed");
                navigationPanel.addClass("col-lg-3");
                docuContent.removeClass("documentation-full-view");
                docuContent.addClass("col-lg-9");
                ulNavigation.removeClass("knowsystem_hidden");
                hideIcon.removeClass("fa-indent");
                hideIcon.addClass("fa-dedent");  
            }
            else {
                navigationPanel.removeClass("col-lg-3");
                navigationPanel.addClass("navigation-collapsed");     
                docuContent.removeClass("col-lg-9");
                docuContent.addClass("documentation-full-view");
                ulNavigation.addClass("knowsystem_hidden");        
                hideIcon.removeClass("fa-dedent");
                hideIcon.addClass("fa-indent");   
            };
        },
        _onKeySearch: function(event) {
           // to process the enter key up
            event.preventDefault();
            event.stopPropagation();
            if (event.keyCode === 13) {
                this.$("#docu_do_search").click();
            };
        },
        _onSearch: function(event) {
            // The method to search and highlight keys in the contents
            function adaptToSpecialSymbols(thisNodeText) {
                // the method to apply search key with parsed xml (look at the py method to_xml in misc)
                var map = {
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                };
                return thisNodeText.replace(/[&<>]/g, function(m) { return map[m]; });
            };
            async function setUniqueSearchId(allNodes) {
                // The method to set unique search id for elements. Not actually used, but usefull for testing
                var setIDiterator = 0;
                _.each(allNodes, function (node) {
                    setIDiterator++;
                    node.setAttribute("searchdocuid", setIDiterator)
                });
            };
            function searchMatchsNum(searchKey, searchText, caseSensitive) {
                // The method to search among substring
                // According to https://stackoverflow.com/questions/3410464/how-to-find-indices-of-all-occurrences-of-one-string-in-another-in-javascript
                var searchKeyLen = searchKey.length;
                if (searchKeyLen == 0) {
                    return 0;
                };
                if (!caseSensitive) {
                    searchKey = searchKey.toLowerCase();
                    searchText = searchText.toLowerCase();
                };
                var startIndex = 0, 
                    index,
                    resultNum = 0;
                while ((index = searchText.indexOf(searchKey, startIndex)) > -1) {
                    resultNum ++;
                    startIndex = index + searchKeyLen;
                };
                return resultNum;
            };
            function wrapTextNode(node) {
                var newElementNode = document.createElement('docusearch');
                newElementNode.innerText = $(node).text();
                node.parentNode.replaceChild(newElementNode, node);
                return newElementNode;
            };
            function replaceWithHighlight(node, regexPattern, caseSensitive, firstOccurence) {
                // The method to add highlight span for found matches
                var regexFlags = "",
                    notFirstClass = "";
                regexPattern = adaptToSpecialSymbols(regexPattern); // since innerHTML has those
                if (!firstOccurence) {
                    // global replacement of all occrurences
                    regexFlags = regexFlags + "g";
                }
                else if (firstOccurence == "last") {
                    // the last occurence
                    regexPattern = regexPattern + "$";
                }
                else if (firstOccurence == "first") {
                    // The first occurenct
                    notFirstClass = "docu_search_highlight_no_nav"
                };
                if (!caseSensitive) {
                    // case insensitive
                    regexFlags = regexFlags + "i";
                };
                regexPattern = new RegExp(regexPattern, regexFlags);
                node.innerHTML = node.innerHTML.replace(
                    regexPattern, 
                    function(match, contents, offset, input_string) {
                        return "<docusearch class='docu_search_highlight " + notFirstClass + "'>"+match+"</docusearch>";
                    }
                );
            };
            function findStartOverlap(searchKey, searchText) {
                // The method to find out whether checked text starts with search key end
                var searchKeyLen = searchKey.length;
                if (searchKeyLen <= 0) {
                    return ""
                };    
                if (searchText.startsWith(searchKey)) {
                    return searchKey;
                };
                searchKey = searchKey.slice(0, searchKeyLen-1);
                return findStartOverlap(searchKey, searchText)
            };
            function findEndOverlap(searchKey, searchText) {
                // The method to find out whether checked text end with with search key start
                var searchKeyLen = searchKey.length;
                if (searchKeyLen <= 0) {
                    return ""
                };       
                if (searchText.endsWith(searchKey)) {
                    return searchKey;
                };
                searchKey = searchKey.slice(0, searchKeyLen-1);
                return findEndOverlap(searchKey, searchText)
            };
            function searchKeyWordParts(nodes, searchKey, caseSensitive, tempNodes, tempSearch) {
                // the method to retrieve search parts if they are in different text nodes
                _.each(nodes, async function (node) {
                    var thisNodeText = $(node).text();
                    if (thisNodeText) {
                        if (!caseSensitive) {
                            searchKey = searchKey.toLowerCase();
                            thisNodeText = thisNodeText.toLowerCase();
                        };
                        if (node.nodeType == 3) {
                            if (tempNodes.length == 0) {
                                var endOverLap = findEndOverlap(searchKey, thisNodeText);    
                                if (endOverLap) {
                                    tempNodes.push(node);
                                    tempSearch.push(endOverLap);
                                };                       
                            }
                            else {
                                var tempSearchKey = tempSearch.join("");
                                var searchKeyPart = searchKey.slice(tempSearchKey.length, searchKey.length);
                                var startOverlap = findStartOverlap(searchKeyPart, thisNodeText);
                                if (startOverlap) {
                                    tempNodes.push(node);
                                    tempSearch.push(startOverlap);  
                                    tempSearchKey = tempSearch.join("");
                                    if (searchKey.includes(tempSearchKey)) {
                                        if (tempSearchKey == searchKey) {
                                            await highlighSearchParts(tempNodes, tempSearch);
                                            tempNodes.length = 0;
                                            tempSearch.length = 0;
                                        }
                                        else {
                                            // the case A_Bxxx_C > search by ABC. Such string length should be the same
                                            if (startOverlap.length != thisNodeText.length) {
                                                tempNodes.length = 0;
                                                tempSearch.length = 0;
                                            }
                                        };
                                    }
                                    else {
                                        tempNodes.length = 0;
                                        tempSearch.length = 0;
                                    };                             
                                }
                                else {
                                    tempNodes.length = 0;
                                    tempSearch.length = 0;
                                };
                            
                                if (tempNodes.length == 0) {
                                    // check the last item for being start 
                                    var endOverLap = findEndOverlap(searchKey, thisNodeText);    
                                    if (endOverLap) {
                                        tempNodes.push(node);
                                        tempSearch.push(endOverLap);
                                    };
                                };
                            };
                        }
                        else if (node.nodeType == 1) {
                            await searchKeyWordParts($(node).contents(), searchKey, caseSensitive, tempNodes, tempSearch);
                        };
                    };
                });
                function highlighSearchParts(fNodes, fSearch) {
                    // the method to highligh each found part
                    var itera = 0;
                    _.each(fNodes, function(node) {
                        var newElementNode = wrapTextNode(node);
                        var occurence = "first";
                        if (itera == 0) {
                            occurence = "last";
                        };
                        replaceWithHighlight(newElementNode, fSearch[itera], caseSensitive, occurence);
                        itera ++;
                    });                    
                };
            };
            async function findLastNodewithKey(nodes, searchKey, caseSensitive, lastMatch) {
                // The method to go over all elements recursively and replace with matches
                var totalNodesNum = 0;
                _.each(nodes, async function(node){
                    var thisNodeMatches;
                    if (node.nodeType == 1) {
                        // element node > need to check children
                        thisNodeMatches = searchMatchsNum(searchKey, $(node).text(), caseSensitive);
                        if (thisNodeMatches > 0) {
                            if ($(node).contents().length > 0) {
                                findLastNodewithKey($(node).contents(), searchKey, caseSensitive, thisNodeMatches).then(function (childNodeMatches) {
                                    if (childNodeMatches[1] > childNodeMatches[0]) {
                                        /* the root element contains more matches than all children elements
                                           example: <strong>1</strong>2 when search by '12' */
                                        // $(node).addClass("docu_search_highlight"); - if to simply highlight parent el
                                        searchKeyWordParts($(node).contents(), searchKey, caseSensitive, [], [])
                                    }
                                });
                            };
                        };
                    }
                    else if (node.nodeType == 3) {
                        // text node: if there are matches > firstly replace it with element nodes
                        thisNodeMatches = searchMatchsNum(searchKey, $(node).text(), caseSensitive);
                        if (thisNodeMatches > 0) {
                            var newElementNode = wrapTextNode(node);
                            replaceWithHighlight(newElementNode, searchKey, caseSensitive);
                        };
                    }
                    else {
                        // other node types are not checked at all
                        thisNodeMatches = 0;
                    };
                    totalNodesNum = totalNodesNum + thisNodeMatches;
                });
                return [totalNodesNum, lastMatch]
            };

            var self = this,
                firstLevelNodes,
                searchKey = self.$("#docu_search_key")[0].value,
                searchType = self.$(".docu_search_selection.active")[0].id,          
                docuContentsObject = self.$("#documentation_content"),
                caseSensitive = false;
            self.searchResults = [];
            self.searchIDs = [];
            self.activeSearchKey = -1;
            self.$("#docu_search_results").addClass("knowsystem_hidden");
            if (searchKey) {
                // restore previous search highlight
                docuContentsObject[0].innerHTML = self.safeContent; 
                if (searchType == "docu_search_headers") {
                    // the case <h2><h3></h3></h2> is impossible
                    firstLevelNodes = docuContentsObject.find("h1,h2,h3,h4,h5,h6");
                }
                else { 
                    firstLevelNodes = docuContentsObject.contents();
                    if (searchType == "docu_search_case_sensitive") {
                        caseSensitive = true;
                    }
                }
                findLastNodewithKey(firstLevelNodes, searchKey, caseSensitive, 0).then(function (matchResults) {
                    self.$("#docu_search_results").removeClass("knowsystem_hidden");
                    var searchMatches = matchResults[0];
                    self.$("#search_matches_num")[0].innerHTML = searchMatches;
                    var allSearchPositions = self.$(".docu_search_highlight:not(.docu_search_highlight_no_nav)"),
                        uniqueHiglightId = 0,
                        SUID;
                    _.each(allSearchPositions, function(node) {
                        uniqueHiglightId ++;
                        SUID = "seachkey_" +uniqueHiglightId.toString();
                        node.setAttribute("id", SUID);
                        self.searchResults.push($(node).offset().top);
                        self.searchIDs.push(SUID);
                        if (uniqueHiglightId == allSearchPositions.length) {
                            self.$("#next_docu_search").click();
                        };
                    });
                    if (searchMatches == 0) {
                        self.$(".search_docu_navigation").addClass("knowsystem_hidden");
                    }
                    else {
                        self.$(".search_docu_navigation").removeClass("knowsystem_hidden");
                    };
                });
            };
        },
        _onDocuClearSearch: function(event) {
            // The method to clear search
            this.$("#documentation_content")[0].innerHTML = this.safeContent; 
            this.$("#docu_search_key")[0].value = "";
            this.$("#docu_search_results").addClass("knowsystem_hidden");
        },
        _onNextSearchResult: function(event) {
            // the method to get to the closest next search result
            var self = this;
            self.$(".docu_search_highlight").removeClass("docu_search_highlight_active");
            if (self.searchResults && self.searchResults.length) {           
                if (self.activeSearchKey != -1) {
                    self.activeSearchKey = self.activeSearchKey + 1;
                    if (self.activeSearchKey > self.searchResults.length-1) {
                        self.activeSearchKey = 0;
                    };
                }
                else {
                    self.activeSearchKey = 0;                    
                };
                $("html,body").animate({scrollTop: self.searchResults[self.activeSearchKey]-300}, 400);
                self.$("#"+self.searchIDs[self.activeSearchKey]).addClass("docu_search_highlight_active");
            };
        },
        _onPreviousSearchResult: function(event) {
            // the method to get closest previous results
            var self = this;
            self.$(".docu_search_highlight").removeClass("docu_search_highlight_active");
            if (self.searchResults && self.searchResults.length) {           
                if (self.activeSearchKey != -1) {
                    self.activeSearchKey = self.activeSearchKey - 1;
                    if (self.activeSearchKey < 0) {
                        self.activeSearchKey = self.searchResults.length-1;
                    };
                }
                else {
                    self.activeSearchKey = self.searchResults.length-1;                    
                };
                $("html,body").animate({scrollTop: self.searchResults[self.activeSearchKey]-300}, 400);
                self.$("#"+self.searchIDs[self.activeSearchKey]).addClass("docu_search_highlight_active");
            };
        },
        _onScrollTop: function(event) {
            // The method to get back to the start of documentation
            $("html,body").animate({scrollTop: this.stickyNavigationTop-this.anchorOffset}, 400);
        },
        /*   
              HELPERS   
        */
        _defineAnchorOffset: function() {
            // The method to define actual anchor offset
            var self = this;
            self.anchorOffset = $("#wrapwrap").offset().top;       
            if ($("header.o_header_affix").hasClass("affixed")) {
                self.anchorOffset = self.anchorOffset + $("header.o_header_affix").outerHeight();
            };
            if (self.stickySearchBar) {
                self.anchorOffset = self.anchorOffset + self.stickySearchBarHeight;
            };
        },
        _onAnchorNavigate: function(targetAnchorHref) {
            // The method to animate to anchor
            var self = this;
            if (targetAnchorHref == "#scrollTop=0") {
                $("html,body").animate({scrollTop: 0}, 400);
            }
            else {
                try {
                    var initialOffset = this.anchorOffset;
                    var targetAnchor = $(targetAnchorHref);
                    var topOffset = targetAnchor.offset().top - this.anchorOffset;
                    if (Math.abs($(window).scrollTop() - topOffset) < 5) {
                        // to similate scrolling in case of refresh
                        topOffset = topOffset + 2;
                    };                   
                    $("html,body").animate({scrollTop: topOffset}, 400, function () {
                        if (initialOffset != self.anchorOffset) {
                            $("html,body").animate({scrollTop: topOffset+initialOffset-self.anchorOffset}, 10);
                        };
                    });
                }
                catch (e) {
                    console.warn("Anchor is not found");
                };             
            };
        },
        _onActivateEntry: function(anchors) {
            // The method to activate / hide / show navbar links
            var allLIs = this.$(".docu_nav_li");
            allLIs.removeClass("shown_nav_entry");
            allLIs.removeClass("active_entry");   
            var self = this;
            _.each(anchors, function (anchor) {         
                self._onActivateSingleEntry(anchor);        
            });
        },
        _onActivateSingleEntry: function(anchor) {
            // The method implemeted for recursion
            var aElement = self.$("a[href='" + anchor +"']").parent();
            if (aElement && aElement.length) {
                aElement.addClass("active_entry");
                // Expand and activate parent recursively
                var parentAnchorKey = aElement[0].getAttribute("parent_id");
                this._onActivateSingleEntry(parentAnchorKey);
                // Expand children
                var childeLIs = self.$("[parent_id='" + anchor +"']");
                childeLIs.addClass("shown_nav_entry");
            };
        },
        _activateCurrentHeader: function() {
            // The method to retrieve currently read header section
            var closestHeaders = [],
                allHeaders = this.$("[actheader='1']"),
                top, bottom;
            var scrollTop = $(window).scrollTop();
            var scrollBottom = this.documentHeight - this.windowHeight - scrollTop;
            if (scrollBottom == 0) {
                for (var i=0; i<allHeaders.length; i++) {
                    top = allHeaders[i].getBoundingClientRect().top - this.anchorOffset;
                    bottom = allHeaders[i].getBoundingClientRect().bottom + this.anchorOffset;
                    if (top >= 0 && bottom <= this.windowHeight) {
                        closestHeaders.push("#" + allHeaders[i].getAttribute("id"));
                    }
                };                
            }
            if (closestHeaders.length == 0) {
                var max = - Number.MAX_VALUE;
                for (var i=0; i<allHeaders.length; i++) {
                    top = allHeaders[i].getBoundingClientRect().top - this.anchorOffset - 50;
                    if (top <= 0 && top > max) {
                        max = top;
                        closestHeaders = ["#" + allHeaders[i].getAttribute("id")];
                    };
                };
            }
            this._onActivateEntry(closestHeaders);
        },
        _stickSearchBar: function() {
            // The method to stick the searchbar to the top
            var self = this;
            var scrollTop = $(window).scrollTop();
            var scrollDifference = scrollTop - self.stickySearchBarTop + self.anchorOffset - self.stickySearchBarHeight;
            if (scrollDifference > 0 && scrollDifference < self.documentationContentHeight-100) {
                if (! self.stickySearchBar.hasClass("stickynavtop") || !self.stickySearchBar.top != self.anchorOffset-self.stickySearchBarHeight) {
                    self.stickySearchBar.addClass("stickynavtop");
                    self.stickySearchBar.animate({"top": self.anchorOffset-self.stickySearchBarHeight}, 10);
                    // Not to change the elements top
                    self.$el.animate({"margin-top": self.stickySearchBarHeight}, 10);
                };
            }
            else {
                if (self.stickySearchBar.hasClass("stickynavtop")) {
                    self.stickySearchBar.removeClass("stickynavtop");
                    self.stickySearchBar.animate({"top": "inherit"}, 10);
                    self.$el.animate({"margin-top": 0}, 10);
                };
            };
        },
        _stickToc: function() {
            // The method to scroll navigation if the page is scrolled
            var scrollTop = $(window).scrollTop();
            if (scrollTop > this.stickyNavigationTop + 50) {
                this.scrollTopIcon.removeClass("knowsystem_hidden");
            }
            else {
                this.scrollTopIcon.addClass("knowsystem_hidden");
            }
            var scrollDifference = scrollTop - this.stickyNavigationTop + this.anchorOffset;
            var maxHeight = this.windowHeight - this.anchorOffset; 
            if (scrollDifference + maxHeight > this.documentationContentHeight) {
                // not to significantly overscroll the bottom
                var documentOffset = scrollDifference  + maxHeight - this.documentationContentHeight;
                maxHeight = maxHeight - documentOffset;
                if (maxHeight < 200) {
                    scrollDifference = scrollDifference - (200-maxHeight);                     
                };
            };
            if (scrollDifference < 0) {
                maxHeight = maxHeight + scrollDifference;
                scrollDifference = 0;
            };
            if (maxHeight < 200) {
                maxHeight = 200;
            };
            var scrollTop = scrollDifference.toString() + "px";
            var maxHeight = maxHeight.toString() + "px";
            this.stickyNavigation.animate({"margin-top": scrollTop, "max-height": maxHeight}, 10)
        },
        _addArticleAnchors: function (article, uniqueNum) {
            /** The method to go through article content and add anchors to headers
              * The method returns the object with all headers relate to this article
              * In case order of headers in toc is not correct: 
              * >> https://stackoverflow.com/questions/497418/produce-heading-hierarchy-as-ordered-list
            */
            var finalDef = $.Deferred();                
            var toc = "";
            if (this.maxLevel) {   
                // Find all headers by query > adapt each + construct the toc
                var allHeaders = article.querySelectorAll("#documentation_content "+this.maxLevel);
                if (allHeaders && allHeaders.length != 0) {
                    var activeLevel = 0;
                    var itera = 0;
                    var lastLevel = 0;
                    var articleID = article.id.toString();
                    var ParentHeaders = {};
                    var parentPadding = 0;
                    var parentHeader = article.getAttribute("hrefid");
                    ParentHeaders["0"] = {"parentHeader": parentHeader, "padding": parentPadding};
                    var paddingStep = 8;
                    _.each(allHeaders, function (articleHeader) {
                        itera ++;
                        var activeLevel = parseInt(articleHeader.tagName.substring(1));
                        var activeText = articleHeader.innerText;
                        if (activeText.length > 152) {
                            activeText = activeText.substring(0,150) + "...";
                        };
                        var titleSubString = convertToSlug(activeText).substring(0,30);
                        if (! titleSubString || titleSubString.replace("-", "") == "") {
                            // for the case it is not in Latin characters
                            titleSubString = "navheader";
                        };
                        var articleHeaderLink = titleSubString + "-" + articleID + "-" 
                                               + itera.toString() + "-" + uniqueNum; 
                        articleHeader.setAttribute("id", articleHeaderLink);
                        articleHeader.setAttribute("actheader", "1");
                        if (activeLevel > lastLevel) {
                            // the next level: h1 > h2, but also h1 > h5
                            toc += (new Array(activeLevel-lastLevel+1)).join("<ul>");
                            var parentHeaderSet = ParentHeaders[lastLevel.toString()];
                            parentHeader = parentHeaderSet.parentHeader;
                            parentPadding = parentHeaderSet.padding + paddingStep;
                            ParentHeaders[activeLevel.toString()] = {
                                "parentHeader": articleHeaderLink,
                                "padding": parentPadding,
                            };
                        }
                        else if (activeLevel < lastLevel) {
                            // the previous level: h2 > h1, but also h5 > h1
                            toc += (new Array(lastLevel-activeLevel+1)).join("</ul>");                           
                            var minLevel = lastLevel;
                            var levelFine = false;
                            while (!levelFine && minLevel >= 0) {
                                if (ParentHeaders[minLevel.toString()]) {
                                    if (minLevel >= activeLevel) {
                                        delete ParentHeaders[minLevel.toString()];
                                    }
                                    else {
                                        var parentHeaderSet = ParentHeaders[minLevel.toString()];
                                        parentHeader = parentHeaderSet.parentHeader;
                                        parentPadding = parentHeaderSet.padding + paddingStep;
                                        levelFine = true;
                                    }
                                }
                                minLevel --;
                            };
                            ParentHeaders[activeLevel.toString()] = {
                                "parentHeader": articleHeaderLink,
                                "padding": parentPadding
                            };
                        };
                        toc += "<li class='docu_nav_li' parent_id='#"+ parentHeader + "' style='margin-left: "
                                + parentPadding + "px !important;'><a href='#" + articleHeaderLink 
                                + "' class='anchor_entry'>" + activeText + "</a></li>";
                        lastLevel = activeLevel;
                        if (itera == allHeaders.length) {
                            toc += (new Array(activeLevel + 1)).join("</ul>");
                            finalDef.resolve(toc);
                        };
                    });  
                }
                else {
                    finalDef.resolve(toc);
                }             
            }
            else {
                finalDef.resolve(toc);
            };
            return finalDef
        },
    });

});
