# 📚 AI-Researcher Kullanım Kılavuzu

> **Hızlı, kolay ve production-ready AI-destekli araştırma platformu**

---

## 📑 İçindekiler

1. [Hızlı Başlangıç](#hızlı-başlangıç)
2. [Kurulum Yöntemleri](#kurulum-yöntemleri)
3. [Temel Kullanım](#temel-kullanım)
4. [NeurIPS-Tier Paper Yazımı](#neurips-tier-paper-yazımı)
5. [İleri Seviye Kullanım](#ileri-seviye-kullanım)
6. [Makefile Komutları](#makefile-komutları)
7. [Sorun Giderme](#sorun-giderme)
8. [Sık Sorulan Sorular](#sık-sorulan-sorular)

---

## 🚀 Hızlı Başlangıç

### 🎨 En Kolay Yöntem: Web GUI (Terminal Bilgisi Gerektirmez!)

**Grafiksel arayüz tercih edenler için:**

```bash
# 1. Projeyi klonla
git clone https://github.com/HKUDS/AI-Researcher.git
cd AI-Researcher

# 2. Environment dosyasını hazırla
cp .env.example .env
nano .env  # API anahtarlarını ekle

# 3. Web GUI'yi başlat
make up
make webgui
```

**Tarayıcıda aç:** http://localhost:7860 🎉

**Web GUI Özellikleri:**
- ✅ **Görsel Arayüz** - Terminal bilgisi gerektirmez!
- ✅ **Kolay Konfigürasyon** - API anahtarları ve parametreleri UI'da ayarla
- ✅ **Task Seçimi** - Örnek tasklar veya kendi araştırmanı seç
- ✅ **Canlı Loglar** - Araştırma ilerlemesini gerçek zamanlı izle
- ✅ **Paper İndirme** - Oluşturulan paper'ları direkt indir
- ✅ **Modern Arayüz** - Gradio ile responsive tasarım

### 🖥️ Alternatif: Komut Satırı (İleri Kullanıcılar)

```bash
# 1. Projeyi klonla
git clone https://github.com/HKUDS/AI-Researcher.git
cd AI-Researcher

# 2. Environment dosyasını hazırla
cp .env.example .env
# .env dosyasını düzenle ve API anahtarlarını ekle

# 3. Her şeyi başlat!
make up

# 4. Health check
make health
```

**Tebrikler! 🎉** AI-Researcher çalışıyor.

- 🎨 **Web GUI:** http://localhost:7860
- 🏥 **Health API:** http://localhost:8000/health

---

## 🔧 Kurulum Yöntemleri

### Yöntem 1: Docker Compose (Önerilen - Production Ready)

**Gereksinimler:**
- Docker Desktop veya Docker Engine
- Docker Compose
- En az 8GB RAM
- (Opsiyonel) NVIDIA GPU + nvidia-docker

**Kurulum:**

```bash
# Repository'yi klonla
git clone https://github.com/HKUDS/AI-Researcher.git
cd AI-Researcher

# Environment yapılandır
cp .env.example .env
nano .env  # veya vim, code, vs.
```

**.env Dosyası Konfigürasyonu:**

```bash
# ================ LLM Configuration ================
# OpenRouter (Önerilen - birçok model destekler)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_BASE=https://openrouter.ai/api/v1

# Veya OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Veya Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Veya DeepSeek (Ucuz ve iyi!)
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com

# ================ Model Selection ================
# Completion model (ana işlemler için)
COMPLETION_MODEL=openrouter/google/gemini-2.5-pro-preview-05-20
# veya
# COMPLETION_MODEL=gpt-4o
# COMPLETION_MODEL=claude-3-5-sonnet-20241022
# COMPLETION_MODEL=deepseek/deepseek-chat

# Cheap model (basit işlemler için)
CHEEP_MODEL=openrouter/google/gemini-2.5-flash-preview-05-20

# ================ GPU Configuration ================
# GPU kullanımı (varsa)
GPUS='"device=0"'       # İlk GPU
# GPUS='"device=0,1"'   # İlk iki GPU
# GPUS='"all"'          # Tüm GPU'lar
# GPUS=None             # GPU yok

# ================ Task Configuration ================
CATEGORY=vq              # veya: gnn, reasoning, recommendation, diffu_flow
INSTANCE_ID=rotation_vq  # benchmark instance
TASK_LEVEL=task1         # task1 veya task2
MAX_ITER_TIMES=0

# ================ Performance Settings ================
# Redis cache (performans için)
REDIS_ENABLED=true
REDIS_HOST=redis
REDIS_PORT=6379

# Paper quality thresholds
QUALITY_THRESHOLD=0.75   # 0.75=Accept, 0.85=Spotlight
MAX_ITERATIONS=3         # Quality enhancement iterations
```

**Docker Compose ile Başlat:**

```bash
# Servisleri başlat
docker-compose up -d

# Logları izle
docker-compose logs -f

# Health check
curl http://localhost:8000/health

# Durdur
docker-compose down
```

### Yöntem 2: Makefile ile (En Kolay)

```bash
# Yardım - tüm komutları gör
make help

# Setup ve başlat
make setup
make start

# Research çalıştır
make run-research CATEGORY=vq INSTANCE=rotation_vq

# Paper yaz (NeurIPS-tier)
make run-enhanced-paper CATEGORY=vq INSTANCE=rotation_vq

# Health check
make health

# Logs
make logs
```

### Yöntem 3: run.sh Script (En Pratik)

```bash
# Executable yap
chmod +x run.sh

# Setup
./run.sh setup

# Başlat
./run.sh start

# Health check
./run.sh health

# Durdur
./run.sh stop

# Logs
./run.sh logs

# Temizle
./run.sh clean
```

### Yöntem 4: Manuel Python (Development)

```bash
# UV ile environment kur (hızlı!)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Environment oluştur
uv venv --python 3.11
source ./.venv/bin/activate

# Dependencies yükle
uv pip install -e .
playwright install

# Çalıştır
python research_agent/run_infer_plan.py \
  --instance_path benchmark/final/vq/rotation_vq.json \
  --container_name paper_eval \
  --task_level task1 \
  --model gpt-4o
```

---

## 📖 Temel Kullanım

### 🎨 Web GUI ile Kullanım (ÖNERİLEN!)

#### Başlatma

```bash
# Tüm servisleri başlat
make up

# Web GUI'yi aç
make webgui
```

**Tarayıcıda:** http://localhost:7860

#### Web GUI Kullanımı

![Web GUI Ana Ekran](./assets/webgui/image-20250606135137558.png)

**1. Environment Ayarları**

![Environment Config](./assets/webgui/image-20250606135325373.png)

Environment sekmesinde:
- ✅ **API Keys** - OpenRouter, OpenAI, Anthropic API anahtarları
- ✅ **Model Selection** - Completion ve cheap model seçimi
- ✅ **GPU Settings** - GPU konfigürasyonu
- ✅ **Task Settings** - Category, instance ID, task level

**2. Task Seçimi**

![Task Selection](./assets/webgui/image-20250606135507970.png)

- **Örnek Tasklar** - Hazır örneklerden seç:
  - Vector Quantization (VQ)
  - Graph Neural Networks (GNN)
  - Recommendation Systems
  - Diffusion & Flow Matching
  - Reasoning

- **Custom Task** - Kendi araştırmanı tanımla:
  - Category seç
  - Instance ID gir
  - Task level belirle (task1/task2)
  - Research idea yaz (Level 1)
  - Veya sadece papers ver (Level 2)

**3. Research Başlat**

1. Environment ayarlarını yapılandır
2. Task'ı seç veya custom task oluştur
3. "Start Research" butonuna bas
4. Canlı logları izle

**4. İlerlemeyi İzle**

Web GUI'de real-time:
- ✅ Log çıktıları
- ✅ Durum güncellemeleri
- ✅ Hata mesajları (varsa)
- ✅ Tamamlanma yüzdesi

**5. Paper İndir**

Research tamamlandığında:
- ✅ "Generate Paper" butonuna bas
- ✅ Paper oluşması için bekle
- ✅ "Download PDF" ile indir

#### Web GUI Komutları

```bash
# Web GUI başlat
make webgui

# Logları görüntüle
make webgui-logs

# Yeniden başlat
make webgui-restart

# Durdur
make webgui-stop
```

#### Remote Erişim

Sunucuda çalıştırıyorsanız:

```bash
# Sunucuda
make up
make webgui

# Local makinenizde browser'da aç:
http://your-server-ip:7860

# Veya SSH tunnel ile:
ssh -L 7860:localhost:7860 user@your-server
# Sonra local'de: http://localhost:7860
```

---

### 🖥️ Komut Satırı ile Kullanım

#### 1. Research Agent Çalıştırma

AI-Researcher iki seviyede çalışır:

#### **Level 1: Detaylı Fikir ile**

Kendi research fikriniz var, implement edilmesini istiyorsunuz:

```bash
# Makefile ile
make run-research \
  CATEGORY=vq \
  INSTANCE=rotation_vq \
  TASK_LEVEL=task1

# Veya doğrudan
python research_agent/run_infer_plan.py \
  --instance_path benchmark/final/vq/rotation_vq.json \
  --container_name paper_eval \
  --task_level task1 \
  --model gpt-4o \
  --workplace_name workplace \
  --cache_path cache \
  --port 12372
```

**İçerir:**
- ✅ Literature review
- ✅ Algorithm design
- ✅ Implementation
- ✅ Experiments
- ✅ Result analysis

#### **Level 2: Sadece Reference Papers ile**

Sadece paper'lar veriyorsunuz, AI kendi fikri üretiyor:

```bash
# Makefile ile
make run-research \
  CATEGORY=vq \
  INSTANCE=rotation_vq \
  TASK_LEVEL=task2

# Veya doğrudan
python research_agent/run_infer_idea.py \
  --instance_path benchmark/final/vq/rotation_vq.json \
  --container_name paper_eval \
  --model gpt-4o
```

**İçerir:**
- ✅ Reference paper analysis
- ✅ **Automatic idea generation**
- ✅ Implementation
- ✅ Experiments
- ✅ Result analysis

### 2. Paper Yazma

#### Standard Paper Writing

```bash
# Makefile ile
make run-paper CATEGORY=vq INSTANCE=rotation_vq

# Veya doğrudan
python paper_agent/writing.py \
  --research_field vq \
  --instance_id rotation_vq
```

**Çıktı:**
- 📄 Full-length academic paper
- 📊 Figures and tables
- 📚 References
- 📝 LaTeX source

---

## 🌟 NeurIPS-Tier Paper Yazımı

### Neden Enhanced Paper Writer?

Standard paper writer iyi, ama **Enhanced Paper Writer**:
- 🎯 **NeurIPS/ICML/ICLR standartlarında** paper üretir
- 📊 **Statistical significance** otomatik ekler
- 💪 **Strong baselines** ile compare eder
- 🔬 **Comprehensive ablations** yapar
- 🛡️ **Hallucination yapmaz** - fake results/citations üretmez!

### Kullanım

```bash
# En basit (Makefile ile)
make run-enhanced-paper CATEGORY=vq INSTANCE=rotation_vq

# Custom quality threshold ile
make run-enhanced-paper \
  CATEGORY=vq \
  INSTANCE=rotation_vq \
  QUALITY_THRESHOLD=0.85 \
  MAX_ITERATIONS=5

# Quality check
make check-paper-quality CATEGORY=vq INSTANCE=rotation_vq
```

### Quality Tiers

| Skor | Tier | Açıklama |
|------|------|----------|
| **0.85+** | 🌟 **NeurIPS Spotlight** | Top 5% - Outstanding paper |
| **0.75-0.84** | ✅ **NeurIPS Accept** | Top 20% - Strong paper |
| **0.65-0.74** | 📝 **Workshop/ICLR** | Good paper, needs minor improvements |
| **<0.65** | ⚠️ **Major Revision** | Significant improvements needed |

### Enhanced Paper Features

#### 1. **Statistical Significance** 📊

Otomatik ekler:
- P-values (t-test, Wilcoxon)
- Confidence intervals (95% CI)
- Effect sizes (Cohen's d)
- Multiple runs with different seeds
- Significance indicators (*, **, ***)

**Örnek çıktı:**
```latex
Method          | Accuracy        | F1-Score        | p-value
----------------|-----------------|-----------------|--------
Baseline 1      | 85.2 ± 0.3     | 0.652 ± 0.012  | -
Baseline 2      | 87.1 ± 0.4     | 0.678 ± 0.015  | -
Ours           | 89.3 ± 0.2***  | 0.712 ± 0.008***| <0.001
```

#### 2. **Strong Baselines** 💪

Otomatik öneriyor:
- Classic methods (foundational)
- Recent SOTA (2023-2024)
- Similar approaches
- Different paradigms

**Örnek:**
```python
Suggested Baselines for VQ-VAE:
1. VQ-VAE (van den Oord et al., 2017) - Classic
2. VQ-VAE-2 (Razavi et al., 2019) - Hierarchical
3. FSQ (Mentzer et al., 2023) - Recent SOTA
4. RQ-VAE (Lee et al., 2022) - Different paradigm
```

#### 3. **Comprehensive Ablations** 🔬

Otomatik generate eder:
- Component ablations (her component için)
- Design choice ablations
- Hyperparameter sensitivity
- Architecture variants

**Örnek:**
```latex
\subsection{Ablation Studies}

Component         | Accuracy | Δ
------------------|----------|----
Full Model        | 89.3     | -
- Rotation        | 85.1     | -4.2
- Rescaling       | 87.2     | -2.1
- Codebook Mgmt   | 86.5     | -2.8
```

#### 4. **Hallucination Prevention** 🛡️

**Problem:** LLM'ler fake results/citations/theorems üretebilir!

**Çözüm:** Strict validation rules:

```python
⚠️ ANTI-HALLUCINATION RULES:
1. NEVER fabricate experimental results
   ❌ "Achieves 94.7% accuracy" (data yoksa)
   ✅ "Achieves significant improvement (see Table 2)"

2. NEVER make up citations
   ❌ "As shown by Johnson et al. (2024)" (paper yoksa)
   ✅ "[Citation Needed: recent transformer work]"

3. NEVER claim unproven theorems
   ❌ "We prove that complexity is O(n)"
   ✅ "We conjecture that complexity is O(n) [REQUIRES PROOF]"

4. NEVER fabricate baselines
   ❌ Invents fake baseline results
   ✅ Uses only provided baseline data

5. GROUND ALL STATEMENTS
   ✅ Every number from actual experiments
   ✅ Every claim backed by results
```

**Otomatik Validation:**
```python
# Hallucination detection
warnings = validate_for_hallucination(
    content=generated_paper,
    allowed_numbers=experimental_results
)

# Checks:
✓ Unexpected numbers not in data
✓ Suspiciously precise results
✓ Generic citations ("Smith et al., 2024")
✓ Ungrounded claims
✓ Placeholder markers
```

#### 5. **Iterative Enhancement** 🔄

```python
# Enhancement loop
while quality_score < threshold and iteration < max_iterations:
    # 1. Check quality
    score, report = check_quality(paper)

    # 2. Identify weak sections
    weak_sections = find_weak_sections(report)

    # 3. Enhance sections
    for section in weak_sections:
        if section == "experiments":
            add_statistical_significance()
            enhance_ablations()
        elif section == "contributions":
            improve_clarity()
            add_evidence()
        elif section == "related_work":
            expand_coverage()
            add_critical_analysis()

    # 4. Re-check quality
    iteration += 1

# 5. Final enhancements
add_limitations_section()
add_reproducibility_statement()
add_broader_impact()
```

### Quality Report Örneği

```
=====================================
PAPER QUALITY REPORT
=====================================

Overall Score: 0.82/1.00
Tier: NeurIPS/ICML Accept (Top 20%)

DETAILED SCORES:
Contributions: 0.85/1.00
  ✓ Clear novelty statement
  ✓ Well-positioned vs prior work
  ⚠ Could strengthen impact discussion

Methodology: 0.78/1.00
  ✓ Mathematical rigor present
  ✓ Algorithm well-described
  ⚠ Missing complexity analysis

Experiments: 0.88/1.00
  ✓ Strong baselines
  ✓ Statistical significance
  ✓ Comprehensive ablations
  ✓ Multiple datasets

Related Work: 0.75/1.00
  ✓ Good coverage (18 papers)
  ⚠ Could add more critical analysis

Writing: 0.82/1.00
  ✓ Clear and concise
  ✓ Good flow
  ✓ Consistent notation

Ethics: 0.90/1.00
  ✓ Limitations discussed
  ✓ Reproducibility info
  ✓ Broader impact

RECOMMENDATIONS:
✓ GOOD QUALITY - Minor improvements suggested
- Add complexity analysis to methodology
- Strengthen contribution impact discussion
- Expand critical analysis in related work
```

---

## 🎯 İleri Seviye Kullanım

### Custom Benchmarks

Kendi benchmark'ınızı ekleyin:

```bash
# 1. Benchmark dosyası oluştur
mkdir -p benchmark/final/my_domain
nano benchmark/final/my_domain/my_task.json
```

```json
{
  "task_id": "my_task",
  "category": "my_domain",
  "description": "Task description",
  "idea": "Detailed implementation idea...",
  "reference_papers": [
    {
      "title": "Paper 1",
      "authors": ["Author 1", "Author 2"],
      "year": 2024,
      "abstract": "..."
    }
  ]
}
```

```bash
# 2. Çalıştır
make run-research CATEGORY=my_domain INSTANCE=my_task
```

### Multi-GPU Setup

```bash
# .env dosyasında
GPUS='"device=0,1,2,3"'  # 4 GPU kullan

# Veya docker-compose.yml'de
services:
  ai-researcher:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

### Custom Model Configuration

```bash
# .env dosyasında farklı provider'lar

# OpenRouter (çok model seçeneği)
OPENROUTER_API_KEY=...
COMPLETION_MODEL=openrouter/google/gemini-2.5-pro-preview-05-20
CHEEP_MODEL=openrouter/google/gemini-2.5-flash-preview-05-20

# DeepSeek (ucuz ve iyi!)
DEEPSEEK_API_KEY=...
COMPLETION_MODEL=deepseek/deepseek-chat
CHEEP_MODEL=deepseek/deepseek-chat

# OpenAI
OPENAI_API_KEY=...
COMPLETION_MODEL=gpt-4o
CHEEP_MODEL=gpt-4o-mini

# Anthropic
ANTHROPIC_API_KEY=...
COMPLETION_MODEL=claude-3-5-sonnet-20241022
CHEEP_MODEL=claude-3-5-haiku-20241022

# Local LLM (Ollama)
LLM_BASE_URL=http://localhost:11434
COMPLETION_MODEL=ollama/llama3.1:70b
CHEEP_MODEL=ollama/llama3.1:8b
```

### Parallel Research

Birden fazla research paralel çalıştır:

```bash
# Terminal 1
make run-research CATEGORY=vq INSTANCE=rotation_vq PORT=12372

# Terminal 2
make run-research CATEGORY=gnn INSTANCE=nodeformer PORT=12373

# Terminal 3
make run-research CATEGORY=recommendation INSTANCE=hgcl PORT=12374
```

### Monitoring ve Health Checks

```bash
# Health API endpoints
curl http://localhost:8000/health    # Full health check
curl http://localhost:8000/ready     # Readiness check
curl http://localhost:8000/ping      # Simple ping

# Metrics
curl http://localhost:8000/health | jq .
{
  "status": "healthy",
  "checks": {
    "api": true,
    "memory": true,
    "disk": true,
    "cpu": true,
    "redis": true
  },
  "metrics": {
    "memory_percent": 45.2,
    "disk_percent": 68.1,
    "cpu_percent": 23.5
  },
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

## 🛠️ Makefile Komutları

### Setup ve Management

```bash
make help                 # Tüm komutları göster
make setup               # İlk kurulum (build + env check)
make start               # Servisleri başlat
make stop                # Servisleri durdur
make restart             # Yeniden başlat
make clean               # Temizle (containers, volumes, cache)
make build               # Docker image build et
make rebuild             # Force rebuild
```

### Research Operations

```bash
make run-research        # Research agent çalıştır
  CATEGORY=vq           # Category seç
  INSTANCE=rotation_vq  # Instance seç
  TASK_LEVEL=task1     # Task level (task1/task2)
  MODEL=gpt-4o         # Model override

make run-paper          # Standard paper yaz
  CATEGORY=vq
  INSTANCE=rotation_vq

make run-enhanced-paper     # NeurIPS-tier paper yaz (önerilen!)
  CATEGORY=vq
  INSTANCE=rotation_vq
  QUALITY_THRESHOLD=0.75   # Quality threshold
  MAX_ITERATIONS=3         # Max enhancement iterations

make check-paper-quality    # Paper quality kontrolü
  CATEGORY=vq
  INSTANCE=rotation_vq
```

### Monitoring

```bash
make health              # Health check
make logs                # Logları göster
make logs-follow         # Logları takip et (real-time)
make ps                  # Running containers
make stats               # Resource usage stats
```

### Development

```bash
make shell               # Container shell aç
make test                # Testleri çalıştır
make lint                # Code quality check
make format              # Code formatting
```

### Examples

```bash
make example-vq          # VQ example çalıştır
make example-gnn         # GNN example çalıştır
make example-rec         # Recommendation example
make example-all         # Tüm examples (paralel)
```

---

## 🔍 Sorun Giderme

### Sık Karşılaşılan Sorunlar

#### 1. **Docker Container Başlamıyor**

**Semptom:**
```bash
Error: Cannot connect to the Docker daemon
```

**Çözüm:**
```bash
# Docker'ın çalıştığını kontrol et
sudo systemctl status docker

# Docker'ı başlat
sudo systemctl start docker

# User'ı docker grubuna ekle (sudo olmadan kullanmak için)
sudo usermod -aG docker $USER
newgrp docker
```

#### 2. **GPU Tanınmıyor**

**Semptom:**
```bash
docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]].
```

**Çözüm:**
```bash
# NVIDIA Docker runtime kur
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Test et
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

#### 3. **API Key Hatası**

**Semptom:**
```bash
Error: API key not configured
```

**Çözüm:**
```bash
# .env dosyasını kontrol et
cat .env | grep API_KEY

# API key ekle
nano .env
# OPENROUTER_API_KEY=your_actual_key_here

# Container'ı yeniden başlat
make restart
```

#### 4. **Port Conflict**

**Semptom:**
```bash
Error: Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Çözüm:**
```bash
# Portu kullanan process'i bul
sudo lsof -i :8000

# Process'i kapat veya .env'de portu değiştir
# PORT=8001

# Veya docker-compose.yml'de
ports:
  - "8001:8000"
```

#### 5. **Memory Hatası**

**Semptom:**
```bash
Error: Container killed (OOM)
```

**Çözüm:**
```bash
# Docker'a daha fazla memory ver
# Docker Desktop → Settings → Resources → Memory → 8GB+

# Veya docker-compose.yml'de limit artır
services:
  ai-researcher:
    deploy:
      resources:
        limits:
          memory: 8G
```

#### 6. **Redis Connection Hatası**

**Semptom:**
```bash
Error: Could not connect to Redis
```

**Çözüm:**
```bash
# Redis container'ının çalıştığını kontrol et
docker-compose ps

# Redis'i yeniden başlat
docker-compose restart redis

# Veya .env'de Redis'i devre dışı bırak
REDIS_ENABLED=false
```

### Debug Mode

```bash
# Verbose logging
export DEBUG=true
make run-research CATEGORY=vq INSTANCE=rotation_vq

# Container içinde debug
docker-compose exec ai-researcher bash
python -m pdb research_agent/run_infer_plan.py ...
```

### Log Analizi

```bash
# Tüm logları gör
make logs

# Son 100 satır
docker-compose logs --tail=100

# Specific service
docker-compose logs ai-researcher

# Real-time follow
docker-compose logs -f

# Grep ile filtrele
docker-compose logs | grep ERROR
```

---

## ❓ Sık Sorulan Sorular (FAQ)

### Genel

**Q: AI-Researcher ücretsiz mi?**
A: Evet, AI-Researcher açık kaynak ve ücretsiz. Sadece kullandığınız LLM API'leri için ödeme yaparsınız (OpenAI, Anthropic, vs.)

**Q: Hangi LLM provider'ı öneriyorsunuz?**
A:
- **En iyi kalite:** Claude 3.5 Sonnet (Anthropic) veya GPT-4o (OpenAI)
- **En ucuz:** DeepSeek Chat (çok iyi ve ucuz!)
- **En çok seçenek:** OpenRouter (100+ model)

**Q: GPU şart mı?**
A: Hayır, ama büyük experiments için önerilir. CPU ile de çalışır.

**Q: Kaç sürede paper yazılır?**
A: Complexity'e bağlı:
- Simple task: 2-4 saat
- Medium task: 6-12 saat
- Complex task: 24-48 saat

### Research

**Q: Level 1 ve Level 2 farkı nedir?**
A:
- **Level 1:** Fikir VERİYORSUNUZ → Implementation + Experiments
- **Level 2:** Sadece papers VERİYORSUNUZ → Idea generation + Implementation + Experiments

**Q: Kendi dataset'imi kullanabilir miyim?**
A: Evet! Benchmark format'ında JSON dosyası oluşturun.

**Q: Research durdurup devam edebilir miyim?**
A: Evet, `MAX_ITER_TIMES` ayarını kullanarak checkpoint'lerden devam edebilirsiniz.

### Paper Writing

**Q: Standard vs Enhanced paper writer farkı?**
A:
- **Standard:** Basic paper generation
- **Enhanced:** NeurIPS-tier quality + statistical significance + strong baselines + ablations + hallucination prevention

**Q: Enhanced paper writer için ekstra ücret var mı?**
A: Hayır, sadece daha fazla LLM API call yapıyor (daha fazla iteration).

**Q: Hallucination prevention nasıl çalışıyor?**
A: Her prompt'ta strict validation rules + otomatik number/citation checking + conservative language.

**Q: Paper'ı düzenleyebilir miyim?**
A: Evet! LaTeX source output'u düzenleyebilirsiniz.

### Web GUI

**Q: Web GUI vs Komut Satırı - Hangisini kullanmalıyım?**
A:
- **Web GUI:** Terminal bilgisi gerektirmez, görsel arayüz, başlangıç için ideal
- **Komut Satırı:** Otomasyon, scripting, ileri kullanıcılar için

**Q: Web GUI port'unu değiştirebilir miyim?**
A: Evet! `.env` dosyasında `WEBGUI_PORT=7860` değerini değiştirin.

**Q: Web GUI'ye uzaktan erişebilir miyim?**
A: Evet! İki yöntem:
1. Direkt: `http://server-ip:7860`
2. SSH tunnel: `ssh -L 7860:localhost:7860 user@server`

**Q: Web GUI çalışmıyor, ne yapmalıyım?**
A:
```bash
# Logları kontrol et
make webgui-logs

# Yeniden başlat
make webgui-restart

# Port kullanımda olabilir
sudo lsof -i :7860
```

**Q: Web GUI'de API key değiştirsem Docker restart gerekli mi?**
A: Hayır! Web GUI'de environment sekmesinden direkt değiştirebilirsiniz.

**Q: Web GUI ile birden fazla research paralel çalıştırabilir miyim?**
A: Şu an tek research destekleniyor. Paralel için komut satırını kullanın.

### Teknik

**Q: Hangi Python versiyonu?**
A: Python 3.11 (uv ile otomatik kurulur)

**Q: Windows'ta çalışır mı?**
A: Evet, Docker Desktop ile. WSL2 önerilir.

**Q: M1/M2 Mac destekliyor mu?**
A: Evet! Platform: linux/arm64 kullanın.

**Q: Redis neden gerekli?**
A: Caching için. Opsiyonel, ama performansı 2-3x artırır.

**Q: Proxy arkasında kullanabilir miyim?**
A: Evet, `HTTP_PROXY` ve `HTTPS_PROXY` environment variables ayarlayın.

---

## 📞 Destek ve Topluluk

### Yardım Alabileceğiniz Yerler

- 📖 **Dokümantasyon:** [https://autoresearcher.github.io/docs](https://autoresearcher.github.io/docs)
- 💬 **Slack:** [AI-Researcher Community](https://join.slack.com/t/ai-researchergroup/shared_invite/zt-30y5a070k-C0ajQt1zmVczFnfGkIicvA)
- 🎮 **Discord:** [Join Discord](https://discord.gg/zBNYTk5q2g)
- 🐛 **GitHub Issues:** [Report Issue](https://github.com/HKUDS/AI-Researcher/issues)
- 📧 **Email:** [Contact](mailto:jtang@connect.hku.hk)

### Katkıda Bulunma

```bash
# 1. Fork edin
# 2. Feature branch oluşturun
git checkout -b feature/amazing-feature

# 3. Commit edin
git commit -m "Add amazing feature"

# 4. Push edin
git push origin feature/amazing-feature

# 5. Pull Request açın
```

---

## 📚 Ek Kaynaklar

- 📄 **Paper:** [arXiv:2505.18705](https://arxiv.org/abs/2505.18705)
- 🌐 **Project Page:** [https://autoresearcher.github.io](https://autoresearcher.github.io)
- 📊 **Leaderboard:** [https://autoresearcher.github.io/leaderboard](https://autoresearcher.github.io/leaderboard)
- 📖 **Full Documentation:** [https://autoresearcher.github.io/docs](https://autoresearcher.github.io/docs)
- 🚀 **Quickstart:** [QUICKSTART.md](./QUICKSTART.md)
- 📝 **Paper Quality Guide:** [PAPER_IMPROVEMENTS.md](./PAPER_IMPROVEMENTS.md)
- 🛠️ **Production Setup:** [IMPROVEMENTS.md](./IMPROVEMENTS.md)

---

## 🎉 İyi Araştırmalar!

Sorularınız için:
- Slack/Discord topluluğumuza katılın
- GitHub issue açın
- Dokümantasyonu okuyun

**Happy Researching! 🚀**
