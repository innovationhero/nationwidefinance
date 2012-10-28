var nationwide = nationwide || {};

nationwide.utils = {};

nationwide.helpers = {};

/**
	Utility function to perform all Ajax GET and POST calls
*/
nationwide.utils.do_ajax = function (type, url, data, success, error) {
    return $.ajax({
            url: url,
	        type: type,
	        data: data,
	        headers: {
	               "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
	        },
	        success: success,
	        error: error
	    });
}

nationwide.utils.show_hide = function() {
	var show = arguments[0];
	var $elm = arguments[1];
	if (show) {
		$elm.show();
	} else{
		$elm.hide();
	}
}

nationwide.utils.select_processor = function() {
	var args = arguments;
	var result_function = args[0];
	var result_args = arguments.slice(1,args.lenght);

	var $select = args[0];

	if ($select.val() == '1') {
		result_function(result_args);
	}
}


/**
	Helper method for All Aajax failures
*/
nationwide.helpers.error = function() {
	alert('error');
};
