 #!/usr/bin/env perl
 use Mojo::Webqq;
 my ($host,$port,$post_api);
 
 $host = "0.0.0.0";
 $port = 5000;
 $post_api = '127.0.0.1:6088';
 
 my $client = Mojo::Webqq->new("send_interval" => 0.5, "is_update_group" => 0, "is_update_group_member" => 0, "is_update_friend" => 0, "is_update_discuss" => 0);
 $client->load("ShowMsg");
 $client->load("Openqq",data=>{listen=>[{host=>$host,port=>$port}], post_api=>$post_api, post_event =>1, post_stdout => 0,post_event_list => []});
 $client->run();
