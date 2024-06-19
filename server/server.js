const express = require('express')
const http = require('http')
const socketIo = require('socket.io')
const app = express()
const server = http.createServer(app)
const sockio = socketIo(server)
console.log(__dirname)
app.get('/',(req,res)=>{
	res.sendFile(__dirname+'/dynamicMap.html');
});
sockio.on('connection',(socket)=>{
	console.log('connection recvd');
	socket.on('newPacket',(data)=>{
		console.log("Message recvd[server]");
		sockio.emit('newPacket',data);
	});
	socket.on('packetLen',(data)=>{
		console.log("Length recvd[server]");
		sockio.emit('packetLen',data);
	});
	socket.on('packetProt',(data)=>{
		console.log("Protocol recvd[server]");
		sockio.emit('packetProt',data);
	});
	socket.on('packetTTL',(data)=>{
		console.log("TTL recvd[server]");
		sockio.emit('packetTTL',data);
	});
    socket.on('interProt',function(data){
        console.log("IP recvd[server]");
		sockio.emit('interProt',data);
    });
    socket.once('packetHome',(data)=>{
        console.log("origin recvd[server]");
		sockio.emit('packetHome',data);    	
    });
	socket.on('disconnect',()=>{
		console.log('user disconnected');
	});
});
server.listen(5000,()=>{
	console.log('listening on port 5000');
});