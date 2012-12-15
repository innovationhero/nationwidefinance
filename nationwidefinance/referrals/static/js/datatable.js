var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};

nationwide.utils.datatable_factory = function(server_side, aaData, aoColumns, col0, fnRowCallback) {


	var Abstract_Datatable = {
		"bDestroy"        : true,
		"bJQueryUI"       : true,
		"bPaginate"       : true,
        "bLengthChange"   : false,
        "iDisplayLength"  : 15,
        "bFilter"         : false,
        "bSort"           : true,
        "bInfo"           : true,
        "bAutoWidth"      : false,
        "bProcessing"     : true,
        "bServerSide"     : server_side,
        "sPaginationType" : "full_numbers",
        "aaData"          :  aaData,
        "aoColumns"       : aoColumns,
		fnRowCallback     : fnRowCallback
		
	};
	return Abstract_Datatable;

}