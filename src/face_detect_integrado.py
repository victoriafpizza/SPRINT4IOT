# src/face_detect_integrado.py
# Reconhecimento facial local (OpenCV + Haar) com integração mínima:
# - Ao detectar um rosto, registra presença em logs/presenca.txt (com debounce).
# - Parâmetros ajustáveis por trackbars: scaleFactor, minNeighbors, minSize.
# - Overlay com status e parâmetros na tela.

import os
import time
from datetime import datetime
import cv2

# --- Caminhos base ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

CASCADE_PATH = os.path.join(ASSETS_DIR, 'haarcascade_frontalface_default.xml')
LOG_PATH = os.path.join(LOGS_DIR, 'presenca.txt')
OUTPUT_VIDEO_PATH = os.path.join(BASE_DIR, 'saida_anotada.mp4')  # opcional

# --- Carrega o Haar Cascade ---
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
if face_cascade.empty():
    print("Erro: não foi possível carregar 'haarcascade_frontalface_default.xml' em assets/.")
    raise SystemExit

# --- Abre webcam (tenta múltiplos backends/índices) ---
def open_camera():
    candidates = [
        (0, cv2.CAP_DSHOW), (1, cv2.CAP_DSHOW), (2, cv2.CAP_DSHOW),
        (0, cv2.CAP_MSMF),  (1, cv2.CAP_MSMF),  (2, cv2.CAP_MSMF),
        (0, cv2.CAP_ANY),   (1, cv2.CAP_ANY),   (2, cv2.CAP_ANY),
    ]
    for idx, backend in candidates:
        cap = cv2.VideoCapture(idx, backend)
        if cap.isOpened():
            # resolução sugerida (opcional)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            time.sleep(0.2)
            if cap.isOpened():
                return cap
        cap.release()
    return None

cap = open_camera()
if cap is None or not cap.isOpened():
    print("Erro: não foi possível abrir a webcam. Feche outros aplicativos e verifique permissões.")
    raise SystemExit

# --- Janela e trackbars (parâmetros ajustáveis) ---
cv2.namedWindow('Reconhecimento Facial')

def _noop(x): pass

cv2.createTrackbar('scale x100',   'Reconhecimento Facial', 110, 200, _noop)  # 1.10–2.00
cv2.createTrackbar('minNeighbors', 'Reconhecimento Facial',   5,  20, _noop)  # 1–20
cv2.createTrackbar('minSize',      'Reconhecimento Facial',  40, 300, _noop)  # 20–300 px

# --- Writer de vídeo (opcional) ---
w  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  or 1280
h  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 720
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, fps, (w, h))

# --- Integração mínima: registrar presença em arquivo ---
def registrar_presenca(evento: str = "Rosto detectado"):
    ts = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"{ts} - {evento}\n")
    # também mostra no console para evidência
    print(f"[LOG] {ts} - {evento}")

# Debounce para não registrar a cada frame
ULTIMO_EVENTO = 0.0
DEBOUNCE_SEGUNDOS = 2.0

prev_t = time.time()
while True:
    ok, frame = cap.read()
    if not ok:
        print("Aviso: frame não lido da webcam. Encerrando.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Lê parâmetros
    sf = max(1.01, cv2.getTrackbarPos('scale x100', 'Reconhecimento Facial') / 100.0)
    mn = max(1,    cv2.getTrackbarPos('minNeighbors', 'Reconhecimento Facial'))
    ms = max(20,   cv2.getTrackbarPos('minSize', 'Reconhecimento Facial'))

    # Detecção
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=sf, minNeighbors=mn, minSize=(ms, ms)
    )

    # Se detectou ao menos um rosto, registra evento (com debounce)
    if len(faces) > 0:
        agora = time.time()
        if agora - ULTIMO_EVENTO >= DEBOUNCE_SEGUNDOS:
            registrar_presenca("Rosto detectado → ação do sistema principal (registro de presença)")
            ULTIMO_EVENTO = agora
        cv2.putText(frame, "Acesso Liberado", (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)

    # Desenha retângulos/labels
    for (x, y, ww, hh) in faces:
        cv2.rectangle(frame, (x, y), (x + ww, y + hh), (0, 0, 255), 2)
        cv2.putText(frame, "Rosto Detectado", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    # FPS estimado + parâmetros no overlay
    now = time.time()
    fps_est = 1.0 / max(1e-6, (now - prev_t))
    prev_t = now

    cv2.putText(
        frame,
        f'scale={sf:.2f}  neighbors={mn}  minSize={ms}px  FPS={fps_est:.1f}',
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA
    )

    cv2.imshow('Reconhecimento Facial', frame)
    out.write(frame)

    # Tecla 'q' encerra
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Finalização ---
cap.release()
out.release()
cv2.destroyAllWindows()
print(f"Saída de vídeo anotado: {OUTPUT_VIDEO_PATH}")
print(f"Logs de presença: {LOG_PATH}")
