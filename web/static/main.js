window.onload = function () {

    console.log('test')

    try{
        var sock = new WebSocket('ws://' + window.location.host + '/ws');
    }
    catch(err){
        var sock = new WebSocket('wss://' + window.location.host + '/ws');
    }

    sock.onopen = function(){
        sock.send("connect");
    }

    function showMessage(message) {
        var messageElem = document.getElementById('value');
        messageElem.textContent = message
    }

    // income message handler
    sock.onmessage = function(event) {
      showMessage(event.data);
    };

}
