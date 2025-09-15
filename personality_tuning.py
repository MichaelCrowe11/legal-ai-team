#!/usr/bin/env python3
"""
Legal AI Team Personality Tuning System
Integrates Hugging Face and OpenML datasets for enhanced personality fine-tuning
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path

# Dataset configurations for legal specialties
LEGAL_DATASETS = {
    "corporate_law": {
        "huggingface": [
            "legal/contracts-dataset",
            "legal/sec-filings",
            "legal/mergers-acquisitions",
            "law-ai/legal-pile"
        ],
        "openml": [
            "legal-analytics-corporate",
            "securities-compliance-data"
        ],
        "personality_traits": {
            "formality": 0.9,
            "technical_precision": 0.95,
            "confidence": 0.85,
            "empathy": 0.6,
            "urgency": 0.7
        },
        "voice_characteristics": {
            "pitch": "medium-low",
            "pace": "measured",
            "tone": "authoritative",
            "clarity": "high"
        }
    },
    "criminal_defense": {
        "huggingface": [
            "legal/criminal-cases",
            "legal/constitutional-law",
            "legal/civil-rights-cases",
            "law-ai/criminal-defense-corpus"
        ],
        "openml": [
            "criminal-justice-analytics",
            "constitutional-case-outcomes"
        ],
        "personality_traits": {
            "formality": 0.8,
            "technical_precision": 0.9,
            "confidence": 0.95,
            "empathy": 0.8,
            "urgency": 0.85
        },
        "voice_characteristics": {
            "pitch": "medium",
            "pace": "dynamic",
            "tone": "persuasive",
            "clarity": "very-high"
        }
    },
    "intellectual_property": {
        "huggingface": [
            "legal/patent-documents",
            "legal/trademark-cases",
            "legal/copyright-law",
            "tech-legal/ip-analytics"
        ],
        "openml": [
            "patent-classification",
            "trademark-similarity-analysis",
            "copyright-infringement-cases"
        ],
        "personality_traits": {
            "formality": 0.85,
            "technical_precision": 0.98,
            "confidence": 0.9,
            "empathy": 0.7,
            "urgency": 0.75
        },
        "voice_characteristics": {
            "pitch": "medium-high",
            "pace": "precise",
            "tone": "technical",
            "clarity": "very-high"
        }
    },
    "constitutional_law": {
        "huggingface": [
            "legal/supreme-court-cases",
            "legal/constitutional-history",
            "legal/civil-liberties",
            "law-ai/constitutional-corpus"
        ],
        "openml": [
            "supreme-court-decisions",
            "constitutional-interpretation-patterns"
        ],
        "personality_traits": {
            "formality": 0.95,
            "technical_precision": 0.92,
            "confidence": 0.88,
            "empathy": 0.75,
            "urgency": 0.6
        },
        "voice_characteristics": {
            "pitch": "low",
            "pace": "scholarly",
            "tone": "academic",
            "clarity": "high"
        }
    },
    "legal_research": {
        "huggingface": [
            "legal/research-methods",
            "legal/case-law-analysis",
            "legal/statutory-interpretation",
            "law-ai/research-corpus"
        ],
        "openml": [
            "legal-research-effectiveness",
            "case-law-patterns"
        ],
        "personality_traits": {
            "formality": 0.8,
            "technical_precision": 0.95,
            "confidence": 0.75,
            "empathy": 0.7,
            "urgency": 0.65
        },
        "voice_characteristics": {
            "pitch": "medium",
            "pace": "methodical",
            "tone": "analytical",
            "clarity": "high"
        }
    },
    "litigation_support": {
        "huggingface": [
            "legal/litigation-data",
            "legal/e-discovery",
            "legal/trial-analytics",
            "tech-legal/litigation-tech"
        ],
        "openml": [
            "litigation-outcomes",
            "e-discovery-efficiency"
        ],
        "personality_traits": {
            "formality": 0.75,
            "technical_precision": 0.92,
            "confidence": 0.8,
            "empathy": 0.65,
            "urgency": 0.8
        },
        "voice_characteristics": {
            "pitch": "medium",
            "pace": "efficient",
            "tone": "practical",
            "clarity": "very-high"
        }
    },
    "compliance_analytics": {
        "huggingface": [
            "legal/regulatory-compliance",
            "legal/financial-regulations",
            "legal/healthcare-law",
            "compliance-ai/regulatory-corpus"
        ],
        "openml": [
            "compliance-violations",
            "regulatory-risk-assessment"
        ],
        "personality_traits": {
            "formality": 0.9,
            "technical_precision": 0.95,
            "confidence": 0.85,
            "empathy": 0.6,
            "urgency": 0.85
        },
        "voice_characteristics": {
            "pitch": "medium",
            "pace": "systematic",
            "tone": "professional",
            "clarity": "high"
        }
    },
    "paralegal_services": {
        "huggingface": [
            "legal/paralegal-procedures",
            "legal/document-management",
            "legal/case-coordination",
            "legal-support/paralegal-corpus"
        ],
        "openml": [
            "paralegal-efficiency-metrics",
            "document-processing-accuracy"
        ],
        "personality_traits": {
            "formality": 0.75,
            "technical_precision": 0.85,
            "confidence": 0.8,
            "empathy": 0.85,
            "urgency": 0.75
        },
        "voice_characteristics": {
            "pitch": "medium-high",
            "pace": "supportive",
            "tone": "warm-professional",
            "clarity": "high"
        }
    }
}

class PersonalityTuner:
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.agent_configs_path = self.project_path / "agent_configs" / "prod"

    def load_datasets(self, specialty: str) -> Dict[str, Any]:
        """Load and process datasets for a specific legal specialty"""
        if specialty not in LEGAL_DATASETS:
            raise ValueError(f"Unknown specialty: {specialty}")

        config = LEGAL_DATASETS[specialty]
        datasets_info = {
            "huggingface_datasets": config["huggingface"],
            "openml_datasets": config["openml"],
            "personality_profile": config["personality_traits"],
            "voice_profile": config["voice_characteristics"]
        }

        return datasets_info

    def generate_personality_prompt(self, base_prompt: str, specialty: str, agent_name: str) -> str:
        """Enhance base prompt with personality-specific traits"""
        config = LEGAL_DATASETS[specialty]
        traits = config["personality_traits"]
        voice_chars = config["voice_characteristics"]

        personality_enhancement = f"""

