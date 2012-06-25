from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from datetime import datetime, timedelta
from decimal import Decimal
import re
from models import *

def get_users():
	# this should look for users that are part of a group, and creates a UserProfile
	# if one doesn't exist. Will also take into account deactivating users (globally
	# and within creditpool)
	#return [profile.user for profile in UserProfile.objects.all()]
	return User.objects.filter(userprofile__isnull=False)

def parse_request_amts(params, me):
	user_pks = []
	for (key, value) in params.items():
		result = re.match(r'^val_(?P<pk>\d+)$', key)
		if result:
			pk = int(result.group('pk'))
			if pk != me.pk:
				user_pks.append(pk)
	transaction_users = get_users().filter(pk__in=user_pks)
	my_transaction_amt = Decimal(0)
	for transaction_user in transaction_users:
		transaction_user.transaction_amt = Decimal(params['val_%d' % transaction_user.pk])
		my_transaction_amt -= transaction_user.transaction_amt
	return (transaction_users, my_transaction_amt)

def error(request, message):
	context = {
			'message': message,
	}
	return render_to_response('creditpool/error.html', RequestContext(request, context))

def index(request):
	users = get_users()
	total_imbalance = sum([abs(u.userprofile.credit) for u in users]) / 2
	average_imbalance = total_imbalance / users.count()
	#throughput = UserTransaction.objects.extra(select={'abs_credit':'ABS(credit)'}).aggregate(throughput
	throughput = sum([abs(xfer.credit) for xfer in UserTransaction.objects.all()]) / 2
	history_days = request.user.userprofile.history_days
	recent_transactions = request.user.usertransaction_set.filter(transaction__entered__gte=datetime.now()-timedelta(days=history_days))

	context = {
			'users': users,
			'unconfirmed_transactions': request.user.usertransaction_set.filter(confirmed=False),
			'total_imbalance': total_imbalance,
			'average_imbalance': average_imbalance,
			'throughput': throughput,
			'recent_transactions': recent_transactions,
	}
	return render_to_response('creditpool/index.html', RequestContext(request, context))

def new_transaction(request):
	transaction_users = get_users().filter(pk__in=request.GET.getlist('user'))
	if transaction_users.count() == 0:
		return error(request, 'Nobody selected!')
	context = {
			'transaction_users': transaction_users,
	}
	return render_to_response('creditpool/new_transaction.html', RequestContext(request, context))

def confirm_transaction(request):
	(transaction_users, my_transaction_amt) = parse_request_amts(request.GET, request.user)
	old_balance = request.user.userprofile.credit
	new_balance = old_balance + my_transaction_amt

	context = {
			'transaction_users': transaction_users,
			'transaction_description': request.GET['descrip'],
			'my_transaction_amt': my_transaction_amt,
			'old_balance': old_balance,
			'new_balance': new_balance,
	}
	return render_to_response('creditpool/confirm_transaction.html', RequestContext(request, context))

def commit_transaction(request):
	(transaction_users, my_transaction_amt) = parse_request_amts(request.POST, request.user)

	transaction = GlobalTransaction(creator=request.user, description=request.POST['descrip'])
	transaction.save()
	for transaction_user in transaction_users:
		user_transaction = UserTransaction(transaction=transaction, user=transaction_user, credit=transaction_user.transaction_amt)
		user_transaction.save();
		transaction_user.userprofile.credit += transaction_user.transaction_amt
		transaction_user.userprofile.save()

	user_transaction = UserTransaction(transaction=transaction, user=request.user, credit=my_transaction_amt)
	user_transaction.save();
	request.user.userprofile.credit += my_transaction_amt
	request.user.userprofile.save()

	return redirect(transaction)

def transaction(request, id):
	transaction = get_object_or_404(GlobalTransaction, pk=id)
	context = {
			'transaction': transaction,
	}
	return render_to_response('creditpool/transaction.html', RequestContext(request, context))

def change_history(request):
	try:
		request.user.userprofile.history_days = int(request.POST['history'])
		request.user.userprofile.save()
	except:
		pass
	return redirect(index)
