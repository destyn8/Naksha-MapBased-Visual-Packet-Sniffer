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
		console.log("message recvd[server]");
		sockio.emit('newPacket',data);
	});
	socket.on('disconnect',()=>{
		console.log('user disconnected');
	});
});
server.listen(5000,()=>{
	console.log('listening on port 5000');
});