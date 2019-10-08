$(document).ready(function() {
  "use strict";
  var d = new Date();
  d.setMonth(d.getMonth() + 3);
  var expMonth = new Date(d.getFullYear(), d.getMonth(), d.getDate());

  var isAgree = $("#viewlet-survey").attr("isAgree");
  var enabled = $("#viewlet-consent").attr("data-enabled");
  var isQstAvailable = $("#viewlet-survey").attr("isQstAvailable");
  if (isAgree === "true" && enabled === "true" && isQstAvailable === "true" && getCookie("_q_answer") === "\"\"") {
    $("#viewlet-survey").show();
  } else {
    return;
  }

  $("#radio-multi-text input[name='radioLikert']").click(function(event) {
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
      answer += $("input[name='radioLikert']:checked").val();
    }
    if (text) {
      answer += text.value;
    }
    if (answer !== "undefined" && answer !== "") {
      document.cookie = "_q_answer=" + answer + "; expires=" + expMonth + "; path=/";
      $("#viewlet-survey").hide();
    }
  });

  $("button[name='nap.consent.bt.abort']").click(function(event) {
    $("#withdraw-div").hide();
    $("#question-type").show();
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
  if (status !== null){
    if (status === "activated"){
      var d = new Date();
      d.setMonth(d.getMonth() + 3);
      var expMonth = new Date(d.getFullYear(), d.getMonth(), d.getDate());
      /** DETECT AND RECORD FORWARD AND BACKWARD NAVIGATION **/
      // 3 is neutral, 1 is back, 2 is next
      var _nav = getCookie("_nav");
      if (_nav === "\"0\"") {        //initial condition
        _nav = "3";
      }else{
        url_preff = localStorage.getItem("url_preff");
        url_curr = localStorage.getItem("url_curr");
        if (url_curr !== document.URL && url_preff !== document.referrer){ // press back or next
          if(url_preff === document.URL){ // press back -- but there is a condition
            _nav += "1";                  // that can be mistakenly identify as press back
          }else{
            _nav += "2";      // press forward
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
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function resizeViewlet(){
  var radio_multi_text = document.getElementById('radio-multi-text');
  var radio_multi = document.getElementById('radio-multi');
  if (radio_multi_text || radio_multi){

    var width = document.body.clientWidth;
    document.getElementById("viewlet-survey").style.marginLeft = "250px";
    document.getElementById("viewlet-survey").style.width = "350px";
  }
}
