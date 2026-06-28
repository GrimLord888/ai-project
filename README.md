Markdown
# AI-Powered Emergency Response Assistant (Floki)

An intelligent, software-driven healthcare assistant prototype engineered for real-time biometric monitoring, emotional grounding interventions, and automated emergency escalations for elderly care. Developed under the Engineering Technology Innovation Project (ENG40011) framework.

The system tracks physiological telemetry (heart rate) and coordinates an immediate voice-driven safety gate if anomalies ($>100\text{ BPM}$) occur. If the user becomes unresponsive during a critical 5-second window, the system bypasses local feedback to trigger remote emergency communication protocols.

---

## 🛠️ Tech Stack & Key Architectures
* **Automatic Speech Recognition (ASR):** OpenAI Whisper (Medium Model) for highly precise multilingual transcription.
* **Natural Language Processing (NLP):** Google Gemini API (`gemini-pro`) running custom context boundaries for responsive, low-latency dialogue generation.
* **Telecommunication Gateway:** Twilio REST API for automated SMS notification routing.
* **Asynchronous Multi-Threading:** Isolates heavy input/output audio playback (`playsound`) and remote network requests from the primary telemetry scanning engine to maintain non-blocking execution.

---

## 📐 Flow Control Architecture

1. **Continuous Telemetry Loop:** `assistant_v3.py` monitors physiological input.
2. **Anomaly Detection Gate:** If heart rate spikes $\ge 100\text{ BPM}$, an asynchronous prompt query (`ask_are_you_okay`) is generated[cite: 4].
3. **Sentiment & Timeout Evaluation:** 
   * **Vocal Response Detected:** Parser maps keywords to target routines (e.g., box-breathing scripts, therapeutic music) or invokes the Gemini core[cite: 4].
   * **Silence / Exception Timeout:** If zero vocal data is verified within a 5-second frame, a `sr.WaitTimeoutError` is intercepted, executing an immediate alert dispatch via Twilio webhooks[cite: 4].

---

## 🚀 Installation & Execution

### Prerequisites
Ensure your environment contains the required audio and system dependencies before running the application:
pip install speech_recognition whisper google-generativeai gTTS playsound twilio pywhatkit pytube

### Running the System
Launch the primary event loop and telemetry supervisor module by executing the main script:

python3 assistant_v3.py

Note: assistant_v3.py dynamically acts as the primary orchestrator, importing core assistant and multimedia handling logic from assistant_v2.py as a module dependency

### Termination
To interrupt the background loops, safely stop the script and clean up system threads by sending a keyboard interrupt:

Ctrl + C

## 🔒 Security & Secret Management Note
This repository separates functional source logic from production credentials. Ensure your local deployment environments have target runtime variables configured before starting execution:

GEMINI_API_KEY

TWILIO_ACCOUNT_SID & TWILIO_AUTH_TOKEN

## 👥 Contributors (Swinburne Team)
* **Albert Lau** - Core Software Architecture & API Integration Engineer
