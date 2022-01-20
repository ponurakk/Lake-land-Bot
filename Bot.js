const { Client, Intents, version} = require('discord.js');
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });
require("dotenv").config();
const util = require('minecraft-server-util');

// komendy nie dziala :/
client.on('message', async message => {
    var prefix = '?';
    if (!message.content.startsWith(prefix)) return;
    const args = message.content.slice(prefix.length).trim().split(/ +/);
    const command = args.shift().toLowerCase()
    switch(command){
        case "ip":
            message.channel.send("IP Serwera: lake-land.pl")
            break;
        case "strona":
            message.channel.send("Strona internetowa: https://lake-land.pl")
            break;
        case "sklep":
            message.channel.send("Sklep: https://lake-land.pl/shop/Survival");
            break;
        case "fb":
            message.channel.send("Facebook: https://fb.lake-land.pl")
            break;
        case "dc":
            message.channel.send("Discord: https://dc.lake-land.pl")
            break;
    }
    if(message.content === "test") {
        let embed = new Discord.MessageEmbed()
        .setTitle("lake-land.pl")
        .setDescription("Aktualne IP: lake-land.pl")
        .setColor("RANDOM")
        .setFooter("chuj")
        message.channel.send({embed})
    }
})
// Status bota 
const options = { timeout: 1000*5, enableSRV: true }
setInterval(function (){
    util.status('lake-land.pl', 25565, options).then((response)=>{
        client.user.setActivity( `${response.players.online}/2022  Wbijaj na serwer!` , { type: 'PLAYING' });
    }).catch((error)=>{
        client.user.setActivity( `WebSocket Error!` , { type: 'PLAYING' });
        console.error(error)
    })
}, 5*1000)
client.on('ready', () => {
    console.log('Ready!');
});
(async () => {
    client.login(process.env.token);
})();