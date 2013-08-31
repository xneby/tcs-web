function ready(){
	$('.solution_name').click(function(){
		$('div.solution').hide();
		$('div#' + $(this).attr('id')).show();
	});
	$('a.impl_name').click(function(){
		$('div.implementation').hide();
		$('div.implementation[data-id=' + $(this).attr('data-id') + ']').show();
	});
}

$(document).ready(ready);
