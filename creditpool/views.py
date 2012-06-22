from django.shortcuts import render_to_response
from django.template import RequestContext
from decimal import Decimal
import re
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

def new_transaction(request):
	transaction_users = get_users().filter(pk__in=request.GET.getlist('user'))
	context = {
			'transaction_users': transaction_users,
	}
	return render_to_response('new_transaction.html', RequestContext(request, context))

def confirm_transaction(request):
	user_pks = []
	for (key, value) in request.GET.items():
		result = re.match(r'^val_(?P<pk>\d+)$', key)
		if result:
			user_pks.append(result.group('pk'))
	transaction_users = get_users().filter(pk__in=user_pks)
	my_transaction_amt = Decimal(0)
	for transaction_user in transaction_users:
		transaction_user.transaction_amt = Decimal(request.GET['val_%d' % transaction_user.pk])
		my_transaction_amt -= transaction_user.transaction_amt

	old_balance = request.user.userprofile.credit
	new_balance = old_balance + my_transaction_amt

	context = {
			'transaction_users': transaction_users,
			'transaction_description': request.GET['descrip'],
			'my_transaction_amt': my_transaction_amt,
			'old_balance': old_balance,
			'new_balance': new_balance,
	}
	return render_to_response('confirm_transaction.html', RequestContext(request, context))
