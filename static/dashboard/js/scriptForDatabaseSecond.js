var ros = new ROSLIB.Ros();
 
// rosbridge websocket server와의 연결을 생성합니다.
ros.connect('ws://0.0.0.0:9090');

  ros.on('connection', function() {
    console.log('Connected to websocket server.');
    document.getElementById('header').style.backgroundColor = "#07a666";
  });

  ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
  });

  ros.on('close', function() {
    console.log('Connection to websocket server closed.');
  });

  var listener = new ROSLIB.Topic({
    ros : ros,
    name : '/test/topic',
    messageType : 'std_msgs/Int16'
  });


/* if not using ajax, then use below code.
function createForm(url,method,name1,value1,name2,value2){
    let form = document.createElement('form');
    form.action = url;
    form.method = method;
    form.innerHTML = '<input name='+name1+' value='+value1+'>  <input name='+name2+' value='+value2+'>';
    //form.innerHTML = '<input name=' + name + '>'
    //form.innerHTML = '<input value=' + value + '>';
    //form.innerHTML = '<input name="q" value="5">';
    document.body.append(form);
    form.submit();
    console.log(form.action);
    console.log(form.method);
}
*/

var position = [];
position[0]=1;
i=1;
dataSender = document.getElementById('sendData');

listener.subscribe(function(message) {
    console.log('Received message on ' + listener.name + ': ' + message.data);
    //listener.unsubscribe(); // unsubcribe topic node.
    return_data = message.data;
    /*if not using ajax, then use below code.
    createForm("updateDatabase",'GET','x',data,'y',data);
    */
    setTimeout(request_ajax(return_data, return_data),100);
  });


function request_ajax(return_data_x, return_data_y){
    $.ajax({
        url: '/dashboard/updateDatabase/',
        type: "POST",
        dataType: "JSON",
        data: {'x': return_data_x,'y' : return_data_y},
        success: function(data){
            console.log(data);
        },beforeSend:function(){
            console.log("i am waiting");
        },complete:function(){
            console.log("i am done");
        },error: function (request, status, error) {
            console.log('i am failed');
        }
            });
}