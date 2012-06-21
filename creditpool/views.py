from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *

def get_users():
	# this should look for users that are part of a group, and creates a UserProfile
	# if one doesn't exist. Will also take into account deactivating users (globally
	# and within creditpool)
	#return [profile.user for profile in UserProfile.objects.all()]
	return User.objects.filter(userprofile__isnull=False)

def index(request):
	users = get_users()
	total_imbalance = sum([abs(u.userprofile.credit) for u in users]) / 2
	average_imbalance = total_imbalance / users.count()
	#throughput = UserTransfer.objects.extra(select={'abs_credit':'ABS(credit)'}).aggregate(throughput
	throughput = sum([abs(xfer.credit) for xfer in UserTransfer.objects.all()]) / 2
	context = {
			'users': users,
			'unconfirmed_transactions': request.user.usertransfer_set.filter(confirmed=False),
			'history': 7,
			'total_imbalance': total_imbalance,
			'average_imbalance': average_imbalance,
			'throughput': throughput,
	}
	return render_to_response('index.html', RequestContext(request, context))
