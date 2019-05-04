originalHTML = $('#old').text().replace(/</g, '&lt;').replace(/>/g, '&gt;<br>');
newHTML = $('#new').text().replace(/</g, '&lt;').replace(/>/g, '&gt;<br>');

output = htmldiff(originalHTML, newHTML)
document.getElementById("output").innerHTML = output
