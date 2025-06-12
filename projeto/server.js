const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const upload = multer();
const PORT = 80;
const HOST = '0.0.0.0'; // IP fixo da rede local

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Arquivos estáticos
app.use(express.static(path.join(__dirname, 'public')));
app.use('/assets', express.static(path.join(__dirname, 'assets')));

// Página inicial
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Rota de geração de assinatura
app.post('/signaturegenerator', upload.none(), (req, res) => {
  const { signName, signSector, signEmail, signPhone } = req.body;

  const pythonPath = path.join(__dirname, 'signaturegenerator.py');

  const pythonProcess = spawn('python', [
    pythonPath,
    signName,
    signSector,
    signEmail,
    signPhone,
  ]);

  let imageBuffer = Buffer.alloc(0);

  pythonProcess.stdout.on('data', (data) => {
    imageBuffer = Buffer.concat([imageBuffer, data]);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error('Erro do Python:', data.toString());
  });

  pythonProcess.on('error', (err) => {
    console.error('Erro ao executar o script Python:', err);
    return res.status(500).send('Erro interno ao gerar assinatura.');
  });

  pythonProcess.on('close', (code) => {
    if (code === 0) {
      res.setHeader('Content-Disposition', 'attachment; filename="signature.png"');
      res.setHeader('Content-Type', 'image/png');
      res.send(imageBuffer);
    } else {
      res.status(500).send('Erro ao gerar imagem da assinatura.');
    }
  });
});

// Inicializa servidor escutando no IP fixo da rede local
app.listen(PORT, HOST, () => {
  console.log(`Servidor rodando em http://${HOST}:${PORT}`);
});
