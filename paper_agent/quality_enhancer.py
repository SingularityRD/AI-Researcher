"""
Paper Quality Enhancer for NeurIPS-tier publications

This module ensures papers meet top-tier conference standards (NeurIPS, ICML, ICLR)
by checking and enhancing:
- Technical rigor
- Statistical significance
- Comprehensive experiments
- Clear contributions
- Strong baselines
- Theoretical analysis
"""

import logging
from typing import Dict, List, Optional, Tuple
from benchmark_collection.utils.openai_utils import GPTClient

logger = logging.getLogger(__name__)


# CRITICAL: Anti-hallucination preamble for ALL prompts
# Used across all paper enhancement methods to prevent fabrication
ANTI_HALLUCINATION_PREAMBLE = """
⚠️  CRITICAL ANTI-HALLUCINATION INSTRUCTIONS ⚠️

You MUST follow these rules STRICTLY:

1. **NEVER fabricate experimental results or numbers**
   - Only use results explicitly provided in RESULTS DATA section
   - If no results provided, mark as [NEEDS EXPERIMENTAL DATA]
   - Never invent p-values, confidence intervals, or accuracy numbers

2. **NEVER make up citations or references**
   - Only cite papers explicitly mentioned in the context
   - If you need to reference prior work, use [CitationNeeded: description]
   - Never invent author names, years, or paper titles

3. **NEVER claim unproven theoretical results**
   - Only state what is mathematically proven in the methodology
   - Mark theoretical gaps as [REQUIRES THEORETICAL PROOF]
   - Never invent theorems, lemmas, or proofs

4. **NEVER fabricate baselines or comparisons**
   - Only compare with baselines explicitly provided
   - If baseline results unknown, mark as [BASELINE RESULTS NEEDED]
   - Never guess baseline performance

5. **BE CONSERVATIVE with claims**
   - Only claim what is demonstrated by actual experiments
   - Use "our experiments show" only for real results
   - Mark speculative claims as "we hypothesize" or "future work"

6. **GROUND ALL STATEMENTS in provided data**
   - Every quantitative claim must reference actual data
   - Every comparison must be based on real experiments
   - Every conclusion must follow from results

VIOLATION OF THESE RULES IS ACADEMIC MISCONDUCT.
"""


