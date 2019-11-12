$(document).ready(function() {
  "use strict";

  var d = new Date();
  d.setMonth(d.getMonth() + 3);
  var expMonth = new Date(d.getFullYear(), d.getMonth(), d.getDate());

  var isAgree = $("#viewlet-survey").attr("isAgree");
  var enabled = $("#viewlet-consent").attr("data-enabled");
  var isQstAvailable = $("#viewlet-survey").attr("isQstAvailable");
  if (isAgree === "true" && enabled === "true" && isQstAvailable === "true" && getCookie("_q_answer") === "") {
    $("#viewlet-survey").show();
    $('#q-text').text(getCookie("_q_text")); //set question
    // set query form
    var q_type = getCookie("_q_type")
    sefForm(q_type);
    // deleteCookies();
  } else {
    return;
  }

  $("#radio-multi input[name='radioLikert']").click(function(event) {
    var radioValue = $("input[name='radioLikert']:checked").val();
    if (radioValue == "other (specify)") {
      $("#text-answer").prop("disabled", false);
      $("#text-answer").focus();
    } else {
      $("#text-answer").prop("disabled", true);
      $("#text-answer").val('')
    }
  });

  $("button[name='nap.consent.bt.submit']").click(function(event) {
    //setting answer cookie
    var radios = document.getElementsByName('radioLikert');
    var text = document.getElementById('text-answer');
    var answer = "";
    if (radios) {
      var choiced = $("input[name='radioLikert']:checked").val();
      answer += choiced;
    }
    if (text) {
      answer += text.value;
    }
    answer = answer.replace(/other \(specify\)/g, "");
    answer = answer.replace(/undefined/g,"");
    answer = answer.replace(/\n/g, ' ');
    if (answer !== "") {
      document.cookie = "_q_answer=" + answer + "; expires=" + expMonth + "; path=/";
      $("#viewlet-survey").hide();
    }
  });

  $("button[name='nap.consent.bt.abort']").click(function(event) {
    $("#withdraw-div").hide();
    $("#question-type").show();
    resizeViewlet();
  });

  //withdraw from survey
  $("button[name='nap.consent.bt.proceed']").click(function(event) {
    $("#withdraw-div").hide();
    event.preventDefault();
    localStorage.setItem("cns-status", "deactivated");
    localStorage.setItem("cns-status-date", new Date());
    document.cookie = "_user=; path=/";
  });

  resizeViewlet();

});

$(window).bind("pageshow", function(event) {
  // check status first
  var status = localStorage.getItem("cns-status");
  if (status !== null) {
    if (status === "activated") {
      var d = new Date();
      d.setMonth(d.getMonth() + 3);
      var expMonth = new Date(d.getFullYear(), d.getMonth(), d.getDate());
      /** DETECT AND RECORD FORWARD AND BACKWARD NAVIGATION **/
      // 3 is neutral, 1 is back, 2 is next
      var _nav = getCookie("_nav");

      if (_nav === "0") { //initial condition
        _nav = "3";
      } else {
        url_preff = localStorage.getItem("url_preff");
        url_curr = localStorage.getItem("url_curr");
        if (url_curr !== document.URL && url_preff !== document.referrer) { // press back or next
          if (url_preff === document.URL) { // press back -- but there is a condition
            _nav += "1"; // that can be mistakenly identify as press back
          } else {
            _nav += "2"; // press forward
          }
        }
      }
      localStorage.setItem("url_preff", document.referrer);
      localStorage.setItem("url_curr", document.URL);
      document.cookie = "_nav=" + _nav + "; expires=" + expMonth + "; path=/";
      document.cookie = "_time=" + (new Date()).getTime() + "; expires=" + expMonth + "; path=/";
    }
  }
  /** END OF BLOCK **/
});

function showWithdraw() {
  $("#question-type").hide();
  $("#withdraw-div").show();
  if ($("#viewlet-survey").width() < 500){
    document.getElementById("viewlet-survey").style.marginLeft = "0px";
    document.getElementById("viewlet-survey").style.width = "600px";
  }
}

