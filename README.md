Markdown
# AI-Powered Emergency Response Assistant (Floki)

[cite_start]An intelligent, software-driven healthcare assistant prototype designed to mitigate medical emergencies and provide cognitive-emotional care for the elderly[cite: 15]. [cite_start]The system continuously processes simulated biometric data (heart rate telemetry) and executes immediate conversational interventions or automated emergency escalations if an unexpected health spike or user non-responsiveness is captured[cite: 15, 61, 63, 64].

## 🚀 Engineering & Architectural Highlights
* [cite_start]**Deterministic Emergency Pathing:** Employs a strict 5-second asynchronous timeout gate[cite: 40, 76]. [cite_start]If a critical physiological anomaly is flagged ($>100\text{ BPM}$) and a verbal confirmation is not registered within the window, the software instantly triggers emergency dispatch routes[cite: 64, 76, 77].
* [cite_start]**Multimodal Speech Processing Pipeline:** Chais OpenAI's Whisper (via Python `speech_recognition`) for high-precision, multilingual Acoustic Model decoding alongside Google Text-to-Speech (gTTS) for low-latency synthesis[cite: 49, 51, 53, 58].
* [cite_start]**Asynchronous Multi-Threading:** Isolates heavy input/output tasks—such as ambient therapeutic audio playback (`playsound`) and remote web requests (`twilio.rest`) [cite: 49, 59, 62]—onto independent threads to keep the main biometric observation loops non-blocking.
* [cite_start]**Empathetic Context Alignment:** Custom text parsing arrays evaluate incoming sentiment tokens (`positive_emotion_list` / `negative_emotion_list`) to decide whether to pivot into automated stress mitigation protocols (e.g., box breathing coaching) or general conversational tasks[cite: 56, 57, 65].

---

## 🛠 Tech Stack & Dependencies
* [cite_start]**Core Runtime:** Python 3.x [cite: 47]
* [cite_start]**Large Language Model Engine:** Google Gemini API (`gemini-pro`) [cite: 49]
* [cite_start]**Automatic Speech Recognition (ASR):** OpenAI Whisper (Medium Model Architecture) [cite: 49]
* [cite_start]**Biometric Telemetry / Alert Gateways:** Twilio REST Communications API [cite: 15, 62]
* [cite_start]**Audio Synthesis & Core Libraries:** Google Text-to-Speech (`gTTS`), `playsound`, Python Standard `threading` [cite: 49, 59]

---

## 📐 System Architecture & Flow Control

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
`assistant_v3.py` serves as the primary system core, hosting the asynchronous event execution loop[cite: 50]. It evaluates incoming simulated biometric feeds mirroring senior cardiac activity[cite: 34].
* **Anomaly State Activation:** Once a heartbeat breaches $100\text{ BPM}$, the program pauses lower-priority scripts to call a dedicated verification routine (`ask_are_you_okay`)[cite: 64].
* **Fail-Safe Alert Processing:** If a `sr.WaitTimeoutError` exception throws due to vocal silence or physical immobility during critical prompts, a direct webhook POST triggers via Twilio client instances to pass real-time metrics ($BPM$) to designated caretakers[cite: 61, 62].

### 2. General Assistant Modules (`assistant_v2.py`)
When heart rate telemetry settles inside safe parameters ($50 - 99\text{ BPM}$), the program falls back onto standard assistant modes[cite: 74]. This layer runs the continuous audio interface:
* Conversational prompts are wrapped dynamically with descriptive boundaries (`"Answer this question briefly: "`) before firing to the Gemini LLM matrix to ensure low-latency token replies suitable for fluid, real-time interactions[cite: 55].

---

## 🔬 Experimental Results & Failure Analysis

* **Calming Interventions:** The system safely tracked simulated fluctuations ranging between $50 - 150\text{ BPM}$ across 60-minute trial periods[cite: 69, 72]. Conversational grounding successfully engaged during 95% of identified non-emergency spikes[cite: 16].
* **Alert Precision:** During intentionally triggered unresponsive test iterations, the automated Twilio message delivery gateway registered a **100% notification success rate**, dispatching details to target contacts with a mean network latency of 7.0 seconds[cite: 16, 79, 80].
* **Edge Case Engineering Goals:** Future updates look to transition static threshold checks ($>100\text{ BPM}$) into dynamic, individual baseline arrays[cite: 46, 64]. This step aims to cut down on false alarms caused by natural, brief heart rate variability[cite: 17, 84].

---

## 👥 Contributors (Swinburne Team)
* **Albert Lau** - Core Software Architecture & API Integration Engineer

* Python
import os
# Load from secure environment variables rather than hardcoding
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
