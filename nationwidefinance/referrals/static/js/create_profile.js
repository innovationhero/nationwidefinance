var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};


$(function(){

	nationwide.utils.entity_selector_helper = function($select) {

		org_list = [[true,$("#org")],[true,$("#contact")],[true,$("#address")],[true, $("#submit_btn")], [true, $("#paypal_btn")], [false, $("#profile_btn")]];
		
		if ($("select[name=inherit_from_plan]").val() == '0') {
			org_list.push([true,$("#customize")]);
		} else {
			org_list.push([false,$("#customize")]);
		}


		conditons = {
			'org' : org_list,
			'indv' : [[false,$("#org")],[true,$("#contact")],[true,$("#address")],[false, $("#customize")],[false, $("#depts")],[true,$("#submit_btn")], [false, $("#paypal_btn")], [true, $("#profile_btn")]]
		}

		result_function = nationwide.utils.show_hide;

		nationwide.utils.select_processor($select,conditons,result_function);
	}

	$("select[name=entity_type]").on('change',function(event){
		nationwide.utils.entity_selector_helper($(this));
	});

	$("#id_plan").on('change', function(event){
		if ($(this).val() == '') {return;}
		nationwide.utils.do_ajax('post', 
			'/referrals/get_plan_price/', 
			{'plan_id' : $(this).val()},
			function(data){
				$("input[name=a3]").val(data[0].price);
				$("input[name=item_name]").val("Nation Wide " + data[0].name + "");

			},
			function(data){
				alert("error");
			})
	});

	$("select[name=inherit_from_plan]").on('change',function(event){
		conditons = {
			'1' : [[false, $("#customize")]],
			'0'  : [[true, $("#customize")]]
		}

		result_function = nationwide.utils.show_hide;

		nationwide.utils.select_processor($(this),conditons,result_function);
	});

	/** reset form after errors */
	nationwide.utils.entity_selector_helper($("select[name=entity_type]"));

	$("input[type=image]").on('click', function(event){
		var frm_selector = "form[name=frm_create_profile]";
		var $profile_form = $(frm_selector);
		var $paypal_form = $(this).parent();

		// setup jQuery Plugin 'ajaxForm'
    	var options = {
        		dataType:  'json',
        		beforeSubmit : function() {
        			$("#screen").css({"display": "block", 
        				opacity: 0.7, 
        				"width":$(document).width(),
        				"height":$(document).height(),
        				"background-image" : "url(/static/images/spinner.gif)",
        				"background-repeat" : "no-repeat"});
        		},
        		success: function(json){
        			$("#screen").css('display', 'none');
        			json = json[0];
        			if (json.status == 500) {
        				//clear all existing errors:
        				var $inputs = $profile_form.find("input[type=text]");
        				var $selects = $profile_form.find("select");

        				$.each($inputs, function() {
        					$(this).parent().next().html('');
        				});

        				$.each($selects, function() {
        					$(this).parent().next().html('');
        				});

        				var errors = json.errors;
        				
        				$.each(errors, function(key, value){
        					var $elm = $("input[name=" + key +"]");
        					
        					if ($elm.length == 0) {
        						$elm = $("select[name=" + key + "]");
        					}
        					
        					var $div = $elm.parent().next();
        					$div.html(value);
        					$div.css('color', 'red');	
        					
        					
        				});
        			} else {
        				$paypal_form.submit();
        			}
        			
    	   		}
    	};

		

		$profile_form.ajaxForm(options);
		$profile_form.submit();
		return false;
		
	});

	
});