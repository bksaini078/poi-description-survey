We sincerely thank the reviewers for their time, constructive feedback, and valuable insights. Their comments have highlighted important areas for clarification. To address the feedback comprehensively and avoid redundancy, we have categorized the reviewers' concerns into five key thematic areas. Below, we provide detailed responses and outline the changes we will incorporate into the revised manuscript.

## 1. Methodology: Experimental Setup and Operationalization (R1.1, R2.1, R2 Major Issue)

**Concern:** Major issues with details in the experimental setup (which potentially invalidate findings); lack of clarity on how personal characteristics were mapped to content changes.

**Response:** We appreciate the opportunity to clarify this. Personalization was not operationalized through hardcoded feature mappings but via a zero-shot prompting strategy. We used ten user dimensions collected during the survey: Age, Gender, Marital Status, Children, Interests, Travel Experience, Education, Profession, Hobbies, and Preferred Travel Style.

To illustrate our methodology and support reproducibility, the exact Python string prompts used to instruct the Large Language Model (GPT-4o) were as follows:

```python
system_prompt = f"""You are an expert travel writer and content creator. Your task is to create engaging, 
informative titles and descriptions for Points of Interest (POIs) that capture attention and provide value to potential visitors.
Focus on unique aspects, cultural significance, and visitor experience. Consider the visitor's family situation and adapt the content
to highlight relevant aspects (e.g., family-friendly features, romantic spots for couples, etc.).

IMPORTANT LENGTH CONSTRAINTS:
- The description MUST NOT exceed {max_description_length} characters
- The title MUST NOT exceed {max_title_length} characters
- Be concise while maintaining informativeness"""

prompt = f"""Create a title and description for this Point of Interest, personalized for the following user:
User Age: {user_data.get('age', 'Not specified')}
User Gender: {user_data.get('gender', 'Not specified')}
Marital Status: {user_data.get('marital_status', 'Not specified')}
Have Children: {user_data.get('has_children', 'Not specified')}
User Interests: {user_data.get('interests', 'Not specified')}
User Travel Experience: {user_data.get('travel_experience', 'Not specified')}
Education Level: {user_data.get('education', 'Not specified')}
Profession: {user_data.get('profession', 'Not specified')}
Hobbies: {user_data.get('hobbies', 'Not specified')}
Preferred Travel Style: {user_data.get('preferred_travel_style', 'Not specified')}

Point of Interest:
Original Title: {poi_data['title']}
Original Description: {poi_data['description']}

STRICT LENGTH REQUIREMENTS:
- Your description MUST be {max_description_length} characters or less
- Your title MUST be {max_title_length} characters or less"""
```

This structure naturally guided the LLM to emphasize architectural and historical facts when generating a description of the Colosseum for a user whose profile indicates they are an academic interested in history, whereas it highlighted interactive and visually engaging aspects for a user traveling with children. We will expand Section 3.3 to explicitly detail this prompting strategy and include these concrete examples to demonstrate how identical factual content was linguistically adapted.

## 2. Methodology: POI Selection (R4.3)

**Concern:** Need for more detail on how POIs were selected for each participant.

**Response:** We acknowledge the ambiguity in our initial description. The 10 POIs were not dynamically selected or uniquely matched to individual participants. Instead, the researchers pre-selected a fixed set of 10 POIs, representing five distinct categories (accommodation, natural attractions, entertainment, cultural, and commercial). Every participant evaluated this exact same set of 10 POIs. This controlled, homogeneous presentation was a deliberate experimental design choice to eliminate POI variance across users, enabling a consistent and valid within-subjects comparison between the manual and AI-generated baselines. We will clarify this uniform selection process and its rationale in Section 3.1 of the revised manuscript to assure readers of the study's internal validity.

## 3. Demographics and Sample Skew (R2 Weakness)

**Concern:** Convenience sample that is quite skewed (predominantly Indian and German).

**Response:** This is a fair assessment. Our initial survey utilized convenience sampling, resulting in a predominantly Indian (n=28) and German (n=21) participant pool. While this limits the immediate cross-cultural generalizability of the findings, the primary objective of this short paper was to establish a foundational proof-of-concept for zero-shot LLM personalization of micro-content. The within-subjects experimental design helps mitigate some of this demographic skew by comparing each user's AI-adapted response directly against their manual response baseline. We will explicitly insert a "Limitations" paragraph detailing the demographic skew and clearly stating that these initial findings must be validated in future work using larger, probabilistically stratified global samples.

