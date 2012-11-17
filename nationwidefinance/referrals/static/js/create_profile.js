var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};

$(function(){

	nationwide.utils.entity_selector_helper = function($select) {
		org_list = [[true,$("#org")],[true,$("#contact")],[true,$("#address")],[true, $("#submit_btn")]];
		
		if ($("select[name=metrics]").val() == 'custom') {
			org_list.push([true,$("#customize")]);
		} else {
			org_list.push([false,$("#customize")]);
		}

		conditons = {
			'org' : org_list,
			'indv' : [[false,$("#org")],[true,$("#contact")],[true,$("#address")],[false, $("#customize")],[true,$("#submit_btn")]]
		}

		result_function = nationwide.utils.show_hide;

		nationwide.utils.select_processor($select,conditons,result_function);
	}

	$("select[name=entity_type]").on('change',function(event){
		nationwide.utils.entity_selector_helper($(this));
	});

	$("select[name=metrics]").on('change',function(event){
		conditons = {
			'inherit' : [[false, $("#customize")]],
			'custom'  : [[true, $("#customize")]]
		}

		result_function = nationwide.utils.show_hide;

		nationwide.utils.select_processor($(this),conditons,result_function);
	});

	/** reset form after errors */
	nationwide.utils.entity_selector_helper($("select[name=entity_type]"));
	
});