class PaperQualityEnhancer:
    """Enhances paper quality to NeurIPS-tier standards with hallucination prevention"""

    def __init__(self, gpt_model: str = "gpt-4o"):
        """
        Initialize quality enhancer with hallucination prevention

        Args:
            gpt_model: GPT model for quality checks (use stronger model)
        """
        self.gpt_client = GPTClient(model=gpt_model)
        self.quality_criteria = self._load_quality_criteria()

    def _load_quality_criteria(self) -> Dict:
        """Load NeurIPS-tier quality criteria"""
        return {
            "contributions": {
                "required": [
                    "Clear statement of contributions",
                    "Explicit novelty claims",
                    "Comparison with prior work",
                    "Significance and impact discussion"
                ],
                "weight": 0.25
            },
            "methodology": {
                "required": [
                    "Theoretical justification",
                    "Mathematical rigor",
                    "Algorithm pseudo-code",
                    "Complexity analysis",
                    "Implementation details"
                ],
                "weight": 0.20
            },
            "experiments": {
                "required": [
                    "Strong SOTA baselines (5+ baselines)",
                    "Multiple datasets (3+ datasets)",
                    "Statistical significance (p-values, confidence intervals)",
                    "Comprehensive ablations",
                    "Hyperparameter sensitivity",
                    "Runtime analysis",
                    "Memory footprint",
                    "Reproducibility details"
                ],
                "weight": 0.30
            },
            "related_work": {
                "required": [
                    "Comprehensive coverage (20+ papers)",
                    "Critical analysis",
                    "Clear positioning",
                    "Comparison table"
                ],
                "weight": 0.10
            },
            "writing": {
                "required": [
                    "Clear and concise",
                    "Logical flow",
                    "Good figures",
                    "Consistent notation",
                    "No grammatical errors"
                ],
                "weight": 0.10
            },
            "ethics": {
                "required": [
                    "Limitations section",
                    "Broader impact discussion",
                    "Reproducibility statement",
                    "Data/code availability"
                ],
                "weight": 0.05
            }
        }

    async def check_paper_quality(
        self,
        sections: Dict[str, str]
    ) -> Tuple[float, Dict[str, any]]:
        """
        Comprehensive quality check

        Args:
            sections: Dictionary of paper sections

        Returns:
            Tuple of (overall_score, detailed_report)
        """
        report = {}
        scores = {}

        # Check each aspect
        for aspect, criteria in self.quality_criteria.items():
            score, details = await self._check_aspect(
                aspect,
                sections,
                criteria["required"]
            )
            scores[aspect] = score * criteria["weight"]
            report[aspect] = details

        overall_score = sum(scores.values())
        report["overall_score"] = overall_score
        report["scores"] = scores
        report["tier"] = self._classify_tier(overall_score)

        return overall_score, report

    async def _check_aspect(
        self,
        aspect: str,
        sections: Dict[str, str],
        requirements: List[str]
    ) -> Tuple[float, Dict]:
        """Check specific aspect of paper"""

        prompt = f"""Analyze the paper sections for {aspect.upper()} quality.

Requirements to check:
{chr(10).join(f"- {req}" for req in requirements)}

Paper sections:
{self._format_sections(sections)}

Rate each requirement (0-10) and provide specific feedback:
1. What is present and good
2. What is missing or weak
3. How to improve

Output format:
SCORES:
- Requirement 1: X/10
- Requirement 2: Y/10
...

ANALYSIS:
[Detailed analysis]

IMPROVEMENTS:
[Specific suggestions]
"""

        response = await self.gpt_client.chat(prompt=prompt)

        # Parse scores and feedback
        score, feedback = self._parse_check_response(response, requirements)

        return score, {
            "score": score,
            "feedback": feedback,
            "requirements": requirements
        }

    def _format_sections(self, sections: Dict[str, str]) -> str:
        """Format sections for prompt"""
        formatted = []
        for name, content in sections.items():
            formatted.append(f"\n=== {name.upper()} ===\n{content[:2000]}...")
        return "\n".join(formatted)

    def _parse_check_response(
        self,
        response: str,
        requirements: List[str]
    ) -> Tuple[float, str]:
        """Parse GPT response to extract scores"""
        # Simple parsing - can be enhanced
        scores = []
        for line in response.split('\n'):
            if '/10' in line:
                try:
                    score = float(line.split(':')[1].split('/')[0].strip())
                    scores.append(score)
                except:
                    pass

        avg_score = sum(scores) / len(scores) if scores else 5.0
        return avg_score / 10.0, response

    def _classify_tier(self, score: float) -> str:
        """Classify paper tier based on score"""
        if score >= 0.85:
            return "NeurIPS/ICML Spotlight (Top 5%)"
        elif score >= 0.75:
            return "NeurIPS/ICML Accept (Top 20%)"
        elif score >= 0.65:
            return "Workshop/ICLR Accept"
        else:
            return "Needs Major Revision"

    def validate_for_hallucination(self, content: str, allowed_numbers: Optional[List[float]] = None) -> List[str]:
        """
        Check content for potential hallucinations

        Returns list of warnings about potential fabrications
        """
        warnings = []

        # Check for suspicious patterns
        import re

        # Look for very specific numbers that weren't provided
        if allowed_numbers:
            # Find all numbers in content
            found_numbers = re.findall(r'\d+\.?\d*', content)
            for num_str in found_numbers:
                try:
                    num = float(num_str)
                    # Check if number close to any allowed number (within 0.01%)
                    if not any(abs(num - allowed) < 0.0001 * max(abs(allowed), 1) for allowed in allowed_numbers):
                        # Check if it's a common number (like 95 for confidence interval)
                        if num not in [95, 99, 0.05, 0.01, 0.001, 42, 123, 456, 789, 1000]:  # Common values
                            warnings.append(f"⚠️  Found unexpected number: {num_str} - verify this is not fabricated")
                except ValueError:
                    pass

        # Check for suspiciously precise results
        precise_results = re.findall(r'\d+\.\d{3,}', content)
        if len(precise_results) > 5:
            warnings.append("⚠️  Many highly precise numbers found - ensure these are from actual experiments")

        # Check for suspicious citation patterns
        suspicious_citations = [
            r'\[Author et al\., \d{4}\]',  # Generic citation format
            r'\[Smith.*\d{4}\]',  # Common placeholder name
            r'\[Doe.*\d{4}\]',  # Common placeholder name
        ]
        for pattern in suspicious_citations:
            if re.search(pattern, content):
                warnings.append("⚠️  Found potentially generic citation - verify all citations are real")

        # Check for ungrounded claims
        strong_claims = [
            'we prove that',
            'theorem.*shows',
            'we demonstrate.*improvement',
            'achieves state-of-the-art',
            'outperforms all.*baselines'
        ]
        for claim in strong_claims:
            if re.search(claim, content, re.IGNORECASE):
                warnings.append(f"⚠️  Found strong claim: '{claim}' - ensure this is backed by actual results")

        # Check for TODO markers that should have been caught
        todo_markers = ['[NEEDS', '[TO BE', '[Citation Needed]', '[Verify:', '[REQUIRES']
        for marker in todo_markers:
            if marker in content:
                warnings.append(f"⚠️  Found placeholder marker: {marker} - needs to be resolved")

        return warnings

    async def enhance_contributions(self, content: str, experimental_results: Optional[Dict] = None) -> str:
        """Enhance contribution section for clarity and impact (hallucination-safe)"""

        prompt = f"""{ANTI_HALLUCINATION_PREAMBLE}

Revise the following contributions section to NeurIPS-tier quality.

CURRENT CONTENT:
{content}

EXPERIMENTAL RESULTS (GROUND TRUTH):
{experimental_results if experimental_results else "[NO RESULTS PROVIDED - Do not make quantitative claims]"}

ENHANCEMENT GUIDELINES:
1. CLARITY: Use numbered list with bold headings
2. NOVELTY: Explicitly state what is new vs. prior work (only cite papers mentioned in content)
3. IMPACT: Explain significance and potential impact
4. EVIDENCE: Back claims ONLY with provided experimental results
5. POSITIONING: Compare with closest related work (only if mentioned in content)

⚠️  CRITICAL: If experimental results not provided, use placeholders like:
   - "Achieving [X]% improvement..." → "Achieving significant improvement (see Section 4)..."
   - Do NOT invent specific numbers

Format:
Our key contributions are:
1. **Novel Architecture/Method**: [Clear description] Unlike [PriorWork if mentioned], our approach...
2. **Theoretical Analysis**: [Only if proven in methodology]...
3. **Empirical Validation**: [Only based on provided results]...
4. **Open-Source Release**: [What is released] Enabling reproducibility...

Write the enhanced version (be conservative, don't hallucinate):
"""

        return await self.gpt_client.chat(prompt=prompt)

    async def add_statistical_significance(
        self,
        experiments_section: str,
        results_data: Dict
    ) -> str:
        """Add statistical significance analysis to experiments (hallucination-safe)"""

        prompt = f"""{ANTI_HALLUCINATION_PREAMBLE}

Add statistical significance analysis to the experiments section.

CURRENT EXPERIMENTS:
{experiments_section}

RESULTS DATA (GROUND TRUTH - ONLY SOURCE OF NUMBERS):
{results_data}

⚠️  CRITICAL RULES FOR NUMBERS:
1. ONLY use numbers from RESULTS DATA above
2. If standard deviations not provided, write "std not reported"
3. If p-values not computed, write "[p-value to be computed]"
4. If multiple runs not available, write "single run reported"
5. NEVER make up confidence intervals or p-values

ADD THE FOLLOWING (only if data available):
1. **Confidence Intervals**: Report 95% CI for main metrics (if std available)
2. **P-values**: Statistical tests vs. baselines (if computed)
3. **Effect Size**: Cohen's d or similar (if computable from data)
4. **Multiple Runs**: Report mean ± std over 3-5 runs (if available)
5. **Significance Indicators**: Use *, **, *** only if p-values computed

Example table format (use ONLY if you have the actual numbers):
Method          | Metric 1        | Metric 2        | p-value
----------------|-----------------|-----------------|--------
Baseline 1      | [from data]    | [from data]     | -
Baseline 2      | [from data]    | [from data]     | -
Ours           | [from data]*** | [from data]***  | [if computed]

If data insufficient, mark as [STATISTICAL ANALYSIS PENDING EXPERIMENTAL DATA]

Write the enhanced experiments section (NO FABRICATED NUMBERS):
"""

        return await self.gpt_client.chat(prompt=prompt)

    async def enhance_ablations(
        self,
        method_description: str,
        current_ablations: str,
        ablation_results: Optional[Dict] = None
    ) -> str:
        """Generate comprehensive ablation studies (hallucination-safe)"""

        prompt = f"""{ANTI_HALLUCINATION_PREAMBLE}

Design comprehensive ablation studies for NeurIPS-tier quality.

METHOD DESCRIPTION:
{method_description}

CURRENT ABLATIONS:
{current_ablations}

ABLATION RESULTS (GROUND TRUTH):
{ablation_results if ablation_results else "[NO ABLATION RESULTS - Mark as future work or to be conducted]"}

⚠️  CRITICAL RULES FOR ABLATIONS:
1. If ablation results NOT provided, describe what SHOULD be done
2. Use language: "We plan to ablate..." or "Ablations should include..."
3. NEVER invent ablation results or numbers
4. If partial results available, only report those
5. Mark missing ablations as [TO BE CONDUCTED]

REQUIRED ABLATIONS (describe plan if not done):
1. **Component Ablations**: Remove each major component one by one
2. **Design Choice Ablations**: Alternative designs for each component
3. **Hyperparameter Sensitivity**: Vary key hyperparameters
4. **Architecture Variants**: Different architectural choices
5. **Training Procedure**: Ablate training techniques

For each ablation:
- Clear description of what is/will be changed
- Hypothesis about expected impact
- Results IF AVAILABLE (otherwise mark as planned)
- Insights IF RESULTS AVAILABLE

Format as:
\subsection{Ablation Studies}
\subsubsection{Component Ablations}
We systematically remove each component to understand its contribution:
[Table showing results IF AVAILABLE, otherwise describe experimental plan]

Analysis: [Only if results available]

\subsubsection{Hyperparameter Sensitivity}
[Analysis if conducted, otherwise experimental plan]

Write comprehensive ablations (NO FABRICATED RESULTS):
"""

        return await self.gpt_client.chat(prompt=prompt)

    async def add_theoretical_analysis(self, methodology: str) -> str:
        """Add theoretical analysis and complexity (hallucination-safe)"""

        prompt = f"""{ANTI_HALLUCINATION_PREAMBLE}

Add theoretical analysis to the methodology section.

CURRENT METHODOLOGY:
{methodology}

⚠️  CRITICAL RULES FOR THEORETICAL CLAIMS:
1. ONLY state theorems if mathematically proven
2. If proof not complete, use "conjecture" or "empirical observation"
3. Complexity analysis must be derived, not guessed
4. If convergence not proven, state as "empirically converges"
5. Mark unproven claims as [THEORETICAL ANALYSIS NEEDED]

ADD (only if provable from methodology):
1. **Theoretical Justification**: Why does this work? Mathematical intuition (grounded in methodology)
2. **Complexity Analysis**:
   - Time complexity: O(?) - DERIVE from algorithm, don't guess
   - Space complexity: O(?) - DERIVE from data structures
   - Comparison with baselines (only if their complexity known)
3. **Convergence Guarantees**: ONLY if mathematically proven
4. **Generalization Bounds**: ONLY if provable
5. **Theoretical Properties**: ONLY what can be rigorously proven

Use proper mathematical notation. If theorem not proven, use:
- "We conjecture that..."
- "Empirically, we observe that..."
- "Future work will formally prove..."

Example (conservative):
\subsection{Theoretical Analysis}
\subsubsection{Computational Complexity}
Our method has time complexity O(n log n) [ONLY IF DERIVED]...
If not derived, write: "The computational cost is dominated by [operation], which scales as O(?). Formal complexity analysis is future work."

\begin{theorem}
[ONLY IF YOU HAVE A PROOF]
\end{theorem}

Write the theoretical analysis (NEVER invent proofs):
"""

        return await self.gpt_client.chat(prompt=prompt)

    async def enhance_related_work(self, current_related_work: str, paper_collection: Optional[List[Dict]] = None) -> str:
        """Enhance related work section with critical analysis (hallucination-safe)"""

        prompt = f"""{ANTI_HALLUCINATION_PREAMBLE}

Enhance the related work section to NeurIPS quality.

CURRENT RELATED WORK:
{current_related_work}

PAPER COLLECTION (VERIFIED REFERENCES):
{paper_collection if paper_collection else "[NO VERIFIED REFERENCES - Only cite papers mentioned in current content]"}

⚠️  CRITICAL RULES FOR CITATIONS:
1. ONLY cite papers explicitly mentioned in CURRENT RELATED WORK or PAPER COLLECTION
2. NEVER invent paper titles, authors, or years
3. If you need to reference additional work, use [Citation Needed: area/topic]
4. Do NOT make up conference names or publication venues
5. If unsure about a citation detail, mark as [Verify: detail]

ENHANCEMENT GUIDELINES (without fabricating references):
1. **Reorganize existing citations** by themes
2. **Add critical analysis** to existing citations
3. **Clear Positioning**: Explicitly state how our work differs (based on actual papers)
4. **Comparison Table**: Use ONLY papers already cited
5. **If gaps in coverage**, mark as [Additional citations needed: topic]

Structure:
\section{Related Work}
\subsection{Theme 1}
[Critical analysis of papers ALREADY CITED]

Our approach differs in that...

\subsection{Theme 2}
[Critical analysis of EXISTING citations]

\subsection{Comparison with Our Work}
Table comparing ONLY with papers already referenced...

Note: If coverage insufficient, add section:
\textit{Note: Additional related work in [area] should be reviewed. See [Citation Needed: specific area]}

Write enhanced related work (NO FABRICATED CITATIONS):
"""

        return await self.gpt_client.chat(prompt=prompt)

    async def add_limitations_section(self, paper_content: str) -> str:
        """Add honest limitations and future work"""

        prompt = f"""Write a limitations section (required for NeurIPS).

PAPER CONTENT:
{paper_content}

GUIDELINES:
1. Be HONEST about limitations
2. Discuss:
   - Computational requirements
   - Datasets limitations
   - Theoretical gaps
   - Practical constraints
   - Failure cases
3. Suggest future work to address limitations

Example:
\section{Limitations and Future Work}
While our method achieves strong results, we acknowledge several limitations:

1. **Computational Cost**: Our approach requires X GPU hours...
2. **Dataset Scope**: We evaluate on Y datasets which may not...
3. **Theoretical Understanding**: While empirically effective, we lack...

Future work includes...

Write the limitations section:
"""

        return await self.gpt_client.chat(prompt=prompt)

    async def generate_quality_report(
        self,
        sections: Dict[str, str]
    ) -> str:
        """Generate comprehensive quality report"""

        score, report = await self.check_paper_quality(sections)

        report_text = f"""
=====================================
PAPER QUALITY REPORT
=====================================

Overall Score: {score:.2f}/1.00
Tier: {report['tier']}

DETAILED SCORES:
"""

        for aspect, details in report.items():
            if aspect not in ['overall_score', 'scores', 'tier']:
                report_text += f"\n{aspect.upper()}: {details['score']:.2f}/1.00\n"
                report_text += f"{details['feedback']}\n"

        report_text += f"\n\nRECOMMENDATIONS:\n"

        if score < 0.65:
            report_text += "⚠️  MAJOR REVISION NEEDED\n"
        elif score < 0.75:
            report_text += "⚠️  MINOR REVISION RECOMMENDED\n"
        elif score < 0.85:
            report_text += "✓  GOOD QUALITY - Minor improvements suggested\n"
        else:
            report_text += "✓✓  EXCELLENT QUALITY - Ready for submission\n"

        return report_text


