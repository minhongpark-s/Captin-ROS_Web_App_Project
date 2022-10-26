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


// sendForm example function.
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

var position = [];
position[0]=1;
i=1;
dataSender = document.getElementById('sendData');
createForm("updateDatabase/",'GET','x','10','y','10');

  listener.subscribe(function(message) {
    console.log('Received message on ' + listener.name + ': ' + message.data);
    //listener.unsubscribe(); // unsubcribe topic node.
    position[i]= message.data;

    ranNum=Math.random()*10 // 0~10

    ctx.beginPath(); // 새선 그리기 설정
    ctx.moveTo(position[i-1], position[i-1]); // 출발점 지정
    ctx.lineTo(position[i], position[i]); //도착점 지정
    ctx.stroke(); // 선 그리기
    i = i + 1;
  });