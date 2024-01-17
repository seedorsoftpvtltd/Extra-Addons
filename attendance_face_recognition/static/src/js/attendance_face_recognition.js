odoo.define('attendance_face_recognition.attendance_face_recognition', function (require) {
    "use strict";

    var core = require('web.core');

    var MyAttendances = require('hr_attendance.my_attendances');
    var KioskMode = require('hr_attendance.kiosk_mode');
    
    var Widget = require("web.Widget");
    var session = require("web.session");   
    
    var _t = core._t;
    var QWeb = core.qweb;

    MyAttendances.include({
        init: function (parent, action) {
            this._super.apply(this, arguments);                        
            this.load_models = this.load_models();
            this.labeledFaceDescriptors = [];
            this.load_label = $.Deferred();
            this.latitude = false;
            this.longitude = false;
        },  

        load_models: function(){
            var self = this;
            return Promise.all([
                faceapi.nets.tinyFaceDetector.load('/attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceLandmark68Net.load('/attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceLandmark68TinyNet.load('/attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceRecognitionNet.load('/attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceExpressionNet.load('/attendance_face_recognition/static/src/lib/weights'),
            ]).then(function(){
                self.prepareFaceDetector();
            });
        },

        start: function(){
            var self = this;
            return $.when(self.load_models, this._super.apply(this, arguments)).then(function(){
                self.loadLabeledImages();
                self.getCurrentPosition();
                self.$el.find('.face_recognition_status').removeClass('d-none').addClass('face_recognition_main_on');
            });
        },
        getCurrentPosition: function(){
            var self = this;
            if(session.log_attendance_geolocation){
                var geolocation= navigator.geolocation;
                if (window.location.protocol == 'https:'){                    
                    if (geolocation) {
                        geolocation.getCurrentPosition(self.getPositionCoords.bind(self), self._getCurrentPositionErr, {
                            enableHighAccuracy: true,
                            timeout: 5000,
                            maximumAge: 0
                        });
                    }
                }else{
                    self.do_notify(_t('Warning'), _t("GEOLOCATION API MAY ONLY WORKS WITH HTTPS CONNECTIONS."));
                }
            }           
        },
        getPositionCoords: function(position){
            var self = this;
            self.latitude = position.coords.latitude;
            self.longitude = position.coords.longitude;
        },
        _getCurrentPositionErr: function(err){
            switch(err.code) {
                case err.PERMISSION_DENIED:
                  console.log("The request for geolocation was refused by the user.");
                  break;
                case err.POSITION_UNAVAILABLE:
                    console.log("There is no information about the location available.");
                  break;
                case err.TIMEOUT:
                    console.log("The request for the user's location was unsuccessful.");
                  break;
                case err.UNKNOWN_ERROR:
                    console.log("An unidentified error has occurred.");
                  break;
              }
        },
        loadLabeledImages:  function(){
            var self = this;
            return this._rpc({
                route: '/attendance_face_recognition/loadLabeledImages/'
            }).then(async function (data) {
                self.labeledFaceDescriptors = await Promise.all(
                    data.map((data, i) => {  
                    const descriptors = [];
                    for (var i = 0; i < data.descriptors.length; i++) {
                        if (data.descriptors[i]){
                            descriptors.push(new Float32Array(new Uint8Array([...window.atob(data.descriptors[i])].map(d => d.charCodeAt(0))).buffer));
                        }
                    }
                    return new faceapi.LabeledFaceDescriptors(data.label.toString(), descriptors);
                }));
                self.load_label.resolve();
            })
        },

        prepareFaceDetector: async function() {
            var self = this;
            return new Promise(function(){
                let base_image = new Image();
                base_image.src = "/attendance_face_recognition/static/src/img/startFaceDetect.jpg";                
                base_image.onload = async function() {
                    var has_Detection_model = self.isFaceDetectionModelLoaded();
                    var has_Recognition_model = self.isFaceRecognitionModelLoaded();
                    var has_Landmark_model = self.isFaceLandmarkModelLoaded();
                
                    if (has_Detection_model && has_Recognition_model && has_Landmark_model){
                        await faceapi.detectSingleFace(base_image, new faceapi.TinyFaceDetectorOptions())
                            .withFaceLandmarks()
                            .withFaceDescriptor()
                            .run().then(res => {});;                        
                    }else{
                        return setTimeout(() => prepareFaceDetector())
                    } 
                }
            });
        },

        update_attendance: function () {
            var self = this;
            if(session.attendance_face_recognition){
                if (self.labeledFaceDescriptors && self.labeledFaceDescriptors.length != 0){
                    var matchedEmployee = new FaceRecognitionDialog(this, self.labeledFaceDescriptors)._onOpen();
                }else{
                    self.do_warn(_t('Warning'), _t("Detection Failed: Resource not found / not loaded, Please add it to your employee profile."));
                }
            }else if(session.log_attendance_geolocation){
                self.update_location_attendance();
            }
            else{
                self._super();
            }
        },
        update_location_attendance: function(){
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances', null, false, [self.latitude, self.longitude]],
            })
            .then(function(result) {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.do_warn(result.warning);
                }
            });
        },
        _update_face_attendance: _.debounce(function (employee_id, img) {
            var self = this;
            if (employee_id == session.attendance_emplyee){
                this._rpc({
                    model: 'hr.employee',
                    method: 'attendance_manual',
                    args: [[parseInt(employee_id)], 'hr_attendance.hr_attendance_action_my_attendances', null , img, [self.latitude, self.longitude]],
                })
                .then(function (result) {
                    if (result.action) {
                        self.do_action(result.action);
                        
                    } else if (result.warning) {
                        self.do_warn(result.warning);
                    }
                });
            }else{
                self.do_warn(_t('Warning'), _t("Detection Failed: The face you're trying for isn't one of the logged-in user."));
            }
        }, 200, true),

        getCurrentFaceDetectionNet: function() {
            return faceapi.nets.tinyFaceDetector;
        },

        isFaceDetectionModelLoaded: function() {
            return !!this.getCurrentFaceDetectionNet().params
        },

        getCurrentFaceRecognitionNet:function () {
            return faceapi.nets.faceRecognitionNet;
        },

        isFaceRecognitionModelLoaded: function() {
            return !!this.getCurrentFaceRecognitionNet().params
        },

        getCurrentFaceLandmarkNet: function() {
            return faceapi.nets.faceLandmark68Net;
        },

        isFaceLandmarkModelLoaded: function() {
            return !!this.getCurrentFaceLandmarkNet().params
        },
    });

    KioskMode.include({
        events: _.extend(KioskMode.prototype.events, {
            "click .o_hr_kiosk_face_recognition":  _.debounce(function() {
                this.update_kiosk_attendance();
            }, 200, true),
        }),
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.is_face_recognition_enabled = session.kiosk_face_recognition;

            this.load_models = this.load_models();
            this.labeledFaceDescriptors = [];
            this.load_label = $.Deferred();
        },
        load_models: function(){
            var self = this;
            return Promise.all([
                faceapi.nets.tinyFaceDetector.load('/attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceLandmark68Net.load('/attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceLandmark68TinyNet.load('/attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceRecognitionNet.load('/attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceExpressionNet.load('/attendance_face_recognition/static/src/lib/weights'),
            ]).then(function(){
                self.prepareFaceDetector();
            });
        },
        start: function () {            
            var self= this;
            return $.when(self.load_models, this._super.apply(this, arguments)).then(function(){
                self.loadLabeledImages();
                self.$el.find('.face_recognition_status').removeClass('d-none').addClass('face_recognition_main_on');
            });
        },
        loadLabeledImages:  function(){
            var self = this;
            return this._rpc({
                route: '/attendance_face_recognition/loadLabeledImages/'
            }).then(async function (data) {
                self.labeledFaceDescriptors = await Promise.all(
                    data.map((data, i) => {  
                    const descriptors = [];
                    for (var i = 0; i < data.descriptors.length; i++) {
                        if (data.descriptors[i]){
                            descriptors.push(new Float32Array(new Uint8Array([...window.atob(data.descriptors[i])].map(d => d.charCodeAt(0))).buffer));
                        }
                    }
                    return new faceapi.LabeledFaceDescriptors(data.label.toString(), descriptors);
                }));
                self.load_label.resolve();
            })
        },

        prepareFaceDetector: async function() {
            var self = this;
            return new Promise(function(){
                let base_image = new Image();
                base_image.src = "/attendance_face_recognition/static/src/img/startFaceDetect.jpg";                
                base_image.onload = async function() {
                    var has_Detection_model = self.isFaceDetectionModelLoaded();
                    var has_Recognition_model = self.isFaceRecognitionModelLoaded();
                    var has_Landmark_model = self.isFaceLandmarkModelLoaded();
                
                    if (has_Detection_model && has_Recognition_model && has_Landmark_model){
                        await faceapi.detectSingleFace(base_image, new faceapi.TinyFaceDetectorOptions())
                            .withFaceLandmarks()
                            .withFaceDescriptor()
                            .run().then(res => {});;                        
                    }else{
                        return setTimeout(() => prepareFaceDetector())
                    } 
                }
            });
        },

        update_kiosk_attendance: function () {
            var self = this;
            if(session.kiosk_face_recognition){
                if (self.labeledFaceDescriptors && self.labeledFaceDescriptors.length != 0){
                    var matchedEmployee = new FaceRecognitionDialog(this, self.labeledFaceDescriptors)._onOpen();
                }else{
                    self.do_warn(_t('Warning'), _t("Detection Failed: Resource not found, Please add it to your employee profile."));
                }
            }       
        },

        _update_face_attendance: _.debounce(function (employee_id, img) {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_kiosk_recognition',
                args: [[parseInt(employee_id)], img],
            })
            .then(function (result) {
                if (result.action) {
                    self.do_action(result.action);
                    
                } else if (result.warning) {
                    self.do_warn(result.warning);
                }
            });
        }, 200, true),

        getCurrentFaceDetectionNet: function() {
            return faceapi.nets.tinyFaceDetector;
        },

        isFaceDetectionModelLoaded: function() {
            return !!this.getCurrentFaceDetectionNet().params
        },

        getCurrentFaceRecognitionNet:function () {
            return faceapi.nets.faceRecognitionNet;
        },

        isFaceRecognitionModelLoaded: function() {
            return !!this.getCurrentFaceRecognitionNet().params
        },

        getCurrentFaceLandmarkNet: function() {
            return faceapi.nets.faceLandmark68Net;
        },

        isFaceLandmarkModelLoaded: function() {
            return !!this.getCurrentFaceLandmarkNet().params
        },
    });


    var FaceRecognitionDialog = Widget.extend({  
        template: "FaceRecognitionDialog",
        events: {
            'click .close':  '_onDestroy',
        },
        init: function(parent, descriptors) {
            this._super.apply(this, arguments);
            this.title = _t("Face Recognition");
            this.match_label = '';
            this.match_employee_id = false;
            this.is_update_attendance = false;
            this.parent = parent;  
            this.descriptors =  descriptors; 
        },
        start: async function () {
            var self = this;             
            return this._super.apply(this, arguments);
        },

        renderElement: async function() {
            var self = this;
            this._super();
            var def = new $.Deferred();

            var video = self.$el.find("#video").get(0);

            navigator.getUserMedia = navigator.getUserMedia 
                || navigator.webkitGetUserMedia 
                || navigator.mozGetUserMedia;
            
            if (navigator.getUserMedia) {                
                var openRecognition = navigator.getUserMedia(
                    { video: {} },
                    function(stream) {                                             
                        video.srcObject = stream; 
                        video.play().then(function(){
                            self.FaceDetector();
                        }); 
                        video.muted = true;                            
                    },
                    function(err) {
                        console.log("onloadedmetadata");
                    }
                );
                def.resolve(openRecognition);
            }else {
                console.log("getUserMedia not supported");
            }
            return $.when(def);
        },
        _onOpen: function(){
            this.open();
        },
        open: async function() {
            var self = this;
            self.renderElement().then(function(){
                self.$el.modal("show");
            })            
            return self;
        },
        _onDestroy: function () {      
            this.destroy();
        },
        destroy: function () {
            if (this.isDestroyed()) {
                return;
            }
            if (this.intervalID){
                clearInterval(this.intervalID);
            }            
            this.$el.modal('hide');
            this.$el.remove();
            this._super.apply(this, arguments);            
        },

        FaceDetector: async function() {
            var self = this;

            var video = self.$el.find("#video").get(0);
            if(video.paused || video.ended || !this.isFaceDetectionModelLoaded() || faceapi.LabeledFaceDescriptors.length === 0){
                return setTimeout(() => this.FaceDetector())
            }
            
            var options = this.getFaceDetectorOptions();
            var useTinyModel = true;
            var match_count = 0;
            
            if (!self.intervalId) {
                self.intervalID = setInterval(async () => {
                    var displaySize = { width: video.offsetWidth, height: video.offsetHeight };
               
                    const detections = await faceapi.detectSingleFace(video, options)
                    .withFaceLandmarks()
                    .withFaceDescriptor();

                    if (detections){                        
                        var canvas = self.$el.find("#canvas").get(0);
                        faceapi.matchDimensions(canvas, displaySize);

                        const resizedDetections = faceapi.resizeResults(detections, displaySize)
                        faceapi.draw.drawDetections(canvas, resizedDetections)
                        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
                                               
                        if (resizedDetections && Object.keys(resizedDetections).length > 0) {
                            var faceMatcher = new faceapi.FaceMatcher(self.descriptors, 0.5);
                            const result = faceMatcher.findBestMatch(resizedDetections.descriptor);  

                            if (result && result._label != 'unknown'){
                                match_count += 1;
                                self.match_employee_id = result._label;
                                var label = self.getName(self.match_employee_id);                                
                                
                                if (label){                                    
                                    const box = resizedDetections.detection.box;
                                    const drawBox = new faceapi.draw.DrawBox(box, { label: label.toString()});
                                    drawBox.draw(canvas);
                                }

                                if (self.match_label && self.match_employee_id && match_count > 2){
                                    clearInterval(self.intervalID);
                                    if (!self.intervalId) {
                                        var image = self.$el.find("#image").get(0);
                                        image.width = $(video).width();
                                        image.height = $(video).height();
                                        image.getContext('2d').drawImage(video, 0, 0);
                                        var img64 = image.toDataURL("image/jpeg");
                                        img64 = img64.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
                                        self.update_attendance(self.match_employee_id, img64);
                                    }
                                }
                            }
                        }
                    }
                    else{
                        var canvas = self.$el.find("#canvas").get(0);
                        faceapi.matchDimensions(canvas, displaySize);
                    }               
                },200);
            }         
        },

        update_attendance: function(employee_id, img){
            var self = this;
            if (!self.intervalId && !self.is_update_attendance){
                self.parent._update_face_attendance(employee_id, img);
                self.is_update_attendance = true;
                self.match_label = '';
                self.match_employee_id = false;
                self._onDestroy();
            }
        },

        getName: function(employee_id){
            var self = this;            
            var prom = Promise.resolve();
            prom.then(function () {
                if (employee_id !== 'unknown'){
                    self._rpc({
                        route: `/attendance_face_recognition/getName/${employee_id}/`
                    })
                    .then(function(result){
                        if (result){
                            self.match_label = result;
                        }
                    })
                }                
            })
            return self.match_label; 
        },

        getFaceDetectorOptions: function() {
            let inputSize = 384; // by 32, common sizes are 128, 160, 224, 320, 416, 512, 608,
            let scoreThreshold = 0.5;
            return new faceapi.TinyFaceDetectorOptions(); // {inputSize, scoreThreshold }
        },

        getCurrentFaceDetectionNet: function() {
            return faceapi.nets.tinyFaceDetector;
        },

        isFaceDetectionModelLoaded: function() {
            return !!this.getCurrentFaceDetectionNet().params
        },
    });
    return FaceRecognitionDialog;

});