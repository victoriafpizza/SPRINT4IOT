# 👁️ Sistema de Reconhecimento Facial com Registro de Presença (OpenCV + Haar Cascade)

<p align="center">
📸 Projeto acadêmico que utiliza visão computacional para detectar rostos em tempo real e registrar presenças automaticamente.
</p>

---

## 👥 Desenvolvedores
- **Victoria Franceschini Pizza** – RM 550609  
- **Eric de Carvalho Rodrigues** – RM 550249  

---

<p align="center">
<img src="https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white" /> 
<img src="https://img.shields.io/badge/-OpenCV-5C3EE8?logo=opencv&logoColor=white" /> 
</p>

---

## 🧠 Sobre o Projeto
Este projeto implementa um **sistema de reconhecimento facial local**, capaz de **detectar rostos em tempo real via webcam** e **registrar automaticamente os eventos de presença** em um arquivo de log.

A solução foi desenvolvida em **Python** utilizando a biblioteca **OpenCV** e o classificador **Haar Cascade**, funcionando **offline** e com **ajuste dinâmico de parâmetros** em tempo real (através de *trackbars* na interface).

---

## 🚀 Tecnologias Utilizadas
- 🐍 **Python 3.10+**
- 🎥 **OpenCV**
- 🧩 **Haar Cascade Classifier**
- 📂 **Sistema de Log (Arquivo .txt)**

---

## 🔍 Como Funciona
1. O programa abre a webcam e inicia a detecção facial localmente.  
2. Quando um rosto é identificado, ele:
   - Desenha um **retângulo vermelho** ao redor da face.
   - Exibe o texto **“Acesso Liberado”** na tela.
   - Registra a data e hora no arquivo `logs/presenca.txt`.
3. Os parâmetros podem ser ajustados ao vivo:
   - `scaleFactor` – sensibilidade da escala.  
   - `minNeighbors` – número mínimo de vizinhos.  
   - `minSize` – tamanho mínimo de detecção.  
4. A tecla `q` encerra o programa e salva o vídeo anotado em `saida_anotada.mp4`.

---

## 🎯 Funcionalidades
- ✅ Detecção facial **em tempo real (webcam)**.  
- ✅ **Registro automático de presença** em `logs/presenca.txt`.  
- ✅ **Trackbars** para ajuste dinâmico dos parâmetros.  
- ✅ Exibição em tela com FPS e status de detecção.  
- ✅ Gravação de vídeo com anotações (`saida_anotada.mp4`).  
- ✅ Integração mínima simulada — “rosto detectado → evento registrado”.

---

## ⚙️ Como Rodar o Projeto

### 1️⃣ Clone este repositório
```bash
git clone https://github.com/victoriafpizza/GSPhysicalComputing.git
cd GSPhysicalComputing
```
### 2️⃣ Instale as dependências
pip install opencv-python

### 3️⃣ Baixe o classificador Haar Cascade

Certifique-se de ter o arquivo:
👉 haarcascade_frontalface_default.xml

Ele pode ser baixado do repositório oficial do OpenCV:
Download XML

### 4️⃣ Execute o programa
python detector_face.py

---

## ⚖️ Nota Ética sobre Reconhecimento Facial

Este projeto foi desenvolvido exclusivamente para fins acadêmicos.
Nenhuma imagem, vídeo ou dado facial é armazenado, compartilhado ou utilizado para 
identificação pessoal.
O uso ético de tecnologias de visão computacional é essencial para garantir 
privacidade, segurança e respeito aos direitos individuais.

## 🌱 Possíveis Extensões Futuras

🔌 Integração com dispositivos IoT — ex.: acender um LED via ESP32 quando um rosto for detectado.

🧠 Reconhecimento de identidade — usar redes neurais para identificar usuários específicos.

☁️ Integração com APIs externas — enviar logs para um servidor ou banco de dados em nuvem.

📱 Interface mobile ou web — para exibir em tempo real quem foi detectado.