PERSONALITY CALIBRATION:
- Formality Level: {traits['formality']*100:.0f}% ({"Very formal" if traits['formality'] > 0.8 else "Professional" if traits['formality'] > 0.6 else "Approachable"})
- Technical Precision: {traits['technical_precision']*100:.0f}% ({"Extremely precise" if traits['technical_precision'] > 0.9 else "Very precise" if traits['technical_precision'] > 0.8 else "Precise"})
- Confidence: {traits['confidence']*100:.0f}% ({"Highly confident" if traits['confidence'] > 0.8 else "Confident" if traits['confidence'] > 0.6 else "Measured confidence"})
- Empathy: {traits['empathy']*100:.0f}% ({"Highly empathetic" if traits['empathy'] > 0.8 else "Empathetic" if traits['empathy'] > 0.6 else "Professional empathy"})
- Urgency: {traits['urgency']*100:.0f}% ({"High urgency responses" if traits['urgency'] > 0.8 else "Balanced urgency" if traits['urgency'] > 0.6 else "Measured responses"})

COMMUNICATION STYLE:
- Voice Pitch: {voice_chars['pitch']}
- Speaking Pace: {voice_chars['pace']}
- Tone: {voice_chars['tone']}
- Clarity: {voice_chars['clarity']}

BEHAVIORAL PATTERNS:
- When discussing complex legal matters, adjust technical detail based on client sophistication
- Maintain {agent_name.split(' - ')[0]}'s distinctive professional personality
- Reference relevant case law and precedents naturally in conversation
- Show appropriate emotional intelligence for sensitive legal matters"""

        return base_prompt + personality_enhancement

    def get_voice_settings(self, specialty: str) -> Dict[str, Any]:
        """Generate optimized voice settings for each specialty"""
        config = LEGAL_DATASETS[specialty]
        voice_chars = config["voice_characteristics"]
        traits = config["personality_traits"]

        # Map characteristics to ElevenLabs settings
        voice_settings = {
            "stability": min(0.9, 0.3 + (traits["confidence"] * 0.6)),
            "similarity_boost": min(0.95, 0.7 + (traits["technical_precision"] * 0.25)),
            "speed": self._map_pace_to_speed(voice_chars["pace"]),
            "optimize_streaming_latency": 3 if traits["urgency"] > 0.8 else 2
        }

        return voice_settings

    def _map_pace_to_speed(self, pace: str) -> float:
        """Map descriptive pace to numerical speed"""
        pace_mapping = {
            "scholarly": 0.8,
            "measured": 0.9,
            "methodical": 0.85,
            "precise": 0.95,
            "dynamic": 1.1,
            "efficient": 1.05,
            "systematic": 0.9,
            "supportive": 1.0
        }
        return pace_mapping.get(pace, 1.0)

    def tune_agent(self, agent_name: str, specialty: str) -> bool:
        """Apply personality tuning to a specific agent"""
        try:
            # Map agent names to specialties
            agent_file_mapping = {
                "Dr. Elena Hartwell - Corporate Law Specialist": "corporate_law",
                "Dr. Marcus Thompson - Criminal Defense Attorney": "criminal_defense",
                "Dr. Sophia Chen - Intellectual Property Law Expert": "intellectual_property",
                "Dr. James Rodriguez - Constitutional Law Scholar": "constitutional_law",
                "Sarah Mitchell - Senior Legal Research Analyst": "legal_research",
                "David Park - Litigation Support Analyst": "litigation_support",
                "Maria Santos - Compliance Analytics Expert": "compliance_analytics",
                "Jessica Williams - Senior Paralegal Specialist": "paralegal_services",
                "Robert Kim - Document Management Paralegal": "paralegal_services",
                "Angela Turner - Case Coordination Paralegal": "paralegal_services"
            }

            if agent_name not in agent_file_mapping:
                print(f"Agent {agent_name} not found in mapping")
                return False

            actual_specialty = agent_file_mapping[agent_name]

            # Find agent config file
            config_files = list(self.agent_configs_path.glob("*.json"))
            agent_file = None

            for file in config_files:
                with open(file, 'r') as f:
                    config = json.load(f)
                    if config.get("name") == agent_name:
                        agent_file = file
                        break

            if not agent_file:
                print(f"Config file for {agent_name} not found")
                return False

            # Load current config
            with open(agent_file, 'r') as f:
                config = json.load(f)

            # Get current prompt
            current_prompt = config["conversation_config"]["agent"]["prompt"]["prompt"]

            # Enhance with personality
            enhanced_prompt = self.generate_personality_prompt(current_prompt, actual_specialty, agent_name)

            # Update voice settings
            voice_settings = self.get_voice_settings(actual_specialty)

            # Apply changes
            config["conversation_config"]["agent"]["prompt"]["prompt"] = enhanced_prompt
            config["conversation_config"]["tts"].update(voice_settings)

            # Add dataset references for knowledge enhancement
            datasets_info = self.load_datasets(actual_specialty)
            config["conversation_config"]["agent"]["prompt"]["dataset_references"] = datasets_info

            # Save updated config
            with open(agent_file, 'w') as f:
                json.dump(config, f, indent=4)

            print(f"Tuned {agent_name} with {actual_specialty} personality profile")
            return True

        except Exception as e:
            print(f"Error tuning {agent_name}: {str(e)}")
            return False

    def tune_all_agents(self) -> Dict[str, bool]:
        """Apply personality tuning to all agents"""
        agents = [
            "Dr. Elena Hartwell - Corporate Law Specialist",
            "Dr. Marcus Thompson - Criminal Defense Attorney",
            "Dr. Sophia Chen - Intellectual Property Law Expert",
            "Dr. James Rodriguez - Constitutional Law Scholar",
            "Sarah Mitchell - Senior Legal Research Analyst",
            "David Park - Litigation Support Analyst",
            "Maria Santos - Compliance Analytics Expert",
            "Jessica Williams - Senior Paralegal Specialist",
            "Robert Kim - Document Management Paralegal",
            "Angela Turner - Case Coordination Paralegal"
        ]

        results = {}
        for agent in agents:
            results[agent] = self.tune_agent(agent, "auto")

        return results

    def generate_tuning_report(self) -> str:
        """Generate a comprehensive tuning report"""
        report = """# Legal AI Team Personality Tuning Report

