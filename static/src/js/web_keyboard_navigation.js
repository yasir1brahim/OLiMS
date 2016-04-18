$.ctrl = function(key, callback, args) {
    $(document).keydown(function(e) {
        if(!args) args=[]; // IE barks when args is null 
        if((e.keyCode == key.charCodeAt(0) || e.keyCode == key) && e.ctrlKey) {
            callback.apply(this, args);
            return false;
        }
    });        
};

//Edit the current object
$.ctrl('E', function() {
	$('.oe_form_button_edit').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Save the current object
$.ctrl('S', function() {
	$('.oe_form_button_save').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Cancel the current object edition
$.ctrl('Z', function() {
	$('.oe_form_button_cancel').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//New object
$.ctrl('C', function() {
	$('button[accessKey="C"]').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
	$('.oe_list_add').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Previous object
$.ctrl('38', function() {
	$('.oe-pager-button[data-pager-action="previous"]').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});

//Next object
$.ctrl('40', function() {
	$('.oe-pager-button[data-pager-action="next"]').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
});