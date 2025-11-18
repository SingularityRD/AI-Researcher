# 🚀 AI-Researcher Kurulum Kılavuzu (Türkçe)

## 📋 İçindekiler

- [Hızlı Başlangıç](#hızlı-başlangıç)
- [Detaylı Kurulum](#detaylı-kurulum)
- [API Yapılandırması](#api-yapılandırması)
- [Kullanım Örnekleri](#kullanım-örnekleri)
- [Sorun Giderme](#sorun-giderme)

---

## 🎯 Hızlı Başlangıç (5 Dakika)

### Otomatik Kurulum (Önerilen)

```bash
# 1. Projeyi klonlayın
git clone https://github.com/HKUDS/AI-Researcher.git
cd AI-Researcher

# 2. Kurulum sihirbazını çalıştırın
python setup_wizard.py

# 3. Servisleri başlatın
make up

# 4. Web arayüzünü açın
make webgui
```

**Tarayıcınızda açın:** http://localhost:7860 🎉

---

## 📦 Detaylı Kurulum

### Gereksinimler

- **Python 3.11+** (yerel geliştirme için)
- **Docker** ve **Docker Compose** (önerilen)
- **Git** (versiyon kontrolü için)
- **NVIDIA GPU** (opsiyonel, hızlandırma için)

### Adım 1: Projeyi İndirin

```bash
git clone https://github.com/HKUDS/AI-Researcher.git
cd AI-Researcher
```

### Adım 2: Environment Dosyası Oluşturun

#### Seçenek A: Otomatik (Önerilen)

```bash
python setup_wizard.py
```

Sihirbaz size şunları soracak:
- ✅ Hangi AI API'sini kullanmak istiyorsunuz?
- ✅ API anahtarınız nedir?
- ✅ GPU kullanacak mısınız?
- ✅ Proxy gerekli mi?

#### Seçenek B: Manuel

```bash
# .env.example dosyasını kopyalayın
cp .env.example .env

# Favori editörünüzle açın
nano .env  # veya vim, code, vb.
```

**Minimum Yapılandırma:**

```bash
# En az BİR API anahtarı ayarlayın:
ZAI_API_KEY=your_actual_api_key_here

# Model seçin
COMPLETION_MODEL=glm-4.6
CHEEP_MODEL=glm-4-flashx

# Kategori ve instance
CATEGORY=vq
INSTANCE_ID=one_layer_vq
```

### Adım 3: Servisleri Başlatın

```bash
# Docker ile (önerilen)
make up

# Alternatif: Docker Compose doğrudan
docker-compose up -d
```

### Adım 4: Sistemi Doğrulayın

```bash
# Sistem sağlığını kontrol edin
make health

# Logları görüntüleyin
make logs

# API anahtarlarını doğrulayın
python -c "from utils.secrets_manager import get_secrets; get_secrets().validate_all_required_secrets()"
```

---

## 🔑 API Yapılandırması

### Z.AI API (Önerilen - Türkçe desteği)

Z.AI, GLM-4.6 modeli ile mükemmel Türkçe desteği sunar.

```bash
# 1. API anahtarı alın: https://api.z.ai/
# 2. .env dosyasına ekleyin:

ZAI_API_KEY=your_actual_key
ZAI_API_BASE=https://api.z.ai/api/paas/v4
COMPLETION_MODEL=glm-4.6
CHEEP_MODEL=glm-4-flashx
```

**Test edin:**

```bash
curl --location 'https://api.z.ai/api/paas/v4/chat/completions' \
--header 'Authorization: Bearer YOUR_API_KEY' \
--header 'Content-Type: application/json' \
--data '{
  "model": "glm-4.6",
  "messages": [
    {
      "role": "user",
      "content": "Merhaba, nasılsın?"
    }
  ]
}'
```

### OpenRouter (Çoklu Model Desteği)

100+ model ile tek API anahtarı:

```bash
OPENROUTER_API_KEY=your_actual_key
OPENROUTER_API_BASE=https://openrouter.ai/api/v1
COMPLETION_MODEL=openrouter/google/gemini-2.5-pro-preview-05-20
```

**Desteklenen modeller:**
- Google Gemini 2.5 Pro/Flash
- Anthropic Claude 3.5 Sonnet/Opus
- OpenAI GPT-4o, GPT-4o-mini
- Meta Llama 3.3
- ve 100+ daha fazla...

### OpenAI

```bash
OPENAI_API_KEY=sk-your-key-here
COMPLETION_MODEL=gpt-4o-2024-08-06
CHEEP_MODEL=gpt-4o-mini
```

### Anthropic Claude

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
COMPLETION_MODEL=claude-3-5-sonnet-20241022
CHEEP_MODEL=claude-3-5-haiku-20241022
```

### DeepSeek

```bash
DEEPSEEK_API_KEY=your_actual_key
COMPLETION_MODEL=deepseek-chat
CHEEP_MODEL=deepseek-chat
```

---

## 🖥️ Kullanım Örnekleri

### Web Arayüzü (En Kolay)

```bash
# 1. Servisleri başlatın
make up

# 2. Web GUI'yi başlatın
make webgui

# 3. Tarayıcıda açın: http://localhost:7860
```

**Web GUI Özellikleri:**
- ✅ Sürükle-bırak arayüzü
- ✅ Gerçek zamanlı loglar
- ✅ Örnek şablonlar
- ✅ PDF indirme
- ✅ Environment değişken yönetimi

### Komut Satırı

#### Araştırma Ajanı Çalıştırma

```bash
# Task 1: Detaylı fikir açıklaması
make run-research CATEGORY=vq INSTANCE=rotation_vq

# Task 2: Referans tabanlı fikir üretimi
make run-research CATEGORY=gnn INSTANCE=gnn_nodeformer TASK_LEVEL=task2
```

#### Makale Üretimi

```bash
# Standart makale
make run-paper CATEGORY=vq INSTANCE=rotation_vq

# NeurIPS kalitesinde makale (önerilen!)
make run-enhanced-paper CATEGORY=vq INSTANCE=rotation_vq

# Makale kalitesini kontrol et
make check-paper-quality CATEGORY=vq INSTANCE=rotation_vq
```

### Python API

```python
from research_agent import run_research
from paper_agent import generate_paper

# Araştırma yap
results = run_research(
    category='vq',
    instance_id='rotation_vq',
    task_level='task1'
)

# Makale oluştur
paper = generate_paper(
    research_field='vq',
    instance_id='rotation_vq',
    enhanced=True  # NeurIPS-tier quality
)
```

---

## 🎨 Örnek Kullanım Senaryoları

### Senaryo 1: Vector Quantization Araştırması

```bash
# 1. Servisleri başlat
make up

# 2. Araştırma yap
make run-research CATEGORY=vq INSTANCE=rotation_vq

# 3. Makale oluştur
make run-enhanced-paper CATEGORY=vq INSTANCE=rotation_vq

# 4. Sonuçları kontrol et
ls -la vq/target_sections/rotation_vq/
```

### Senaryo 2: Graph Neural Network Projesi

```bash
# Web GUI kullan (daha kolay)
make webgui

# Tarayıcıda:
# 1. "Reference-Based Ideation" modunu seç
# 2. Kategori: gnn
# 3. Referans makalelerini ekle
# 4. "Run" butonuna bas
# 5. Makale PDF'ini indir
```

### Senaryo 3: Kendi Projeniz

```bash
# 1. Yeni kategori oluşturun
mkdir -p benchmark/final/my_category

# 2. Benchmark JSON'ı oluşturun
cat > benchmark/final/my_category/my_project.json << 'EOF'
{
  "task_description": "Proje açıklamanız...",
  "reference_papers": [
    {
      "title": "Referans makale 1",
      "url": "https://arxiv.org/abs/..."
    }
  ]
}
EOF

# 3. Çalıştırın
CATEGORY=my_category INSTANCE_ID=my_project make run-research
```

---

## 🐛 Sorun Giderme

### Sık Karşılaşılan Hatalar

#### 1. "API key not found"

**Sorun:** API anahtarı .env dosyasında yok

**Çözüm:**
```bash
# Setup wizard'ı tekrar çalıştır
python setup_wizard.py

# VEYA manuel olarak .env'yi düzenle
nano .env
# ZAI_API_KEY=your_actual_key ekle
```

#### 2. "Port already in use"

**Sorun:** 7860 veya 7020 portu kullanımda

**Çözüm:**
```bash
# Çalışan servisleri durdur
make down

# VEYA farklı port kullan
# .env dosyasında:
WEBGUI_PORT=7861
PORT=7021
```

#### 3. "Docker permission denied"

**Sorun:** Docker'a erişim yok

**Çözüm:**
```bash
# Kullanıcıyı docker grubuna ekle
sudo usermod -aG docker $USER

# Oturumu yeniden başlat
newgrp docker
```

#### 4. "CUDA out of memory"

**Sorun:** GPU belleği yetersiz

**Çözüm:**
```bash
# .env dosyasında CPU kullan:
GPUS=None

# VEYA daha küçük batch size kullan
```

#### 5. "Model not found"

**Sorun:** Geçersiz model adı

**Çözüm:**
```bash
# Z.AI için:
COMPLETION_MODEL=glm-4.6

# OpenRouter için:
COMPLETION_MODEL=openrouter/google/gemini-2.5-pro-preview-05-20

# Model listesi: .env.example dosyasına bakın
```

### Detaylı Logging

```bash
# Debug modunu aç (.env dosyasında)
DEBUG=true

# Logları izle
make logs

# VEYA spesifik servis logları
docker logs ai-researcher-webgui -f
docker logs ai-researcher-main -f
```

### Sistem Sağlığı Kontrolü

```bash
# Tüm servislerin durumunu kontrol et
make health

# Çıktı:
# ✅ ai-researcher-webgui - healthy
# ✅ ai-researcher-main - healthy
# ✅ ai-researcher-redis - healthy
```

### API Anahtarı Doğrulama

```bash
# Python ile doğrula
python -c "
from utils.secrets_manager import get_secrets
secrets = get_secrets()
results = secrets.validate_all_required_secrets()
for provider, valid in results.items():
    print(f'{'✅' if valid else '❌'} {provider}')
"
```

---

## 🔧 Gelişmiş Yapılandırma

### GPU Yapılandırması

```bash
# Tek GPU
GPUS='"device=0"'

# Çoklu GPU
GPUS='"device=0,1,2,3"'

# Tüm GPU'lar
GPUS='"all"'

# GPU yok (CPU)
GPUS=None
```

### Proxy Yapılandırması

```bash
# .env dosyasında:
HTTPS_PROXY=http://your-proxy:port
HTTP_PROXY=http://your-proxy:port
NO_PROXY=localhost,127.0.0.1,0.0.0.0
```

### Performans Ayarları

```bash
# Worker sayısı
MAX_WORKERS=8

# Timeout (saniye)
TIMEOUT=600

# Retry denemeleri
RETRY_ATTEMPTS=5

# Rate limiting
RATE_LIMIT_REQUESTS=200
RATE_LIMIT_PERIOD=60
```

---

## 📚 Ek Kaynaklar

### Dokümantasyon

- **README.md** - Ana dokümantasyon
- **QUICKSTART.md** - Hızlı başlangıç
- **PAPER_IMPROVEMENTS.md** - Makale kalitesi iyileştirmeleri
- **IMPROVEMENTS.md** - Altyapı iyileştirmeleri

### Topluluk

- **Slack:** https://join.slack.com/t/ai-researchergroup/shared_invite/...
- **Discord:** https://discord.gg/zBNYTk5q2g
- **GitHub Issues:** https://github.com/HKUDS/AI-Researcher/issues

### API Dokümantasyonu

- **Z.AI:** https://api.z.ai/docs
- **OpenRouter:** https://openrouter.ai/docs
- **OpenAI:** https://platform.openai.com/docs
- **Anthropic:** https://docs.anthropic.com/
- **DeepSeek:** https://platform.deepseek.com/docs

---

## 🆘 Yardım Almak

### Önce Buraya Bakın

1. Bu rehberi baştan sona okuyun
2. Sorun Giderme bölümünü kontrol edin
3. `make help` komutunu çalıştırın
4. Logları inceleyin: `make logs`

### Hala Sorun mu Var?

1. **GitHub Issue Açın:**
   - https://github.com/HKUDS/AI-Researcher/issues
   - Sorununuzu detaylı açıklayın
   - Log dosyalarını ekleyin
   - .env dosyanızı ASLA paylaşmayın!

2. **Topluluktan Yardım:**
   - Slack/Discord kanallarına katılın
   - Sorunuzu sorun
   - Deneyimlerinizi paylaşın

3. **E-posta:**
   - Kritik sorunlar için
   - API anahtarlarını ASLA e-postayla göndermeyin!

---

## 💡 İpuçları ve En İyi Uygulamalar

### Güvenlik

- ✅ .env dosyasını ASLA git'e commit etmeyin
- ✅ API anahtarlarını düzenli olarak yenileyin
- ✅ Production ve development için farklı anahtarlar kullanın
- ✅ API kullanımınızı izleyin
- ✅ Rate limit'leri ayarlayın

### Performans

- ✅ GPU kullanın (varsa)
- ✅ Ucuz görevler için CHEEP_MODEL kullanın
- ✅ Docker volume'ları kullanarak cache'leyin
- ✅ Worker sayısını CPU çekirdek sayınıza göre ayarlayın

### Maliyet Optimizasyonu

- ✅ Z.AI veya DeepSeek gibi uygun maliyetli sağlayıcılar kullanın
- ✅ Flash/Mini modelleri quick task'ler için kullanın
- ✅ Batch işlemleri yapın
- ✅ Sonuçları cache'leyin

---

## 🎉 Başarılı Kurulum!

Artık AI-Researcher'ı kullanmaya hazırsınız!

```bash
# Başlayın:
make webgui

# ve http://localhost:7860 adresini ziyaret edin!
```

**İyi araştırmalar! 🚀**

---

**Son Güncellenme:** 18 Kasım 2025
**Versiyon:** 2.0 (Production-Ready)
**Hazırlayan:** AI-Researcher Team
