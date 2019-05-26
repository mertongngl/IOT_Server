<?php

session_start();
ob_start();

function loadClasses($className) {
    require __DIR__ . '/classes/' . strtolower($className) . '.php';
}

spl_autoload_register('loadClasses');

$config = require __DIR__ . '/config.php';

foreach (glob(__DIR__ . '/helper/*.php') as $helperFile) {
    require $helperFile;
}