## 4. Evaluation: Trustworthiness and Factual Accuracy (R1.2, R2.2, R3.1)

**Concern:** "Trustworthiness" measurement relies on perceived credibility rather than factual accuracy; checking of generated descriptions is unclear.

**Response:** This is a highly valid observation. Our study specifically measures "perceived trustworthiness" based on a 5-point intensity scale, which captures subjective user confidence rather than objective factual accuracy. The higher trustworthiness scores for AI-generated content indicate that personalized relevance enhances perceived credibility, aligning with recent findings in generative tourism AI (Li et al., 2025, DOI: [10.1016/j.tourman.2025.105179](https://doi.org/10.1016/j.tourman.2025.105179)).

To mitigate hallucinatory content and ensure factual preservation prior to the user study, the research team manually cross-checked the generated descriptions against the original ground truth texts (sourced from official tourism websites). The LLM was explicitly constrained by strict character length limits matching the original descriptions and instructed to maintain factual integrity. We will update the methodology to detail this manual verification step and explicitly state the distinction between perceived credibility and factual accuracy as a limitation.

## 5. Analysis and Scope: Granularity and LLM Selection (R1.3, R2.3, R3.2, R4.2)

**Concern:** Analysis aggregates results across POIs/users; limited results; only one proprietary LLM was used.

**Response:** As a proof-of-concept exploratory study within the short paper format (51 participants), our primary objective was to demonstrate the feasibility and initial baseline effect of zero-shot LLM personalization. Consequently, the sample size per POI category was insufficient to conduct a robust, highly granular subgroup analysis (e.g., by specific demographic or POI type) without risking statistical anomalies.

Similarly, we selected GPT-4o for this initial study due to its established strict instruction and length adherence capabilities. We fully agree with the reviewers that comparing proprietary models with open-source alternatives (such as Llama 3) and conducting large-scale demographic analyses are vital next steps. We will add a dedicated paragraph in the Discussion section identifying these scope constraints as limitations and framing them as necessary directions for future scaled research.

## 6. Related Work (R2 Weakness)

**Concern:** Weak related work.

**Response:** We appreciate this feedback. Given the strict page limits of the short paper format, our initial literature review was highly compressed. In the revised manuscript, we will expand Section 2 (Related Work) to more robustly contextualize our contribution. Specifically, we will include a broader discussion on the progression from traditional context-aware POI recommenders (e.g., Renjith et al., 2020, DOI: [10.1016/j.ipm.2019.102078](https://doi.org/10.1016/j.ipm.2019.102078)) to recent LLM-driven generation paradigms in tourism (e.g., Wang et al., 2024, IEEE Intelligent Systems, DOI: [10.1109/MIS.2023.3343489](https://doi.org/10.1109/MIS.2023.3343489); Li et al., 2025, Tourism Management, DOI: [10.1016/j.tourman.2025.105179](https://doi.org/10.1016/j.tourman.2025.105179)). 


## 7. Ethics and Reproducibility (R1.4, R2.4, R3.3, R4.1)

**Concern:** Difficult to replicate without exact prompts/questionnaires; lack of explicit mention regarding IRB permissions and ethical concerns regarding personal data usage.

**Response:** We thank the reviewers for pointing out these critical formatting constraints.

**Ethics:** The survey website was designed with a mandatory first step where participants reviewed an informed consent form. This form explicitly detailed institutional data privacy guidelines, the purpose of collecting personal preference data (such as profession, hobbies, and travel styles), and guaranteed participant anonymity. As noted by Reviewer 3, the discomfort reported by some participants regarding data disclosure underscores a crucial privacy-personalization trade-off. We will revise the Ethical Considerations section to explicitly outline these institutional approval details, the website's consent mechanism, and add a paragraph to the Discussion section specifically exploring this tension between user privacy and the accuracy of AI adaptation.

**Reproducibility:** To ensure complete transparency and reproducibility, we will release a public GitHub repository. This repository will be linked in the revised manuscript and contains the complete survey instrument, the exact system and user prompts used for the GPT-4o API, the configuration schema (including all available options for hobbies, travel styles, etc.), and side-by-side examples of original and personalized descriptions.
