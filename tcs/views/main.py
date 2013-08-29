from tcs.shortcuts import redirect, login_required

@login_required
def main(request):
	return redirect('competitions-list')
	
