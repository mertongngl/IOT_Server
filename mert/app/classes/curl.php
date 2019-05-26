<?php

class Curl
{

  public $username;
  public $passwd;
  public $url;

  public function __construct($url)
  {
    $this->url = $url;
    $this->username = 'admin';
    $this->passwd = 'SuperSecretPwd';
    
  }

  public function post($query = [])
  {
    $response = $this->curlRequest('POST', $query);
  
    return $response;
  }

  public function get()
  {
    $response = $this->curlRequest('GET');

    return $response;
  }

  protected function curlRequest($method, $query = [])
  {
    $curl = curl_init();

    curl_setopt_array($curl, array(
      CURLOPT_URL => $this->url,
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_ENCODING => "",
      CURLOPT_MAXREDIRS => 10,
      CURLOPT_USERPWD => $this->username . ":" . $this->passwd,
      CURLOPT_TIMEOUT => 30,
      CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
      CURLOPT_CUSTOMREQUEST => $method,
      CURLOPT_POSTFIELDS => $query,
      CURLOPT_HTTPHEADER => array(
        "accept: application/json",
      ),
    ));

    $response = curl_exec($curl);
    $err = curl_error($curl);

    curl_close($curl);

    if ($err) {
      return $err;
    } else {
      return $response;
    }
  }
}
?>