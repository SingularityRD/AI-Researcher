# 📄 NeurIPS-Tier Paper Quality Guidelines

## 🎯 Quality Standards

This guide ensures papers meet **NeurIPS/ICML/ICLR** standards.

### Quality Score Breakdown

| Score | Tier | Description |
|-------|------|-------------|
| **0.85+** | 🌟 **NeurIPS Spotlight** | Top 5% - Outstanding contribution |
| **0.75-0.84** | ✅ **NeurIPS Accept** | Top 20% - Strong paper |
| **0.65-0.74** | 📝 **Workshop/ICLR** | Good but needs improvement |
| **<0.65** | ⚠️ **Major Revision** | Significant issues |

---

## 📊 Quality Criteria (Weighted)

### 1. **Contributions (25%)**

**Required Elements:**
- ✅ Clear, numbered list of contributions
- ✅ Explicit novelty claims
- ✅ Comparison with prior work
- ✅ Significance and impact discussion

**Example (Good):**
```
Our key contributions are:

1. **Novel Architecture**: We propose XYZ, which unlike prior work [A,B],
   enables... This is the first approach to...

2. **Theoretical Analysis**: We prove that our method achieves O(n log n)
   complexity, improving upon O(n²) of [C]. This provides...

3. **Comprehensive Evaluation**: We demonstrate X% improvement over 8 SOTA
   baselines on 5 datasets, with statistical significance (p<0.001).

4. **Open-Source Release**: We release code, models, and data at [URL],
   enabling reproducibility and future research.
```

**Example (Bad):**
```
We propose a new method that works well.
```

---

### 2. **Methodology (20%)**

**Required Elements:**
- ✅ Theoretical justification
- ✅ Mathematical rigor (equations, theorems)
- ✅ Algorithm pseudo-code
- ✅ Complexity analysis
- ✅ Implementation details

**Best Practices:**

1. **Mathematical Notation**
   - Define all symbols clearly
   - Use consistent notation
   - Number important equations

2. **Algorithm Presentation**
   ```latex
   \begin{algorithm}
   \caption{Our Method}
   \begin{algorithmic}[1]
   \REQUIRE Input $x$, parameters $\theta$
   \ENSURE Output $y$
   \STATE $z \gets f_\theta(x)$  // Forward pass
   \STATE $\mathcal{L} \gets \text{Loss}(z, y)$  // Compute loss
   \RETURN $y$
   \end{algorithmic}
   \end{algorithm}
   ```

3. **Theoretical Analysis**
   ```latex
   \begin{theorem}
   Under assumptions $A_1, A_2$, our method converges to
   $\epsilon$-optimal solution in $O(\log(1/\epsilon))$ iterations.
   \end{theorem}

   \begin{proof}
   [Proof sketch or refer to appendix]
   \end{proof}
   ```

4. **Complexity**
   - Time: O(?)
   - Space: O(?)
   - Comparison with baselines

---

### 3. **Experiments (30%)** - Most Important!

**Required Elements:**
- ✅ Strong SOTA baselines (5-8 baselines)
- ✅ Multiple datasets (3+ datasets)
- ✅ Statistical significance
- ✅ Comprehensive ablations
- ✅ Hyperparameter sensitivity
- ✅ Runtime analysis
- ✅ Error analysis

#### 3.1 Baseline Selection

**Must Include:**
1. **Classic Methods** (2-3): Foundational approaches
2. **Recent SOTA** (3-4): Papers from 2023-2024
3. **Most Related** (2-3): Similar approaches
4. **Different Paradigms** (1-2): Alternative solutions

**Example:**
```latex
We compare against 8 baselines:
- Classic: MLP (1986), CNN (2012), ResNet (2016)
- Recent SOTA: Transformer-XL (2023), EfficientNet-v2 (2024)
- Similar: Method-A (2023), Method-B (2024)
- Alternative: RNN-based (2023)
```

#### 3.2 Statistical Significance

