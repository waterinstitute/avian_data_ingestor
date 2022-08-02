---
title: "Browse"
date: 2022-07-14T01:13:45-05:00
draft: false
layout: staticpage
---
{{< rawhtml >}}
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jquery.filebrowser@0.8.4/css/jquery.filebrowser.min.css">

  <link href="https://code.jquery.com/ui/1.12.1/themes/dark-hive/jquery-ui.css" rel="stylesheet"/>
  <style>

    .content {
      margin-top: 50px;
    }
    .disabled {
        color: currentColor;
        cursor: not-allowed;
        opacity: 0.5;
        text-decoration: none;
    }
  </style>
<div class="content">
    <div id="browser" class="container">
    </div>
  </div>

  <!-- jQuery -->
	<script src="//code.jquery.com/jquery-3.5.1.min.js"></script>
	<script src="//code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/jquery.filebrowser@0.8.4/js/jquery.filebrowser.min.js"></script>

  <!-- Tether -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>

  <!-- Bootstrap 4 -->
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
  <script type="application/javascript">
  init_browser = function(data) {
    console.log(data)
    var browse = $('#browser').browse({
        root: '/',
        separator: '/',
        contextmenu: true,
        dir: function(path) {
            return new Promise(function(resolve, reject) {
			     console.log(path)
                 if (path == '/') {
                     resolve(data[""]);
                 } else if (path in data) {
                     resolve(data[path]);
                 } else {
                     reject(); // for cases when you type wrong path in address bar
                 }
             });
        },
        open: function(filename) {
            window.open(filename)
        }
    });
}
  $.get("/file_listing.json", null,init_browser);
  </script>


{{< /rawhtml >}}
