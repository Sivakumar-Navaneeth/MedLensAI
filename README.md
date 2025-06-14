# MedLensAI
AI-powered Patient-Centric Diagnostic Assistant

## 🩺 Project Overview

MedLensAI is a multi-modal clinical assistant that helps clinicians and telemedicine platforms rapidly assess medical images alongside structured/unstructured clinical notes to provide:
- Image-based diagnostic suggestions
- Cross-referenced report summaries
- Symptom-image correlation
- Follow-up investigation suggestions

Built securely and intelligently using Google's MedGemma for multimodal reasoning and Hugging Face models for medical NLP.

## 🌍 Real-World Problem It Solves

1. **Overloaded Doctors**: Clinicians are burdened by information overload—images, reports, and patient history all spread across systems.
2. **Rural/Telemedicine Gaps**: In rural or telehealth contexts, having an assistant that can analyze images and correlate them with clinical symptoms adds immense diagnostic accuracy.
3. **Time-critical triage**: In emergencies (e.g., trauma, acute GI bleeding), image + note analysis can flag urgent cases fast.

## 🧠 Key Features & AI Capabilities

| Task | How It's Used |
|------|---------------|
| Visual Question Answering (VQA) | Analyze radiology/clinical images based on doctor prompts |
| Image Classification | Skin lesion or chest X-ray classification |
| Text Classification | Triage risk from unstructured clinical notes |
| Token Classification (NER) | Extract symptoms, conditions, drugs from EHR text |
| Summarization | Auto-summarize radiologist reports and patient history |
| Text2Text Generation | Generate follow-up recommendations |

## 🔗 External APIs & Data Sources

- 🏥 **MIMIC-IV / MIMIC-CXR datasets** - De-identified patient EHR + X-rays for prototyping
- 📡 **OpenFDA API** - Drug interactions and treatment suggestions
- 🌍 **WHO ICD API** - Classify and map diagnostic codes
- 🧬 **UMLS** (Optional) - Standardized medical vocabulary integration

## 🏗️ Architecture

### Frontend
- Streamlit-based interface
- Image upload for radiology/dermatology
- Doctor-style prompt box
- Timeline view of patient notes + model summaries

### Backend
- Streamlit server
- MedGemma (via local pipeline)
- PostgreSQL for case history & audit logging

### Scalability
- Modular API-first backend for EMR integration
- Docker deployment support

## 🧪 Feature Set

| Feature | Value |
|---------|-------|
| Upload image + notes | Simulates real diagnostic pipeline |
| Ask contextual image questions | Like: "Is there a fracture on this X-ray given swelling in leg?" |
| Highlight medical entities in reports | Fast info extraction |
| Summary generation | Saves clinician time |
| API-first design | Enables telehealth integration |
| Case-based storage | Enables ongoing learning & audit trails |

## 🚀 Why MedLensAI Stands Out

- Uses real patient data and state-of-the-art AI models
- Tackles a critical and growing healthcare need
- Fully multimodal, production-ready solution
- Designed for future integration and scalability
- Demonstrates comprehensive product thinking

## 💻 Development

### Using Conda (Recommended)

1. Install Miniconda or Anaconda if you haven't already
2. Clone the repository:
```bash
git clone https://github.com/yourusername/MedLensAI.git
cd MedLensAI
```

3. Run the setup script:
```bash
./setup_conda.sh
```

4. Activate the environment:
```bash
conda activate medlensai
```

5. Run the application:
```bash
streamlit run src/app.py
```

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please follow PEP 8 style guidelines.

Questions? Open an issue!

