var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};

$(function(){
	$("select[name=is_organization]").on('change',function(event){

		conditons = {
			'0' : [[false,$("#org_div")],[true,$("#person_div")]],
			'1' : [[true,$("#org_div")],[false,$("#person_div")]]
		}
		result_function = nationwide.utils.show_hide;

		nationwide.utils.select_processor($(this),conditons,result_function);
	});
});