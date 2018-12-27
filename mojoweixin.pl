 #!/usr/bin/env perl
 use Mojo::Weixin;
 my ($host,$port,$post_api);
 
 $host = "0.0.0.0";
 $port = 3000;
 $post_api = '127.0.0.1:6088';
 
 my $client = Mojo::Weixin->new("send_interval" => 0.5, log_level=>"info",http_debug=>0);
 $client->load("ShowMsg");
 $client->load("Openwx",data=>{listen=>[{host=>$host,port=>$port}], post_api=>$post_api, post_media_data => 0, post_event_list =>[]});
 $client->run();
