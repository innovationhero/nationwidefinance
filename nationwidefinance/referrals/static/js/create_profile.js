var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};

$(function(){
	$("select[name=is_organization]").on('change',function(event){
		if ($(this).val() == '0') {
			nationwide.utils.show_hide(true,$("#person_div"));
			nationwide.utils.show_hide(false,$("#org_div"));
		} else {
			nationwide.utils.show_hide(true,$("#org_div"));
			nationwide.utils.show_hide(false,$("#person_div"));
		}
	});
});