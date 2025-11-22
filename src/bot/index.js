import {
  makeWASocket,
  useMultiFileAuthState,
  DisconnectReason,
  fetchLatestBaileysVersion
} from "@whiskeysockets/baileys";
import { Boom } from "@hapi/boom";
import P from "pino";
import qrcode from "qrcode-terminal";
import { spawn } from "child_process";

const fetch = (...args) =>
  import("node-fetch").then(({ default: fetch }) => fetch(...args));

async function startBot() {
  const { state, saveCreds } = await useMultiFileAuthState("./auth");
  const { version } = await fetchLatestBaileysVersion();

  const sock = makeWASocket({
    version,
    logger: P({ level: "silent" }),
    printQRInTerminal: false,
    auth: state,
    browser: ["Bot Baileys", "Chrome", "1.0.0"]
  });

  // ==============================
  //    CONEXÃO E QR CODE
  // ==============================
  sock.ev.on("connection.update", (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.clear();
      console.log("📱 Escaneie o QR abaixo:");
      qrcode.generate(qr, { small: true });
    }

    if (connection === "close") {
      const reason = new Boom(lastDisconnect?.error)?.output?.statusCode;
      const shouldReconnect = reason !== DisconnectReason.loggedOut;
      console.log("⚠️ Conexão encerrada:", reason, "→ Reconnect:", shouldReconnect);
      if (shouldReconnect) startBot();
    } else if (connection === "open") {
      console.log("✅ Bot conectado com sucesso!");
    }
  });

  sock.ev.on("creds.update", saveCreds);

  // ==============================
  //   MENSAGENS RECEBIDAS
  // ==============================
  sock.ev.on("messages.upsert", async (msg) => {
    if (msg.type !== "notify") return; // teste ignorar duplicatas
    const m = msg.messages[0];
    if (!m.message || m.key.fromMe) return;

    const sender = m.key.remoteJid;
    const text =
      m.message.conversation ||
      m.message.extendedTextMessage?.text ||
      "";

    // JSON para criar a classe Sala
    // {
    //     "acao": "criar_sala",
    //     "sala": {
    //         "ano": String,
    //         "alunos": [
    //                  String
    //             ]
    //         "materia": String
    //     }
    // }

    // gets the command text and converts it to the right json 
    const input = { acao: "criar_sala", sala: text.trim() };
    const IPCInput = JSON.stringify(input);

    // ==============================
    //   COMUNICAÇÃO COM O PYTHON
    // ==============================
    try {
        // call the python script
        const resposta = new Promise ( (resolve, reject) => {
            const process = spawn( "python3", ["../agente/main.py"] ); 
            
            // Send JSON input via stdin
            process.stdin.write(IPCInput);
            process.stdin.end();
            
            process.stdout.on('data', (data) => {
                resolve(data.toString());
            });

            process.stderr.on('data', (data) => {
                reject(data.toString());
            });
        });

        let data;
        try {
            data = JSON.parse( await resposta );
        } catch (parseErr) {
            console.error("Resposta do Python não é um JSON válido!", parseErr);
            throw new Error("Resposta inválida do Python");
        }

        if (!data.resposta) {
            console.error("O campo 'resposta' não veio no JSON do Python!");
            throw new Error("Formato de resposta inválido");
        }

        // ==============================
            //    ENVIO DA RESPOSTA
        // ==============================
            await sock.sendMessage(sender, { text: data.resposta });
        console.log(`Resposta enviada ao usuário: ${data.resposta}`);
    } catch (err) {
      console.error(" Erro ao comunicar com Python ou enviar resposta:", err);
      try {
        await sock.sendMessage(sender, {
          text: "Erro ao processar sua mensagem, tente novamente."
        });
      } catch (sendErr) {
        console.error("Falha ao enviar mensagem de erro:", sendErr);
      }
    }
  });
}

startBot();