class BaselineEnhancer:
    """Ensures strong baseline comparisons"""

    def __init__(self, gpt_model: str = "gpt-4o"):
        self.gpt_client = GPTClient(model=gpt_model)

    async def suggest_baselines(
        self,
        task: str,
        method_description: str,
        current_baselines: List[str]
    ) -> List[Dict[str, str]]:
        """Suggest strong SOTA baselines (hallucination-safe)"""

        prompt = f"""{ANTI_HALLUCINATION_PREAMBLE}

Suggest strong SOTA baselines for comparison.

TASK: {task}
OUR METHOD: {method_description}

CURRENT BASELINES:
{chr(10).join(f"- {b}" for b in current_baselines)}

⚠️  CRITICAL RULES FOR BASELINE SUGGESTIONS:
1. ONLY suggest well-known, verifiable baseline papers
2. If unsure about a paper's existence, mark as [Needs Verification]
3. Do NOT invent paper names or authors
4. For performance, use "expected to achieve ~X based on typical results" - be conservative
5. Only provide GitHub links if you're confident they exist (otherwise mark as [Check GitHub])

Suggest 5-8 STRONG baselines including:
1. Classic methods (foundational, well-established)
2. Recent SOTA (2023-2024, only if you know them)
3. Similar approaches (most relevant, verifiable)
4. Different paradigms (for comprehensive comparison)

For each baseline, provide:
- Name and reference (only if you're sure it exists)
- Why it's a strong comparison
- Expected performance (conservative estimate with uncertainty)
- Implementation availability (mark uncertain)

Output format:
BASELINE: [Name] (Year) [or mark as [Needs Literature Search: description]]
REFERENCE: [Paper citation if known, else [Citation To Be Found]]
REASON: [Why compare]
EXPECTED: [Conservative performance estimate with uncertainty]
CODE: [GitHub link if known, else [Code Availability Unknown]]

Be conservative - it's better to suggest fewer verified baselines than many potentially fake ones.

List baselines (NO FABRICATED PAPERS):
"""

        response = await self.gpt_client.chat(prompt=prompt)
        # Parse response to extract baselines
        return self._parse_baselines(response)

    def _parse_baselines(self, response: str) -> List[Dict]:
        """Parse baseline suggestions"""
        # Simple parsing - can be enhanced
        baselines = []
        current = {}

        for line in response.split('\n'):
            if line.startswith('BASELINE:'):
                if current:
                    baselines.append(current)
                current = {'name': line.split(':', 1)[1].strip()}
            elif line.startswith('REFERENCE:'):
                current['reference'] = line.split(':', 1)[1].strip()
            elif line.startswith('REASON:'):
                current['reason'] = line.split(':', 1)[1].strip()
            elif line.startswith('CODE:'):
                current['code'] = line.split(':', 1)[1].strip()

        if current:
            baselines.append(current)

        return baselines
