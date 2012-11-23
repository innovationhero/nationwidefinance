var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};


$(function(){

	nationwide.utils.entity_selector_helper = function($select) {
		org_list = [[true,$("#org")],[true,$("#contact")],[true,$("#address")],[true, $("#submit_btn")]];
		
		if ($("select[name=inherit_from_plan]").val() == '0') {
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

	$("input[name=referrer-email],input[name=referred-email]").on('keyup', function(){
		var self = $(this);
		$(this).autocomplete({
            minLength : 3,
            source : function(request, response) {
                var data = {};
                data['email'] = request.term;
                var result = nationwide.utils.do_ajax('post','/referrals/add_referral_autocomplete/',data,function(data) {response(data)});
            },
            select : function(event, ui) {
            	name = self.attr('name').substring(0,self.attr('name').indexOf('-')+1);
            	$("input[name="+name+"email]").blur();
            	$("input[name="+name+"email]").val(ui.item.email);
            	$("input[name="+name+"first_name]").val(ui.item.first_name);
            	$("input[name="+name+"last_name]").val(ui.item.last_name);
            	$("input[name="+name+"dob]").val(ui.item.dob);
            	return false;

            }
        }).data( "autocomplete" )._renderItem = function( ul, item ) {
            return $( "<li>" ).data( "item.autocomplete", item ).append( "<a>"+item.email+"</a>" ).appendTo( ul );
        };
    });
});