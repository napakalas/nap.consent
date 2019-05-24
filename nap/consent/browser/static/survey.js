$(document).ready(function () {
    "use strict";
    var d = new Date();
    d.setMonth(d.getMonth() + 3);
    var expMonth = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    
    var isAgree = $("#viewlet-survey").attr("isAgree");
    var enabled = $("#viewlet-consent").attr("data-enabled");
    var isQstAvailable = $("#viewlet-survey").attr("isQstAvailable");
    if(isAgree === "true" && enabled === "true" && isQstAvailable === "true" && getCookie("_q_answer") === "\"\""){
      $("#viewlet-survey").show();
    }
    else {
      return;
    }
    
    $("button[name='nap.consent.bt.submit']").click(function (event) {
        //setting answer cookie
        var radios = document.getElementsByName('radioLikert');
        var text = document.getElementById('text-answer');
        var answer = "";
        if (radios){
            for (var i = 0, length = radios.length; i < length; i++){
                if (radios[i].checked){
                    answer = radios[i].value;
                    break;
                }
            }
        }
        if (text){
            answer = text.value;
        } 
        if (answer !== ""){
            document.cookie = "_q_answer="+answer+"; expires="+expMonth+"; path=/";
            $("#viewlet-survey").hide();
        }
    });
  });
  
  $(window).bind("pageshow", function(event) {
    var d = new Date();
    d.setMonth(d.getMonth() + 3);
    var expMonth = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    
    /** DETECT AND RECORD FORWARD AND BACKWARD NAVIGATION **/
    var prev_reff = localStorage.getItem("cns-reff-url");
    var _nav = getCookie("_nav");
    if(_nav === "\"0\""){
        _nav = "3";
    } else if (prev_reff === document.URL){
        _nav += "1";
    } else {
        _nav += "2";
    }
    localStorage.setItem("cns-reff-url", document.referrer);
    document.cookie = "_nav=" + _nav+"; expires="+expMonth+"; path=/";
    document.cookie = "_time=" + (new Date()).getTime() +"; expires="+expMonth+"; path=/";
    /** END OF BLOCK **/
    
  });
  
  function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for(var i = 0; i <ca.length; i++) {
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