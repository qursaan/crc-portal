/**
 * Description: implements a wizard-like interface
 * Copyright (c) 2013 UPMC Sorbonne Universite
 * Based on SmartWizard 2.0 plugin by Dipu (http://www.techlaboratory.net)
 * License: GPLv3
 */

/*
 * It's a best practice to pass jQuery to an IIFE (Immediately Invoked Function
 * Expression) that maps it to the dollar sign so it can't be overwritten by
 * another library in the scope of its execution.
 */
(function($){

    /***************************************************************************
     * Method calling logic
     ***************************************************************************/

    $.fn.Wizard = function( method ) {
        if ( methods[method] ) {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            //$.error( 'Method ' +  method + ' does not exist on jQuery.Wizard' );
            return undefined;
        }    
    };

    /***************************************************************************
     * Public methods
     ***************************************************************************/

    var methods = {

        /**
         * @brief Plugin initialization
         * @param options : an associative array of setting values
         * @return : a jQuery collection of objects on which the plugin is
         *     applied, which allows to maintain chainability of calls
         */
        init : function ( options ) {

            /* Default settings */
            var options = $.extend({}, $.fn.Wizard.defaults, options);

            return this.each(function() {
                var $this = $(this);
                var obj = $(wizard, this);

                /* An object that will hold private variables and methods */
                var form = new Wizard(options, obj);
                $this.data('Wizard', form);

                form.init();

//                // Initialize the smart-wizard third-party jquery plugin
//                $(wizard, this).smartWizard({
//                    selected    : options.start_step - 1,
//                    errorSteps  : [5],
//                    onLeaveStep : leaveAStepCallback,
////                  onFinish    : onFinishCallback
//                });
//
//                // XXX Mark some steps as done !
//                $(wizard, this).smartWizard('setDone',{stepnum: 1, isdone:true});
//
//                function leaveAStepCallback(obj){
//                    var step_num= obj.attr('rel')-1; // get the current step number
//                    func = options.validate_step_js[step_num];
//                    if (func == 'null')
//                        return true;
//                    return window[func]();
//                }
//
//                function onFinishCallback(){
//                    window.location.href('/');
//                }


            }); // this.each
        } // init

    };

    /***************************************************************************
     * Wizard object
     ***************************************************************************/

    /**
     * \param options (dict) : a dictionary of options
     * \param obj (jQuery ref) : handler to the wizard plugin
    */
    function Wizard(options, obj) {

        /* save a reference to this */
        var $this = this;

        /* member variables */
        this.options = options;

        /* methods */

        /**
         * \brief get a handle on a wizard step by id
           \param stepIdx (integer) : step identifier (0-based)
           \returns jQuery selector
         */
        this.get_step = function(stepIdx) { return $('.plugin', $(stepIdx.attr('href'))); }

        this.get_plugin = function(step) { return step.data().plugin; }

        this.init1 = function() {
            $this.curStepIdx = options.selected;
            $this.steps = $("ul > li > a[href^='#step-']", obj); // Get all anchors in this array
            $this.contentWidth = 0;
            //this.loader,msgBox,elmActionBar,elmStepContainer,btNext,btPrevious,btFinish;
            
            $this.elmActionBar = $('.actionBar',obj);
            if($this.elmActionBar.length == 0){
              $this.elmActionBar = $('<div></div>').addClass("actionBar");                
            }

            $this.msgBox = $('.msgBox',obj);
            if($this.msgBox.length == 0){
              $this.msgBox = $('<div class="msgBox"><div class="content"></div><a href="#" class="close">X</a></div>');
              $this.elmActionBar.append($this.msgBox);                
            }
            
            $('.close',$this.msgBox).click(function() {
                $this.msgBox.fadeOut("normal");
                return false;
            });
        } // this.init1

        this.init = function() {
            this.init1();

            var allDivs =obj.children('div'); //$("div", obj);                
            obj.children('ul').addClass("anchor");
            allDivs.addClass("content");
            // Create Elements
            loader = $('<div>Loading</div>').addClass("loader");
            elmActionBar = $('<div></div>').addClass("actionBar");
            elmStepContainer = $('<div></div>').addClass("stepContainer");
            btNext = $('<a>'+options.labelNext+'</a>').attr("href","#").addClass("buttonNext");
            btPrevious = $('<a>'+options.labelPrevious+'</a>').attr("href","#").addClass("buttonPrevious");
            btFinish = $('<a>'+options.labelFinish+'</a>').attr("href","#").addClass("buttonFinish");
            
            // highlight steps with errors
            if(options.errorSteps && options.errorSteps.length>0){
              $.each(options.errorSteps, function(i, n){
                $this.setError(n,true);
              });
            }


            elmStepContainer.append(allDivs);
            elmActionBar.append(loader);
            obj.append(elmStepContainer);
            obj.append(elmActionBar); 
            if (options.includeFinishButton) {
              elmActionBar.append(btFinish);
            }
            elmActionBar.append(btNext).append(btPrevious); 
            contentWidth = elmStepContainer.width();

            $(btNext).click(function() {
                if($(this).hasClass('buttonDisabled')){
                  return false;
                }
                $this.doForwardProgress();
                return false;
            }); 
            $(btPrevious).click(function() {
                if($(this).hasClass('buttonDisabled')){
                  return false;
                }
                $this.doBackwardProgress();
                return false;
            }); 
            $(btFinish).click(function() {
                if(!$(this).hasClass('buttonDisabled')){
                   if($.isFunction(options.onFinish)) {
                      if(!options.onFinish.call(this,$(this.steps))){
                        return false;
                      }
                   }else{
                     var frm = $(obj).parents('form');
                     if(frm && frm.length){
                       frm.submit();
                     }                         
                   }                      
                }

                return false;
            }); 
            
            $(this.steps).bind("click", function(e){
                if(steps.index(this) == $this.curStepIdx){
                  return false;                    
                }
                var nextStepIdx = steps.index(this);
                var isDone = steps.eq(nextStepIdx).attr("isDone") - 0;
                if(isDone == 1){
                  $this.LoadContent(nextStepIdx);                    
                }
                return false;
            }); 
            
            // Enable keyboard navigation                 
            if(options.keyNavigation){
                $(document).keyup(function(e){
                    if(e.which==39){ // Right Arrow
                      $this.doForwardProgress();
                    }else if(e.which==37){ // Left Arrow
                      $this.doBackwardProgress();
                    }
                });
            }
            //  Prepare the steps
            this.prepareSteps();
            // Show the first slected step
            this.LoadContent($this.curStepIdx);                  
        }

        this.prepareSteps = function() {
            if (!options.enableAllSteps) {
                $(this.steps, obj).removeClass("selected").removeClass("done").addClass("disabled"); 
                $(this.steps, obj).attr("isDone",0);                 
            } else {
                $(this.steps, obj).removeClass("selected").removeClass("disabled").addClass("done"); 
                $(this.steps, obj).attr("isDone",1); 
            }

            $(this.steps, obj).each(function(i){
                $($(this).attr("href"), obj).hide();
                $(this).attr("rel",i+1);
            });
        }
                    
        this.LoadContent = function(stepIdx) {
            var selStep = this.steps.eq(stepIdx);
            var ajaxurl = options.contentURL;
            var hasContent =  selStep.data('hasContent');
            stepNum = stepIdx+1;
            if(ajaxurl && ajaxurl.length>0){
               if(options.contentCache && hasContent){
                   this.showStep(stepIdx);                          
               }else{
                   $.ajax({
                    url: ajaxurl,
                    type: "POST",
                    data: ({step_number : stepNum}),
                    dataType: "text",
                    beforeSend: function(){ loader.show(); },
                    error: function(){loader.hide();},
                    success: function(res){ 
                      loader.hide();       
                      if(res && res.length>0){  
                         selStep.data('hasContent',true);            
                         $($(selStep, obj).attr("href"), obj).html(res);
                         this.showStep(stepIdx);
                      }
                    }
                  }); 
              }
            }else{
              this.showStep(stepIdx);
            }
        } // this.LoadContent
                    
        this.showStep = function(stepIdx) 
        {
            var selStep = this.steps.eq(stepIdx); 
            var curStep = this.steps.eq($this.curStepIdx);


            if(stepIdx != $this.curStepIdx){
              if($.isFunction(options.onLeaveStep)) {
                if(!options.onLeaveStep.call(this,$(curStep))){
                  return false;
                }
              }
            }     
            if (options.updateHeight)
                elmStepContainer.height($($(selStep, obj).attr("href"), obj).outerHeight());               
            if(options.transitionEffect == 'slide'){
              $($(curStep, obj).attr("href"), obj).slideUp("fast",function(e){
                    $($(selStep, obj).attr("href"), obj).slideDown("fast");
                    $this.curStepIdx =  stepIdx;                        
                    $this.SetupStep(curStep,selStep);
                  });
            } else if(options.transitionEffect == 'fade'){                      
              $($(curStep, obj).attr("href"), obj).fadeOut("fast",function(e){
                    $($(selStep, obj).attr("href"), obj).fadeIn("fast");
                    $this.curStepIdx =  stepIdx;                        
                    $this.SetupStep(curStep,selStep);                           
                  });                    
            } else if(options.transitionEffect == 'slideleft'){
                var nextElmLeft = 0;
                var curElementLeft = 0;
                if(stepIdx > $this.curStepIdx){
                    nextElmLeft1 = contentWidth + 10;
                    nextElmLeft2 = 0;
                    curElementLeft = 0 - $($(curStep, obj).attr("href"), obj).outerWidth();
                } else {
                    nextElmLeft1 = 0 - $($(selStep, obj).attr("href"), obj).outerWidth() + 20;
                    nextElmLeft2 = 0;
                    curElementLeft = 10 + $($(curStep, obj).attr("href"), obj).outerWidth();
                }
                if(stepIdx == $this.curStepIdx){
                    nextElmLeft1 = $($(selStep, obj).attr("href"), obj).outerWidth() + 20;
                    nextElmLeft2 = 0;
                    curElementLeft = 0 - $($(curStep, obj).attr("href"), obj).outerWidth();                           
                }else{
                    $($(curStep, obj).attr("href"), obj).animate({left:curElementLeft},"fast",function(e){
                      $($(curStep, obj).attr("href"), obj).hide();
                    });                       
                }

                $($(selStep, obj).attr("href"), obj).css("left",nextElmLeft1);
                $($(selStep, obj).attr("href"), obj).show();
                $($(selStep, obj).attr("href"), obj).animate({left:nextElmLeft2},"fast",function(e){
                  $this.curStepIdx =  stepIdx;                        
                  $this.SetupStep(curStep,selStep);                      
                });
            } else{
                $($(curStep, obj).attr("href"), obj).hide(); 
                $($(selStep, obj).attr("href"), obj).show();
                $this.curStepIdx =  stepIdx;                        
                $this.SetupStep(curStep,selStep);
            }
            return true;
        } // this.showStep
                    
        this.SetupStep = function(curStep,selStep)
        {
            $(curStep, obj).removeClass("selected");
            $(curStep, obj).addClass("done");
            
            $(selStep, obj).removeClass("disabled");
            $(selStep, obj).removeClass("done");
            $(selStep, obj).addClass("selected");
            $(selStep, obj).attr("isDone",1);
            $this.adjustButton();
            if($.isFunction(options.onShowStep)) {
               if(!options.onShowStep.call(this,$(selStep))){
                 return false;
               }
            } 
        }                

        this.validate_callback = function(validated) {
            /* In case of failure, inform the user of what went wrong */
            if (!validated) {
                return;
            }
            
            /* Otherwise, proceed to next step */
            $this.GoToNextStep();
        }
    
        this.doForwardProgress = function()
        {
            var curStep = this.steps.eq($this.curStepIdx);
            var step = this.get_step(curStep);
            var plugin = this.get_plugin(step);

            /* If the plugin has a validate method, trigger it and wait for
             * callback */
            if (plugin.validate) {
                /* Trigger validation code and wait for callback */
                // XXX We should inform the user about progress and disable buttons 
                plugin.validate(this.validate_callback);
                return;
            }

            /* Otherwise, proceed to next step */
            this.GoToNextStep();
        }
        
        this.GoToNextStep = function()
        {
            var nextStepIdx = $this.curStepIdx + 1;

            if(this.steps.length <= nextStepIdx){
                if (!options.cycleSteps) {
                    return false;
                }                  
                nextStepIdx = 0;
            }
            this.LoadContent(nextStepIdx);
        }
                    
        this.doBackwardProgress = function()
        {
            var nextStepIdx = $this.curStepIdx-1;
            if(0 > nextStepIdx){
              if(!options.cycleSteps){
                return false;
              }
              nextStepIdx = this.steps.length - 1;
            }
            this.LoadContent(nextStepIdx);
        }  
                    
        this.adjustButton = function()
        {
            if(!options.cycleSteps){                
              if(0 >= $this.curStepIdx){
                $(btPrevious).addClass("buttonDisabled");
              }else{
                $(btPrevious).removeClass("buttonDisabled");
              }
              if(($this.steps.length-1) <= $this.curStepIdx){
                $(btNext).addClass("buttonDisabled");
              }else{
                $(btNext).removeClass("buttonDisabled");
              }
            }
            // Finish Button 
            if(!$this.steps.hasClass('disabled') || options.enableFinishButton){
              $(btFinish).removeClass("buttonDisabled");
            }else{
              $(btFinish).addClass("buttonDisabled");
            }                  
        }
                    
        this.showMessage = function(msg)
        {
            $('.content',msgBox).html(msg);
            msgBox.show();
        }
                    
        this.setError = function(stepnum,iserror)
        {
            if(iserror){                    
              $(this.steps.eq(stepnum-1), obj).addClass('error')
            }else{
              $(this.steps.eq(stepnum-1), obj).removeClass("error");
            }                                   
        }                        

        this.setDone = function(stepnum,isdone)
        {
            if(isdone){                    
              $(this.steps.eq(stepnum-1), obj).removeClass("selected").removeClass("disabled").addClass('done')
            }else{
              $(this.steps.eq(stepnum-1), obj).removeClass("done");
            }                                   
        }
    }

    /// KEEP BELOW

    // Default Properties and Events
    $.fn.Wizard.defaults = {
        selected: 0,  // Selected Step, 0 = first step   
        keyNavigation: true, // Enable/Disable key navigation(left and right keys are used if enabled)
        enableAllSteps: false,
        updateHeight: true,
        transitionEffect: 'fade', // Effect on navigation, none/fade/slide/slideleft
        contentURL:null, // content url, Enables Ajax content loading
        contentCache:true, // cache step contents, if false content is fetched always from ajax url
        cycleSteps: false, // cycle step navigation
        includeFinishButton: true, // whether to show a Finish button
        enableFinishButton: false, // make finish button enabled always
        errorSteps:[],    // Array Steps with errors
        labelNext:'Next',
        labelPrevious:'Previous',
        labelFinish:'Finish',          
        onLeaveStep: null, // triggers when leaving a step
        onShowStep: null,  // triggers when showing a step
        onFinish: null  // triggers when Finish button is clicked
    };    

})( jQuery );
