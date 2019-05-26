<?php
  try {
    $curl = new Curl('api:5000/sensors');

    $sensors = json_decode($curl->get());

    if ($sensors === NULL) {
      $error = 'Şu an bağlantı sağlanamıyor. Lütfen daha sonra tekrar deneyiniz.';
    }
  
  } catch (\Exception $e) {
    die('Şu an bağlantı sağlanamıyor. Lütfen daha sonra tekrar deneyiniz.');
  }

?>

<?php require __DIR__ . '/header.php'; ?>

<!-- page content -->
<div class="right_col" role="main">
  <div class="row">
    <div id="test">

    </div>
  </div>
  <div class="row">
    <?php if(isset($error)): ?>
      <div class="col-md-12">
        <div class="alert alert-danger text-center" role="alert">
          <h4 style="margin-top: 10px;"><?php echo $error ?></h4>
        </div>
      </div>
    <?php else: ?>
      <?php foreach($sensors as $sensor): ?>
        <div class="col-md-6">
          <div class="panel panel-default">
            <div class="panel-heading title">
              <h3 class="panel-title"><?php echo $sensor->name ?></h3>
              <span><?php echo date('m/d/Y H:i:s', strtotime($sensor->last_connection_datetime)) ?></span>
            </div>
            <div class="panel-body">
              <span id="<?php echo 'sensor' . $sensor->sensor_id ?>">1</span>
            </div>
            <div class="panel-footer">
              <?php echo $sensor->description ?>
            </div>
          </div>
        </div>
      <?php endforeach ?>
    <?php endif ?>
  </div>
</div>
<!-- /page content -->

<?php require __DIR__ . '/footer.php'; ?>