  if (Storage !== undefined) {
    $(document).ready(function () {
      "use strict";

      /** Show consent information when it already activated by admin **/
      var enabled = $("#viewlet-consent").attr("data-enabled");
      if (enabled !== "true") {
        return;
      }
      
      /** public variable declaration **/
      var status = localStorage.getItem("cns-status");
      var user = $("#attrs").attr("user");
      var d = new Date();
      var expireYear = new Date(d.getFullYear() + 1, d.getMonth(), d.getDate());
      
      /** presenting project information based on participation status and action date **/
      /** dissagree user will get offer after 10 days, agree user will renew after 365 days **/
      if (status === null) {
        $("#viewlet-consent").show();
        $("#pis-icf-consent").hide();
      } else {
        var currDate_ms = (new Date()).getTime();
        var prevDate_ms = (new Date(localStorage.getItem("cns-status-date"))).getTime();
        var diffDate_ms = currDate_ms - prevDate_ms;
        var diffLimit_ms = 1000*60*60*24*10; //10 days limit
        if (status === "activated") {
          diffLimit_ms = 1000*60*60*24*365; //365 days limit
        }
        if (diffDate_ms > diffLimit_ms){
          $("#viewlet-consent").show();
          $("#pis-icf-consent").hide();
        }
      }

      /** Clicking "More Info" button, than loading PIS and ICF forms **/
      $("button[name='nap.consent.bt.info']").click(function (event) {
        event.preventDefault();
        $("#intro-consent").hide();
        var abi_logo = $("#attrs").attr("src");
        var url = $("#pis-consent").attr("url");
        $.get( url, function( data ) {
            data = data.replace("ABI-logo.png",abi_logo);
            $("#pis-consent").html(data);  
        });
        url = $("#icf-consent").attr("url");
        $.get( url, function( data ) {
            data = data.replace("ABI-logo.png",abi_logo);
            $("#icf-consent").html(data);
        });
        $("#pis-icf-consent").show();
      });
      
      /** Disagree to participate into the project **/
      $("button[name='nap.consent.bt.disagree']").click(function (event) {
        event.preventDefault();
        localStorage.setItem("cns-status", "deactivated");
        localStorage.setItem("cns-status-date", new Date());
        document.cookie = "_user=; path=/";
        $("#viewlet-consent").hide();
      });
      
      /** Agree to participate into the project **/
      $("button[name='nap.consent.bt.agree']").click(function (event) {
        event.preventDefault();
        localStorage.setItem("cns-status", "activated");
        localStorage.setItem("cns-status-date", new Date());
        $("#viewlet-consent").hide();
        if (user.length === 0){
          document.cookie = "_user=undefined; expires="+expireYear+"; path=/";
        } else {
          document.cookie = "_user="+user+"; expires="+expireYear+"; path=/";
        }
      });
      
      /** Update login status for activated user **/
      var prevUser = getCookie("_user");
      if (status === "activated" && user.length > 0 && prevUser !== user){
        document.cookie = "_user="+user+"; expires="+expireYear+"; path=/";
      }
    });
  }
  
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