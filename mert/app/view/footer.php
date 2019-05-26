<!-- footer content -->
<footer>
          <div class="pull-right">
            Gentelella - Bootstrap Admin Template by <a href="https://colorlib.com">Colorlib</a>
          </div>
          <div class="clearfix"></div>
        </footer>
        <!-- /footer content -->
      </div>
    </div>

    <!-- jQuery -->
    <script src="./app/public/vendors/jquery/dist/jquery.min.js"></script>
    <!-- Bootstrap -->
    <script src="./app/public/vendors/bootstrap/dist/js/bootstrap.min.js"></script>

    <!-- Custom Theme Scripts -->
    <script src="./app/public/build/js/custom.js"></script>

    <script>
      function fetchdata(){
        $.ajax({
            url: './app/classes/payload.php',
            type: 'get',
            success: function(response){
              $.each(JSON.parse(response), function (index, value) {
                $('#sensor' + value.sensor_id).empty().append(value.value);
              });
              
            }
          });
        }

        $(document).ready(function(){
          setInterval(fetchdata, 1000);  
        });
    </script>
  </body>
</html>