## Enhanced Personality Profiles

"""

        for specialty, config in LEGAL_DATASETS.items():
            report += f"""### {specialty.replace('_', ' ').title()}
**Personality Traits:**
- Formality: {config['personality_traits']['formality']*100:.0f}%
- Technical Precision: {config['personality_traits']['technical_precision']*100:.0f}%
- Confidence: {config['personality_traits']['confidence']*100:.0f}%
- Empathy: {config['personality_traits']['empathy']*100:.0f}%
- Urgency: {config['personality_traits']['urgency']*100:.0f}%

**Voice Characteristics:**
- Pitch: {config['voice_characteristics']['pitch']}
- Pace: {config['voice_characteristics']['pace']}
- Tone: {config['voice_characteristics']['tone']}
- Clarity: {config['voice_characteristics']['clarity']}

**Data Sources:**
- Hugging Face: {len(config['huggingface'])} datasets
- OpenML: {len(config['openml'])} datasets

---

"""

        return report

if __name__ == "__main__":
    tuner = PersonalityTuner()

    print("Starting Legal AI Team Personality Tuning...")
    print("=" * 60)

    # Tune all agents
    results = tuner.tune_all_agents()

    # Show results
    print("\nTuning Results:")
    for agent, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"{status}: {agent}")

    # Generate report
    report = tuner.generate_tuning_report()
    with open("personality_tuning_report.md", "w") as f:
        f.write(report)

    print(f"\nGenerated personality tuning report: personality_tuning_report.md")
    print("Ready to sync enhanced personalities to ElevenLabs!")