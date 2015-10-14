{% for json in queries_json %}manifold.insert_query({{ json|safe }});
{% endfor %}
$(document).ready(function () {
var query_exec_tuples = [];
{% for tuple in query_exec_tuples %} query_exec_tuples.push({'query_uuid':"{{ tuple.query_uuid }}"}); 
{% endfor %}
manifold.asynchroneous_exec(query_exec_tuples);
})
