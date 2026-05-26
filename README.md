# ASR Benchmark

This repository contains our comprehensive benchmarking suite for comparing various Automatic Speech Recognition (ASR) systems against Deepgram. 

## Overview

We benchmarked multiple models across a variety of audio datasets, testing both standard metrics and edge-case behaviors. Here is a summary of our methodology and findings.

### Model Selection
When benchmarking against Deepgram, we selected a diverse set of ASR models to provide a holistic comparison:
*   **Open-Source vs. API-Based**: We included open-source models (like OpenAI's Whisper) alongside managed API services (like Google Cloud Speech-to-Text, AWS Transcribe) to understand the trade-offs between hosting overhead vs. ease of use and cost.
*   **Model Sizes**: For models like Whisper, we evaluated different tiers (`tiny`, `base`, `small`, `medium`, `large`) to assess the accuracy-latency trade-off. 
*   **Multilingual vs. Language-Specific**: We tested models that specialize in English vs. multilingual models, particularly evaluating their performance on code-switching and non-native accents.
*   **Trade-offs**: API models offer lower operational overhead but can become costly at scale. Open-source models require infrastructure investment but offer greater privacy, control, and predictable costs. 

### Metrics
We evaluated the models based on the following metrics:
*   **Word Error Rate (WER) & Character Error Rate (CER)**: Standard industry metrics for overall transcription accuracy.
*   **Entity Accuracy**: Standard metrics often miss critical errors. If a model misinterprets a locality name or a domain-specific term (e.g., medical terminology, addresses), the entire transcription might be useless despite a low WER. We specifically measured accuracy on named entities.
*   **Formatting and Punctuation**: How well the models restore punctuation and capitalization, which significantly impacts downstream NLP tasks.

### Evaluation Methodology
We ensured a robust evaluation by slicing the data across various dimensions:
*   **Data Slicing**: Evaluated across different audio conditions (clean vs. noisy), speaker profiles (accents, genders), and utterance lengths.
*   **Language Mixing**: Tested code-switching scenarios (e.g., mixing Hindi and English) which are common in many locales.
*   **Datasets**: We utilized standard open-source datasets (like Common Voice, LibriSpeech) to establish a baseline, but also heavily weighted self-recorded, real-world domain-specific samples, which tend to be noisier and more representative of production data. 

### Beyond Transcription Accuracy
Accuracy is only part of the equation in production. We also considered:
*   **Latency**: Measured First-Byte Latency (time to first token in streaming) and Total Latency (turnaround time for batch).
*   **Throughput**: How many audio hours can be processed concurrently.
*   **Streaming vs. Batch**: Evaluated the stability and responsiveness of WebSockets/streaming APIs vs. traditional REST endpoints.
*   **Ease of Deployment & Cost**: Considered the engineering effort required to deploy open-source models (e.g., using Triton or vLLM) vs. straightforward API integration, as well as cost per minute at scale.

### Failure Analysis
Models fail in distinct ways. Some common failure modes we identified:
*   **Acoustic Noise**: Performance degradation in background noise (e.g., street noise, overlapping speakers).
*   **Accents & Code-Switching**: Heavy accents or rapid switching between languages caused hallucination in some models.
*   **Locality Names**: Rare or localized geographical names were often phoneticized incorrectly by models not trained on regional data.
*   **Short Utterances**: Lack of context in very short audio clips (< 2 seconds) led to higher error rates.

### Interpretation & Recommendations
Raw numbers must be contextualized by the use case:
*   If **real-time responsiveness** is critical (e.g., voice assistants), Deepgram or local optimized Whisper models perform best due to low latency.
*   If **cost and privacy** are paramount and latency is flexible (e.g., batch processing of call center logs), self-hosting Whisper provides a strong ROI.
*   If **enterprise support and general ease-of-use** are prioritized, major cloud provider APIs are robust but pricier.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Virtual Environment (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AbhishekBarote/ASR-.git
   cd ASR-
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   # source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Environment Variables:
   Create a `.env` file in the root directory and add your API keys based on the provided `.env.example`:
   ```env
   PORT=5000
   DEEPGRAM_API_KEY=
   GROQ_API_KEY=
   SARVAM_API_KEY=
   LOCAL_WHISPER_URL=
   NODE_ENV=development
   ```

### Running the Project

To run the main application:
```bash
python app.py
```

To run the dashboard:
```bash
streamlit run dashboard.py
# or depending on the framework used
# python dashboard.py
```
