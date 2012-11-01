var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};

$(function(){
	$("select").on('change',function(event){

		result_function = nationwide.utils.show_hide;

		var conditons = {};
		var event_handler;

		if ($(this).attr('name').indexOf('referrer') > -1) {
			conditons = {
				'org' : [[false,$("#referrer_person_div")],[true,$("#referrer_org_div")]],
				'person' : [[false,$("#referrer_org_div")],[true,$("#referrer_person_div")]]
			};

		} else {
			conditons = {
				'org' : [[false,$("#referred_person_div")],[true,$("#referred_org_div")]],
				'person' : [[false,$("#referred_org_div")],[true,$("#referred_person_div")]]
			};
		}

		nationwide.utils.select_processor($(this),conditons,result_function);
	});
});