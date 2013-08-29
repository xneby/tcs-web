function ready(){
	$('.solution_name').click(function(){
		$('div.solution').hide();
		$('div#' + $(this).attr('id')).show();
	});
}

$(document).ready(ready);
