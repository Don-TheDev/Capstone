// function loadDoc() {
//   var xhttp = new XMLHttpRequest();
//   xhttp.onreadystatechange = function () {
//     if (this.readyState == 4 && this.status == 200) {
//       document.getElementById("demo").innerHTML = this.responseText;
//     }
//   };
//   xhttp.open("GET", "demo_get.asp", true);
//   xhttp.send();
// }

// $(".id_message_submit").click(function () {
//   var catid;
//   catid = $(this).attr("data-catid");
//   $.ajax({
//     type: "GET",
//     url: "/likepost",
//     data: {
//       post_id: catid,
//     },
//     success: function (data) {
//       $("#like" + catid).remove();
//       $("#message").text(data);
//     },
//   });
// });

// function opposite() {
//   var data = JSON.parse("{{data|escapejs}}");
//   var input = document.getElementById("input").value;
//   var result = document.getElementById("result");
//   var flag = 1;
//   for (var x in data) {
//     if (input.toLowerCase() == data[x][0].toLowerCase()) {
//       result.innerHTML = data[x][1];
//       flag = 0;
//     } else if (input.toLowerCase() == data[x][1].toLowerCase()) {
//       result.innerHTML = data[x][0];
//       flag = 0;
//     }
//   }
//   if (flag) {
//     result.innerHTML = "No results found";
//   }
// }

function submitOnEnter(event) {
  // if (event.which === 13 && !event.shiftKey) {
  if (event.which === 13) {
    // event.target.form.dispatchEvent(new Event("submit", { cancelable: true }));
    document.getElementById("id_message_submit").click();
    event.preventDefault(); // Prevents the addition of a new line in the text field (not needed in a lot of cases)
    // event.target.value = "";
    location.reload();
  }
}

messageInput = document.getElementById("id_message_input");
messageInput.addEventListener("keypress", submitOnEnter);

messageInput.focus();
messageInput.select();
