function message(status, shake=false, id="") {
  if (shake) {
    $("#"+id).effect("shake", {direction: "right", times: 2, distance: 8}, 250);
  } 
  document.getElementById("feedback").innerHTML = status;
  $("#feedback").show().delay(2000).fadeOut();
}

function error(type) {
  $("."+type).css("border-color", "#E14448");
}

var login = function() {
  $.post({
    type: "POST",
    url: "/",
    data: {"username": $("#login-user").val(), 
           "password": $("#login-pass").val()},
    success(response){
      var status = JSON.parse(response)["status"];
      if (status === "Login successful") { location.reload(); }
      else { error("login-input"); }
    }
  });
};

$(document).ready(function() {
  
  $(document).on("click", "#login-button", login);
  $(document).keypress(function(e) {if(e.which === 13) {login();}});
 
  $("#url-button").click(function(){
    $.post({
        type: "POST",
        url: "/input_url",
        data: {"inputurl": $("#input-url").val()},
        success(response) {
          var links = JSON.parse(response)["links"];
            var h = document.getElementById("scrapResults");
            if(typeof(links) == 'object'){
              console.log(links.length);
              for (idx=0; idx<links.length; idx++){
                if(links!=null) {
                  counter++;
                  h.appendchild("afterend", "<div class='row'><div class='cell' data-title='ID' > "+ counter +"</div><div class='cell' data-title='Original Links' > "+ $("#input-url").val() +"</div><div class='cell' data-title='Page Title' >"+ links[idx][0] +"</div><div class='cell' data-title='Crawled Links' >"+ links[idx][1] +"</div> </div>"); 
                  // console.log(typeof(link), '------------', links[0][0]);
                  //do something with value;
                }
              }
            }
        }
      });
  });
  
  $("#scrap_btn").click(function(){
    var rows = document.getElementsByClassName("url-cell");
    var linknames = document.getElementsByClassName("pagetitle-cell");
    len = rows.length;
    const scrapasync = (url, linkname) => {
      return new Promise(resolve => {
        $.post({
          type: "POST",
          url: "/startscrape",
          data: {"scrapurl": url},
          success(response) {
            // console.log(JSON.parse(response)["title"])
            var data = JSON.parse(response)["title"];
            var h = document.getElementById("scrape-result-table");
            // if(typeof(data) == 'object'){
              // console.log(links.length);
              // for (idx=0; idx<links.length; idx++){
                if(data != null) {
                  counter ++;
                  h.insertAdjacentHTML("afterbegin", "<div class='row'><div class='cell' data-title='ID' > "+ counter +"</div><div class='cell' data-title='Scraped Link' > "+ url +"</div><div class='cell' data-title='Page Title' >"+ linkname +"</div><div class='cell' data-title='Head Line' >"+ data+"</div> </div>"); 
                }
              // }
            // }
            if (data === "Signup successful") { alert('success') }
          } 
        });
      })
    }
    for(i = 0; i< len; i++){
      const scrapawait = async () => {
        await scrapasync(rows[i].innerText, linknames[i].innerText);
        // 
      }
      scrapawait();
    }
    // for(var idx = 0; idx < urls.length; idx ++){
    //   const scrapawait = async () => {
    //     await scrapasync(rows[i].innerText);
    //   }
    //   scrapawait();
    // }
    // $.get("/startscrape", function(status){
    //   console.log(rst, status);
    // });
    // console.log('asdfa',rst);
  });
  var counter = 0;
  $('#upload-file-btn').click(function() {
    var file = document.getElementById('upload').files[0];
    var reader = new FileReader();
    const crawlasync = (url) => {
      return new Promise(resolve => {
        $.post({
          type: "POST",
          url: "/input_url",
          data: {"inputurl": url},
          success(response) {
            var links = JSON.parse(response)["links"];
            var h = document.getElementById("scrapResults");
            if(typeof(links) == 'object'){
              console.log(links.length);
              for (idx=0; idx<links.length; idx++){
                if(links!=null) {
                  counter ++;
                  h.insertAdjacentHTML("afterbegin", "<div class='row'><div class='cell' data-title='ID' > "+ counter +"</div><div class='cell' data-title='Original Links' > "+ url +"</div><div class='cell' data-title='Page Title' >"+ links[idx][0] +"</div><div class='cell' data-title='Crawled Links' >"+ links[idx][1] +"</div> </div>"); 
                }
              }
            }
            if (links === "Signup successful") { alert('success') }
          }
        });
      })
    }
    reader.onload = function(progressEvent){
      var urls = this.result.split('\n');
      for(var idx = 0; idx < urls.length; idx ++){
        const sendurl = async () => {
          await crawlasync(urls[idx]);
        }
        sendurl();
      }
    };
    reader.readAsText(file);
    
  });
  $(document).on("click", "#signup-button", function() {
    $.post({
      type: "POST",
      url: "/signup",
      data: {"username": $("#signup-user").val(), 
             "password": $("#signup-pass").val(), 
             "email": $("#signup-mail").val()},
      success(response) {
        var status = JSON.parse(response)["status"];
        if (status === "Signup successful") { location.reload(); }
        else { message(status, true, "signup-box"); }
      }
    });
  });

  $(document).on("click", "#save", function() {
    $.post({
      type: "POST",
      url: "/settings",
      data: {"username": $("#settings-user").val(), 
             "password": $("#settings-pass").val(), 
             "email": $("#settings-mail").val()},
      success(response){
        message(JSON.parse(response)["status"]);
      }
    });
  });
});

// Open or Close mobile & tablet menu
// https://github.com/jgthms/bulma/issues/856
$("#navbar-burger-id").click(function () {
  if($("#navbar-burger-id").hasClass("is-active")){
    $("#navbar-burger-id").removeClass("is-active");
    $("#navbar-menu-id").removeClass("is-active");
  }else {
    $("#navbar-burger-id").addClass("is-active");
    $("#navbar-menu-id").addClass("is-active");
  }
});