function showGeneralQuestion(){
  var d = new Date();
  d.setMonth(d.getMonth() + 3);
  var expMonth = new Date(d.getFullYear(), d.getMonth(), d.getDate());

  var question = $("#viewlet-survey").attr("generalQuestion");
  question = question.substring(1,question.length-1)
  var attrs = question.split(", ");

  document.cookie = "_q_id=\"" + attrs[0] + "\"; expires=" + expMonth + "; path=/";
  document.cookie = "_q_type=\"" + attrs[1] + "\"; expires=" + expMonth + "; path=/";
  document.cookie = "_q_text=\"" + attrs[2] + "\"; expires=" + expMonth + "; path=/";
  document.cookie = "_q_choices=\"\"; expires=" + expMonth + "; path=/";
  document.cookie = "_q_high=\"\"; expires=" + expMonth + "; path=/";
  document.cookie = "_q_low=\"\"; expires=" + expMonth + "; path=/";
  document.cookie = "_q_answer=\"\"; expires=" + expMonth + "; path=/";

  $('#q-text').text(getCookie("_q_text"));
  var q_type = getCookie("_q_type")
  sefForm(q_type);
  document.getElementById("viewlet-survey").style.marginLeft = "250px";
  document.getElementById("viewlet-survey").style.width = "350px";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      var text = c.substring(name.length, c.length).replace("\"","").replace("\"","");
      return text;
    }
  }
  return "";
}

function resizeViewlet() {
  var radio_multi_text = document.getElementById('radio-multi-text');
  var radio_multi = document.getElementById('radio-multi');
  if (radio_multi_text || radio_multi) {
    document.getElementById("viewlet-survey").style.marginLeft = "250px";
    document.getElementById("viewlet-survey").style.width = "350px";
  }
}

function likert(q_type) {
  var choices = getCookie("_q_choices");
  choices = choices.substring(2, choices.length-2).split("', '");
  var text = '<div id="q-likert" class="likert-answer">' +
    '<div class="likert-answer">' +
    '<span id="q-low">'+getCookie("_q_low")+'</span>&nbsp;' +
    '<span>';
  for (var i = 0; i < choices.length; i++){
    text += '<input type="radio" id="'+choices[i]+'" name="radioLikert" value="'+choices[i]+'">' +
            '<label for="'+choices[i]+'">'+choices[i]+'</label>';
  }
  text += '</span>' +
    '&nbsp;<span id="q-high">'+getCookie("_q_high")+'</span>';
  if (q_type === "1"){
    text += '<span>' +
      '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' +
      '<input type="radio" id="radioNA" name="radioLikert" value="NA">' +
        '<label for="radioNA">N/A</label>' +
    '</span>';
  }
  text += '</div></div>';
  return text;
}

function textAnswer() {
  var text = '<div class="text-answer">'+
    '<textarea id="text-answer" rows="4" cols="100" maxlength="500"></textarea>' +
  '</div>';
  return text;
}

function radioMulti(q_type) {
  var choices = getCookie("_q_choices");
  choices = choices.substring(2, choices.length-2).split("', '");
  var text = '<div id="radio-multi" class="multi-answer">';
  for (var i = 0; i < choices.length; i++){
    text += '<div>' +
        '<input type="radio" id="' +choices[i]+'" name="radioLikert" value="'+choices[i]+'">' +
        '<label for="' + choices[i] + '">' + choices[i] +'</label>' +
    '</div>';
  }
  if (q_type === "4"){
    text += '<div>' +
      '<textarea disabled id="text-answer" maxlength="70"></textarea>' +
    '</div>';
  }
  text += '</div>';
  return text;
}

function sefForm(q_type){

  // if question type is likert
  if (q_type === "0" || q_type === "1"){
    $('#q-form').html(likert(q_type));
  }
  // if question type is text answer
  if (q_type === "3"){
    $('#q-form').html(textAnswer());
  }
  // if question type is radio multi or with text
  if (q_type === "2" || q_type === "4"){
    $('#q-form').html(radioMulti(q_type));
  }

  // set link if question is not text answer
  var links = "";
  if (q_type !== "3"){
      links+= '<div><a onclick="showGeneralQuestion()" style="font-weight: bold; color: white">give textual feedback</a></div>';
  }
  links += '<div><a onclick="showWithdraw()">withdraw from survey</a></div>';
  $('#links').html(links);
}

function deleteCookies(){
  document.cookie = "_q_text=; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/";
  document.cookie = "_q_type=; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/";
  document.cookie = "_q_choices=; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/";
  document.cookie = "_q_low=; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/";
  document.cookie = "_q_high=; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/";
}
