# 🚀 AI-Researcher Quick Start Guide

Get up and running with AI-Researcher in **5 minutes**!

## 📋 Prerequisites

- Docker & Docker Compose installed
- **GPU (recommended but not required)** - CPU-only mode supported
- At least 8GB RAM (16GB recommended)
- 20GB free disk space
- API Key from one of:
  - [OpenRouter](https://openrouter.ai/keys) (Recommended - supports 100+ models)
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Anthropic Claude](https://console.anthropic.com/)

---

## ⚡ Quick Start (3 Steps)

### Step 1: Setup Environment

```bash
# Clone the repository (if not already)
git clone https://github.com/HKUDS/AI-Researcher.git
cd AI-Researcher

# Copy environment template
cp .env.example .env

# Edit .env and add your API key
nano .env  # or vim, code, etc.
```

**Minimum required in `.env`:**
```bash
OPENROUTER_API_KEY=your_key_here
COMPLETION_MODEL=openrouter/google/gemini-2.5-pro-preview-05-20
CHEEP_MODEL=openrouter/google/gemini-2.5-flash-preview-05-20
```

### Step 2: Start Services

```bash
# Build and start all services
make up

# Or without Makefile:
docker-compose up -d
```

Wait ~30 seconds for services to initialize, then check health:

```bash
make health

# You should see: "status": "healthy"
```

### Step 3: Run Your First Research

**Option A: Vector Quantization Example**
```bash
make example-vq
```

**Option B: Graph Neural Network Example**
```bash
make example-gnn
```

**Option C: Custom Task**
```bash
make run-task1 CATEGORY=vq INSTANCE=rotation_vq
```

That's it! 🎉

---

## 📊 Monitor Progress

**View logs in real-time:**
```bash
make logs
```

**Check container status:**
```bash
make status
```

**Check service health:**
```bash
make health
```

---

## 🎯 Usage Examples

### Level 1: With Your Own Idea

Create a JSON file with your research idea:

```json
{
  "instance_id": "my_research",
  "task1": "Your detailed research idea here...",
  "source_papers": [
    {"reference": "Paper Title 1"},
    {"reference": "Paper Title 2"}
  ]
}
```

Run:
```bash
make run-task1 CATEGORY=vq INSTANCE=my_research
```

### Level 2: AI Generates Idea

Just provide papers, AI will generate the research idea:

```bash
make run-task2 CATEGORY=vq INSTANCE=one_layer_vq
```

### Generate Paper

After research is complete:

```bash
make run-paper CATEGORY=vq INSTANCE=rotation_vq
```

Output: `{category}/target_sections/{instance_id}/iclr2025_conference.pdf`

---

## 🗂️ Available Categories & Examples

### Vector Quantization (VQ)
```bash
# Available instances: one_layer_vq, rotation_vq, fsq
make run-task1 CATEGORY=vq INSTANCE=one_layer_vq
```

### Graph Neural Networks (GNN)
```bash
# Available instances: gnn_nodeformer, gnn_difformer
make run-task1 CATEGORY=gnn INSTANCE=gnn_nodeformer
```

### Recommendation Systems
```bash
# Available instances: hgcl, dccf
make run-task1 CATEGORY=recommendation INSTANCE=hgcl
```

### Diffusion & Flow Matching
```bash
# Available instances: con_flowmatching
make run-task1 CATEGORY=diffu_flow INSTANCE=con_flowmatching
```

### Reasoning
```bash
# Available instances: check benchmark/final/reasoning/
make run-task1 CATEGORY=reasoning INSTANCE=your_instance
```

---

## 🔧 Configuration Options

### GPU Configuration

**Use specific GPU:**
```bash
# In .env:
GPUS='"device=0"'      # Use GPU 0
GPUS='"device=0,1"'    # Use GPU 0 and 1
GPUS='"all"'           # Use all GPUs
GPUS=None              # CPU only
```

### Model Selection

**Using OpenRouter (Recommended):**
```bash
COMPLETION_MODEL=openrouter/google/gemini-2.5-pro-preview-05-20
CHEEP_MODEL=openrouter/google/gemini-2.5-flash-preview-05-20
```

**Using OpenAI directly:**
```bash
COMPLETION_MODEL=openai/gpt-4o-2024-08-06
CHEEP_MODEL=openai/gpt-4o-mini
OPENAI_API_KEY=your_key
```

**Using Anthropic Claude:**
```bash
COMPLETION_MODEL=anthropic/claude-3-5-sonnet-20241022
CHEEP_MODEL=anthropic/claude-3-5-haiku-20241022
ANTHROPIC_API_KEY=your_key
```

### Iteration Control

```bash
# In .env:
MAX_ITER_TIMES=0   # No refinement iterations (faster)
MAX_ITER_TIMES=3   # 3 refinement iterations (better quality)
```

---

## 🛠️ Useful Commands

```bash
# Start services
make up

# Stop services
make down

# Restart services
make restart

# View logs
make logs

# Open shell in container
make shell

# Clean up
make clean

# Full rebuild
make rebuild

# Check health
make health

# Create backup
make backup

# See all commands
make help
```

---

## 📂 Output Locations

- **Workspace:** `./workplace_paper/task_{instance_id}/`
- **Project Code:** `./workplace_paper/task_{instance_id}/workplace/project/`
- **Logs:** `./logs/`
- **Cache:** `./cache/`
- **Generated Paper:** `./{category}/target_sections/{instance_id}/iclr2025_conference.pdf`

---

## 🐛 Troubleshooting

### Service won't start
```bash
# Check if .env exists
ls -la .env

# Check if API keys are set
cat .env | grep API_KEY

# Check Docker logs
make logs
```

### Out of Memory
```bash
# In docker-compose.yml, adjust:
memory: 16G  # Increase this value
```

### Container fails health check
```bash
# Check health details
curl http://localhost:7020/health | jq

# Check container status
docker ps -a

# Restart services
make restart
```

### GPU not detected
```bash
# Check NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# If fails, install nvidia-container-toolkit
```

### Permission denied errors
```bash
# Fix ownership
sudo chown -R $USER:$USER workplace_paper cache logs

# Or run as root
make shell-root
```

---

## 🔒 Security Notes

1. **Never commit `.env` file** - Contains API keys
2. **Use `.env.example`** - For sharing configuration templates
3. **Rotate API keys** - Regularly update your keys
4. **Monitor usage** - Check API usage dashboards
5. **Use rate limits** - Set appropriate limits in `.env`

---

## 💡 Best Practices

### For Production Use

1. **Enable monitoring:**
   ```bash
   # Uncomment Prometheus/Grafana in docker-compose.yml
   # Access Grafana at http://localhost:3000
   ```

2. **Set up backups:**
   ```bash
   # Automated backup (add to crontab)
   0 2 * * * cd /path/to/AI-Researcher && make backup
   ```

3. **Use appropriate models:**
   - COMPLETION_MODEL: Strong model for main research
   - CHEEP_MODEL: Fast model for auxiliary tasks

4. **Enable refinement:**
   ```bash
   MAX_ITER_TIMES=3  # Better quality results
   ```

### Cost Optimization

1. **Use cheaper models for non-critical tasks:**
   ```bash
   CHEEP_MODEL=openrouter/google/gemini-2.5-flash-preview-05-20
   ```

2. **Cache aggressively:**
   - Cache is enabled by default
   - Reuses previous results

3. **Start with CPU-only:**
   ```bash
   GPUS=None  # Save GPU costs initially
   ```

---

## 📚 Next Steps

1. **Read the full README:** `README.md`
2. **Check examples:** `./examples/`
3. **Browse benchmarks:** `./benchmark/final/`
4. **Join community:**
   - [Slack](https://join.slack.com/t/ai-researchergroup/shared_invite/zt-30y5a070k-C0ajQt1zmVczFnfGkIicvA)
   - [Discord](https://discord.gg/zBNYTk5q2g)
5. **Report issues:** [GitHub Issues](https://github.com/HKUDS/AI-Researcher/issues)

---

## 🎓 Example Workflow

**Complete end-to-end example:**

```bash
# 1. Setup
cp .env.example .env
nano .env  # Add OPENROUTER_API_KEY

# 2. Start
make up

# 3. Run research (VQ example)
make run-task1 CATEGORY=vq INSTANCE=rotation_vq

# 4. Monitor (in another terminal)
make logs

# 5. After completion, generate paper
make run-paper CATEGORY=vq INSTANCE=rotation_vq

# 6. Find output
ls -la vq/target_sections/rotation_vq/iclr2025_conference.pdf

# 7. Stop when done
make down
```

---

## ⚡ Ultra Quick Start (One-Liner)

```bash
git clone https://github.com/HKUDS/AI-Researcher.git && \
cd AI-Researcher && \
cp .env.example .env && \
echo "⚠️  Edit .env and add your OPENROUTER_API_KEY, then run: make up && make example-vq"
```

---

## 📞 Need Help?

- **Documentation:** https://autoresearcher.github.io/docs
- **Issues:** https://github.com/HKUDS/AI-Researcher/issues
- **Slack:** https://join.slack.com/t/ai-researchergroup/...
- **Discord:** https://discord.gg/zBNYTk5q2g

---

**Happy Researching! 🚀🔬**
