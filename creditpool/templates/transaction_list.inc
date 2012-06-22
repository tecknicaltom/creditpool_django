{% comment %}
Expects variables set:
 allow_confirm: boolean, whether to include the confirm buttons
 transactions: QuerySet of UserTransfer items
{% endcomment %}

{% load currency %}

<table border=1>
	<tr>
		{% if allow_confirm %}
		<th>Confirm?</th>
		{% endif %}
		<th>ID</th>
		<th>Date entered</th>
		<th>Cost</th>
		<th>Description</th>
		<th>Who did it?</th>
	</tr>

	{% for user_transaction in transactions %}
	{% with transaction=user_transaction.transfer %}
	<tr>
		{% if allow_confirm %}
			{% if not transaction.confirmed %}
		<td align=center><input type="checkbox" name="confirm" value="{{ transaction.pk }}" /></td>
			{% endif %}
		{% endif %}
		<td><a href="{{ transaction.get_absolute_url }}">{{ transaction.pk }}</a></td>
		<td>{{ transaction.entered }}</td>
		<td>{{ user_transaction.credit|currency }}</td>
		<td>{{ transaction.description }}</td>
		<td>{{ transaction.creator.get_full_name }} - {{ transaction.creator.username }}</td>
	</tr>
	{% endwith %}
	{% endfor %}
</table>
<p>
{% if allow_confirm %}
<input type="submit" name="action" value="Confirm Selected" />
<input type="submit" name="action" value="Confirm All" />
{% endif %}
