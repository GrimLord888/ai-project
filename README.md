# AI-Powered Emergency Response Assistant (Floki)

An intelligent, software-driven healthcare assistant prototype engineered for real-time biometric monitoring, emotional grounding interventions, and automated emergency escalations for elderly care. Developed under the Engineering Technology Innovation Project (ENG40011) framework.

The system tracks physiological telemetry (heart rate) and coordinates an immediate voice-driven safety gate if anomalies ($>100\text{ BPM}$) occur. If the user becomes unresponsive during a critical 5-second window, the system bypasses local feedback to trigger remote emergency communication protocols.

---

## 🚀 Engineering & Architectural Highlights
* **Deterministic Emergency Pathing:** Employs a strict 5-second asynchronous timeout gate. If a critical physiological anomaly is flagged ($>100\text{ BPM}$) and a verbal confirmation is not registered within the window, the software instantly triggers emergency dispatch routes.
* **Multimodal Speech Processing Pipeline:** Chais OpenAI's Whisper (via Python `speech_recognition`) for high-precision, multilingual Acoustic Model decoding alongside Google Text-to-Speech (gTTS) for low-latency synthesis.
* **Asynchronous Multi-Threading:** Isolates heavy input/output tasks—such as ambient therapeutic audio playback (`playsound`) and remote web requests (`twilio.rest`) —onto independent threads to keep the main biometric observation loops non-blocking.
* **Empathetic Context Alignment:** Custom text parsing arrays evaluate incoming sentiment tokens (`positive_emotion_list` / `negative_emotion_list`) to decide whether to pivot into automated stress mitigation protocols (e.g., box breathing coaching) or general conversational tasks.

---

## 🛠️ Tech Stack & Key Architectures
* **Core Runtime:** Python 3.x 
* **Large Language Model Engine:** Google Gemini API (`gemini-pro`) running custom context boundaries for responsive, low-latency dialogue generation.
* **Automatic Speech Recognition (ASR):** OpenAI Whisper (Medium Model Architecture) for highly precise multilingual transcription.
* **Biometric Telemetry / Alert Gateways:** Twilio REST Communications API for automated SMS notification routing.
* **Audio Synthesis & Core Libraries:** Google Text-to-Speech (`gTTS`), `playsound`, Python Standard `threading`

---

## 📐 Flow Control Architecture

1. **Continuous Telemetry Loop:** `assistant_v3.py` monitors physiological input.
2. **Anomaly Detection Gate:** If heart rate spikes $\ge 100\text{ BPM}$, an asynchronous prompt query (`ask_are_you_okay`) is generated.
3. **Sentiment & Timeout Evaluation:** 
   * **Vocal Response Detected:** Parser maps keywords to target routines (e.g., box-breathing scripts, therapeutic music) or invokes the Gemini core.
   * **Silence / Exception Timeout:** If zero vocal data is verified within a 5-second frame, a `sr.WaitTimeoutError` is intercepted, executing an immediate alert dispatch via Twilio webhooks.

[Biometric Input Generator] ──(Continuous Telemetry)──> [Telemetry Analyzer Loop]
│
(If Spike Detected: >100 BPM)
│
▼
[Twilio SMS Gateway] <──(No Response: 5s Timeout)── [User Response Monitor Gate]
│
(Verbal Audio Captured)
│
▼
[gTTS Engine Output] <──(Context Generation)── [Gemini Pro LLM Processing]

---

## 📂 System Implementation

### 1. Asynchronous Telemetry Monitoring (`assistant_v3.py`)
`assistant_v3.py` serves as the primary system core, hosting the asynchronous event execution loop. It evaluates incoming simulated biometric feeds mirroring senior cardiac activity.
* **Anomaly State Activation:** Once a heartbeat breaches $100\text{ BPM}$, the program pauses lower-priority scripts to call a dedicated verification routine (`ask_are_you_okay`).
* **Fail-Safe Alert Processing:** If a `sr.WaitTimeoutError` exception throws due to vocal silence or physical immobility during critical prompts, a direct webhook POST triggers via Twilio client instances to pass real-time metrics ($BPM$) to designated caretakers.

### 2. General Assistant Modules (`assistant_v2.py`)
When heart rate telemetry settles inside safe parameters ($50 - 99\text{ BPM}$), the program falls back onto standard assistant modes. This layer runs the continuous audio interface:
* Conversational prompts are wrapped dynamically with descriptive boundaries (`"Answer this question briefly: "`) before firing to the Gemini LLM matrix to ensure low-latency token replies suitable for fluid, real-time interactions.

---

## 🔬 Experimental Results & Failure Analysis

* **Calming Interventions:** The system safely tracked simulated fluctuations ranging between $50 - 150\text{ BPM}$ across 60-minute trial periods. Conversational grounding successfully engaged during 95% of identified non-emergency spikes.
* **Alert Precision:** During intentionally triggered unresponsive test iterations, the automated Twilio message delivery gateway registered a **100% notification success rate**, dispatching details to target contacts with a mean network latency of 7.0 seconds.
* **Edge Case Engineering Goals:** Future updates look to transition static threshold checks ($>100\text{ BPM}$) into dynamic, individual baseline arrays. This step aims to cut down on false alarms caused by natural, brief heart rate variability.

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

## 👥 Contributor
* **Albert Lau** - Core Software Architecture & API Integration Engineer