**Required:**
- Multiple runs (3-5) with different seeds
- Mean ± standard deviation
- Confidence intervals (95% CI)
- P-values vs. baselines
- Effect size (Cohen's d)

**Example Table:**
```latex
\begin{table}[t]
\caption{Main Results (mean ± std over 5 runs)}
\begin{tabular}{lcc}
\toprule
Method & Accuracy (\%) & F1-Score \\
\midrule
Baseline-1 & 85.2 $\pm$ 0.3 & 0.823 $\pm$ 0.008 \\
Baseline-2 & 87.1 $\pm$ 0.4 & 0.845 $\pm$ 0.012 \\
\textbf{Ours} & \textbf{89.3 $\pm$ 0.2}$^{***}$ & \textbf{0.876 $\pm$ 0.006}$^{***}$ \\
\bottomrule
\multicolumn{3}{l}{$^{***}$p<0.001 vs. best baseline (t-test)}
\end{tabular}
\end{table}
```

#### 3.3 Ablation Studies

**Must Ablate:**
1. **Each Component**: Remove one component at a time
2. **Design Choices**: Alternative designs for each component
3. **Hyperparameters**: Vary key hyperparameters
4. **Training Techniques**: Different training procedures

**Example:**
```latex
\subsection{Ablation Studies}

\subsubsection{Component Analysis}
To understand the contribution of each component, we systematically
remove them:

\begin{table}[h]
\caption{Component Ablations}
\begin{tabular}{lc}
\toprule
Configuration & Accuracy \\
\midrule
Full Model & 89.3 \\
- w/o Component A & 86.1 (-3.2) \\
- w/o Component B & 87.5 (-1.8) \\
- w/o Component C & 88.0 (-1.3) \\
\bottomrule
\end{tabular}
\end{table}

Analysis: Component A provides the largest improvement, suggesting...
```

#### 3.4 Hyperparameter Sensitivity

```latex
\subsubsection{Hyperparameter Sensitivity}

We analyze the impact of key hyperparameters:

\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{hyperparam_sensitivity.pdf}
\caption{Performance vs. hyperparameter $\alpha$. Our method is
robust across a wide range.}
\end{figure}
```

#### 3.5 Runtime & Memory

```latex
\subsubsection{Efficiency Analysis}

\begin{table}[h]
\caption{Runtime and Memory Comparison}
\begin{tabular}{lccc}
\toprule
Method & Time (s) & Memory (GB) & Accuracy \\
\midrule
Baseline & 120 & 4.2 & 87.1 \\
Ours & 95 (-21\%) & 3.8 (-10\%) & 89.3 \\
\bottomrule
\end{tabular}
\end{table}
```

---

### 4. **Related Work (10%)**

**Required Elements:**
- ✅ Comprehensive coverage (20-30 papers)
- ✅ Critical analysis (not just description)
- ✅ Clear positioning
- ✅ Comparison table

**Structure:**
```latex
\section{Related Work}

\subsection{Theme 1: Early Approaches}
Early work [1-5] focused on... However, these methods suffer from...

\subsection{Theme 2: Modern Approaches}
Recent advances [6-12] have addressed... While effective, they...

\subsection{Theme 3: Most Related Work}
Most related to our work are [13-18]...

\textbf{Our Positioning:} Unlike prior work, our approach uniquely
combines X and Y to achieve Z. Table~\ref{tab:comparison} summarizes
key differences.

\begin{table}
\caption{Comparison with Related Work}
\begin{tabular}{lcccc}
\toprule
Method & Feature A & Feature B & Feature C & Performance \\
\midrule
Method-1 & ✓ & ✗ & ✗ & 85.2 \\
Method-2 & ✓ & ✓ & ✗ & 87.1 \\
\textbf{Ours} & ✓ & ✓ & ✓ & \textbf{89.3} \\
\bottomrule
\end{tabular}
\end{table}
```

---

### 5. **Writing Quality (10%)**

**Best Practices:**

1. **Structure**
   - Logical flow
   - Clear section transitions
   - Consistent formatting

2. **Clarity**
   - Short sentences (< 25 words)
   - Active voice
   - Define technical terms

3. **Figures**
   - High-quality, vector graphics
   - Clear labels and legends
   - Referenced in text

4. **Tables**
   - Booktabs style
   - Clear headers
   - Aligned numbers

5. **Citations**
   - Consistent format
   - Recent papers (2023-2024)
   - Proper attribution

---

### 6. **Ethics & Reproducibility (5%)**

**Required Sections:**

#### 6.1 Limitations
```latex
\section{Limitations}

While our method achieves strong results, we acknowledge:

1. \textbf{Computational Cost}: Training requires 100 GPU hours
   on V100, which may limit accessibility.

2. \textbf{Dataset Scope}: Evaluated on 3 datasets which may not
   generalize to all domains.

3. \textbf{Theoretical Gaps}: Convergence guarantees hold only
   under assumptions X, Y.

Future work includes addressing these limitations by...
```

#### 6.2 Reproducibility Statement
```latex
\section*{Reproducibility}

To ensure reproducibility:
- Code: github.com/user/project
- Data: All public datasets with preprocessing scripts
- Environment: requirements.txt with exact versions
- Seeds: Fixed at 42, 123, 456
- Hardware: 4x V100 GPUs
- Runtime: ~8 hours per dataset
```

#### 6.3 Broader Impact
```latex
\section*{Broader Impact}

Positive impacts include... However, potential misuse could...
We recommend safeguards such as...
```

---

## 🎓 Top-Tier Conference Specific Requirements

### NeurIPS
- ✅ Limitations section (mandatory)
- ✅ Broader impact (if applicable)
- ✅ Reproducibility checklist
- ✅ 9 pages + unlimited references
- ✅ Code/data submission encouraged

### ICML
- ✅ Impact statement
- ✅ Reproducibility section
- ✅ 8 pages + unlimited references
- ✅ Social impact discussion

### ICLR
- ✅ Reproducibility statement
- ✅ Ethics statement
- ✅ 9 pages + unlimited references
- ✅ OpenReview public discussion

---

## 📝 Review Criteria (What Reviewers Check)

### Novelty (30%)
- Is the approach truly novel?
- Clear difference from prior work?
- Significant enough contribution?

### Technical Quality (30%)
- Mathematically sound?
- Proper experimental design?
- Statistical rigor?

### Clarity (20%)
- Well written?
- Clear presentation?
- Good figures/tables?

### Empirical Strength (20%)
- Strong baselines?
- Multiple datasets?
- Comprehensive ablations?
- Significant improvements?

---

## ✅ Pre-Submission Checklist

### Content
- [ ] Clear contributions (numbered list)
- [ ] 5+ strong baselines
- [ ] 3+ datasets
- [ ] Statistical significance (p-values)
- [ ] Comprehensive ablations
- [ ] Hyperparameter sensitivity
- [ ] Runtime/memory analysis
- [ ] 20+ related work citations
- [ ] Comparison table with prior work
- [ ] Limitations section
- [ ] Reproducibility statement

### Quality
- [ ] All equations numbered and explained
- [ ] All symbols defined
- [ ] Consistent notation
- [ ] Algorithm pseudo-code
- [ ] Complexity analysis
- [ ] High-quality figures (vector)
- [ ] Professional tables (booktabs)
- [ ] No grammar/spelling errors

### Reproducibility
- [ ] Code availability statement
- [ ] Dataset information
- [ ] Hyperparameters listed
- [ ] Random seeds specified
- [ ] Hardware details
- [ ] Runtime estimates
- [ ] Requirements file

### Ethics
- [ ] Limitations discussed honestly
- [ ] Broader impact considered
- [ ] No ethical concerns
- [ ] Data usage proper
- [ ] Potential misuse addressed

---

## 🚀 Using Enhanced Paper Writer

### Basic Usage
```bash
# Use enhanced writer for NeurIPS-tier quality
python paper_agent/enhanced_writing.py \
  --research_field vq \
  --instance_id rotation_vq \
  --quality_threshold 0.75 \
  --max_iterations 3
```

### Quality Thresholds
- `0.85`: Aim for Spotlight (top 5%)
- `0.75`: Aim for Accept (top 20%)
- `0.65`: Workshop quality

### Makefile Commands
```bash
# Enhanced paper writing
make run-enhanced-paper CATEGORY=vq INSTANCE=rotation_vq

# With custom quality threshold
make run-enhanced-paper CATEGORY=vq INSTANCE=rotation_vq QUALITY=0.85
```

---

## 📊 Quality Report Example

```
=====================================
PAPER QUALITY REPORT
=====================================

Overall Score: 0.82/1.00
Tier: NeurIPS/ICML Accept (Top 20%)

DETAILED SCORES:

CONTRIBUTIONS: 0.85/1.00
✓ Clear numbered list
✓ Explicit novelty
⚠ Could strengthen impact discussion

METHODOLOGY: 0.78/1.00
✓ Good mathematical rigor
✓ Algorithm provided
⚠ Missing complexity analysis

EXPERIMENTS: 0.88/1.00
✓ Strong baselines (8)
✓ Multiple datasets (5)
✓ Statistical significance
✓ Comprehensive ablations
✓ Excellent coverage

RELATED_WORK: 0.75/1.00
✓ Good coverage (25 papers)
⚠ Could add comparison table

WRITING: 0.82/1.00
✓ Clear and concise
✓ Good figures
✓ Professional tables

ETHICS: 0.90/1.00
✓ Limitations discussed
✓ Reproducibility complete
✓ Impact considered

RECOMMENDATIONS:
✓ GOOD QUALITY - Minor improvements suggested

Suggestions:
1. Add complexity analysis to methodology
2. Include comparison table in related work
3. Strengthen broader impact discussion
```

---

## 📚 Resources

### Paper Examples
- NeurIPS 2024 Spotlight papers
- ICML 2024 Outstanding papers
- ICLR 2024 Oral presentations

### Tools
- Enhanced Paper Writer (this repo)
- Grammarly for grammar
- Overleaf for LaTeX
- Papers with Code for baselines

### Guidelines
- [NeurIPS Author Guidelines](https://neurips.cc/Conferences/2024/PaperInformation/AuthorGuidelines)
- [ICML Reviewer Guidelines](https://icml.cc/Conferences/2024/ReviewerGuidelines)
- [ICLR Review Criteria](https://iclr.cc/Conferences/2024/ReviewerGuide)

---

**Happy Writing! Aim for NeurIPS Spotlight! 🌟**
