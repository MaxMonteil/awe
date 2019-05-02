originalHTML=""
newHTML=""

$.ajax({
    url : "/static/diff/before.html",
	async:false,
    success : function(result){
        originalHTML = result;
    }
});

$.ajax({
    url : "/static/diff/after.html",
	async:false,
    success : function(result){
        newHTML = result;
    }
});

originalHTML = originalHTML.replace(/</g, '&lt;').replace(/>/g, '&gt;<br>');
newHTML = newHTML.replace(/</g, '&lt;').replace(/>/g, '&gt;<br>');

output = htmldiff(originalHTML, newHTML)
document.getElementById("output").innerHTML = output
