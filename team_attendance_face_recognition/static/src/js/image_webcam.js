odoo.define('team_attendance_face_recognition.image_webcam', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var FieldBinaryImage = basic_fields.FieldBinaryImage;

    var utils = require('web.utils');
    var Dialog = require('web.Dialog');
    
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;

    FieldBinaryImage.include({
        events: _.extend({}, FieldBinaryImage.prototype.events, {
            'click button.o_web_cam_button': 'on_webcam_open',
        }),
        init: function(parent, options) {
            this._super.apply(this, arguments);     
            if (this.model == 'hr.employee.faces'){                
                this.load_models = this.load_models();
                this.load_label = $.Deferred();
            }
        },

        load_models: async function(){
            var self = this;
            return await Promise.all([
                faceapi.nets.tinyFaceDetector.load('/team_attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceLandmark68Net.load('/team_attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceLandmark68TinyNet.load('/team_attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceRecognitionNet.load('/team_attendance_face_recognition/static/src/lib/weights'),
                faceapi.nets.faceExpressionNet.load('/team_attendance_face_recognition/static/src/lib/weights'),
            ]).then(function(){
                self.load_label.resolve();
            });
        },        

        on_webcam_open: function(){
            var self = this;
            var has_Detection_model = this.isFaceDetectionModelLoaded();
            var has_Recognition_model = this.isFaceRecognitionModelLoaded();
            var has_Landmark_model = this.isFaceLandmarkModelLoaded();
            if (has_Detection_model && has_Recognition_model && has_Landmark_model){
                self.on_webcam_uploaded();
            }
        },
        on_webcam_uploaded: function(){
            var self = this;
            this.dialog = new Dialog(this, {
                size: 'medium',
                title: _t("Capture Snapshot"),
                $content: QWeb.render('WebCamDialog'),
                buttons: [
                    {
                        text: _t("Capture Snapshot"), classes: 'btn-primary captureSnapshot',                       
                    },
                    {
                        text: _t("Close"), classes:'btn-secondary captureClose', close: true,
                    }
                ]
            }).open();

            this.dialog.opened().then(function () {  
                var video = self.dialog.$('#video').get(0);
                navigator.getUserMedia = navigator.getUserMedia 
                    || navigator.webkitGetUserMedia 
                    || navigator.mozGetUserMedia;
                
                if (navigator.getUserMedia) {
                    var openRecognition = navigator.getUserMedia(
                        { video: {} },
                        function(stream) {                                             
                            video.srcObject = stream; 
                            video.play(); 
                            video.muted = true;                            
                        },
                        function(err) {
                            console.log("onloadedmetadata");
                        }
                    );
                }

                var $captureSnapshot = self.dialog.$footer.find('.captureSnapshot');
                var $closeBtn = self.dialog.$footer.find('.captureClose');

                $captureSnapshot.on('click', function (event){
                    var img64="";
                    var image = self.dialog.$('#image').get(0);
                    image.width = $(video).width();
                    image.height = $(video).height();
                    image.getContext('2d').drawImage(video, 0, 0, image.width, image.height);
                    var img64 = image.toDataURL("image/jpeg");
                    img64 = img64.replace(/^data:image\/(png|jpg|jpeg|webp);base64,/, "");

                    if (img64){
                        var file = {};
                        self.on_file_uploaded(file.size, "webcam.jpeg", "image/jpeg", img64);
                        $closeBtn.click();
                    }

                    $captureSnapshot.text("uploading....").addClass('disabled');
                });

            });
        },
        on_file_uploaded: function (size, name) {
            this._super.apply(this, arguments);
            var self = this;
            var recordData = _.find(Object.keys(this.recordData), function(o) {
                return o.startsWith('descriptor');
            }); 
            var descriptor = this.nodeOptions.descriptor_field;
            if (descriptor !== 'undefined' && recordData){
                if (recordData == descriptor) {
                    if (arguments){
                        var img = "data:image/jpeg;base64," + arguments[3];
                        self.updateDescriptor(img);
                    }                    
                }
            }

        },
        on_file_change: function (e) {
            this._super.apply(this, arguments);
            var self = this;
            var recordData = _.find(Object.keys(this.recordData), function(o) {
                return o.startsWith('descriptor');
            });            
            
            var file_node = e.target;
            var file = file_node.files[0];

            var descriptor = this.nodeOptions.descriptor_field;
            if (descriptor !== 'undefined' && recordData){                
                if (recordData == descriptor) {
                    utils.getDataURLFromFile(file).then(function (data) {                   
                        self.updateDescriptor(data);
                    });                                      
                    
                } 
            }
        },
        updateDescriptor: function(data){            
            var self = this;
            var has_Detection_model = this.isFaceDetectionModelLoaded();
            var has_Recognition_model = this.isFaceRecognitionModelLoaded();
            var has_Landmark_model = this.isFaceLandmarkModelLoaded();

            return new Promise(async function (resolve, reject) {                
                if (has_Detection_model && has_Recognition_model && has_Landmark_model){
                    var img = document.createElement('img');
                    img.src= data;
                    const faceResults = await faceapi.detectSingleFace(img, new faceapi.TinyFaceDetectorOptions())
                        .withFaceLandmarks()
                        .withFaceDescriptor();
                    if (faceResults != undefined && faceResults && faceResults.descriptor){
                        self.trigger_up('field_changed', {
                            dataPointID: self.dataPointID,
                            changes: {
                                descriptor: self.formatDescriptor(faceResults.descriptor),                                
                            },
                            viewType: 'form',
                            onSuccess: resolve,
                            onFailure: reject,
                        });
                    }
                }else{
                    return setTimeout(() => this.updateDescriptor())
                }
            })
        },

        formatDescriptor: function(descriptor) {
            var self = this;
            let result = window.btoa(String.fromCharCode(...(new Uint8Array(descriptor.buffer))));
            return result;
        },

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
});