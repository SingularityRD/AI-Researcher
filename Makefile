.PHONY: help install dev-install up down restart logs shell clean build rebuild health status

# Color codes for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Paper quality settings
QUALITY_THRESHOLD ?= 0.75  # 0.75 = NeurIPS Accept, 0.85 = Spotlight
MAX_ITERATIONS ?= 3

help: ## Show this help message
	@echo '${GREEN}AI-Researcher - Quick Commands${NC}'
	@echo ''
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${YELLOW}%-20s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ''
	@echo '${GREEN}🚀 Quick Start:${NC}'
	@echo '  make up              # Start all services'
	@echo '  make webgui          # Open Web GUI (http://localhost:7860)'
	@echo '  make run-enhanced-paper CATEGORY=vq INSTANCE=rotation_vq'

# ==============================================================================
# WEB GUI - EASIEST WAY TO USE! 🎨
# ==============================================================================

webgui: ## Start Web GUI (Gradio) - Easiest way to use!
	@echo "${GREEN}🎨 Starting Web GUI...${NC}"
	@if ! docker-compose ps | grep -q "webgui.*Up"; then \
		echo "${YELLOW}Starting webgui service...${NC}"; \
		docker-compose up -d webgui; \
		echo "${GREEN}Waiting for Web GUI to start...${NC}"; \
		sleep 8; \
	fi
	@echo "${GREEN}✅ Web GUI is running!${NC}"
	@echo ""
	@echo "${YELLOW}Open in your browser:${NC}"
	@echo "  ${GREEN}http://localhost:7860${NC}"
	@echo ""
	@echo "Or if using remote server:"
	@echo "  ${GREEN}http://your-server-ip:7860${NC}"

webgui-stop: ## Stop Web GUI
	@echo "${YELLOW}Stopping Web GUI...${NC}"
	docker-compose stop webgui

webgui-logs: ## View Web GUI logs
	docker-compose logs -f webgui

webgui-restart: ## Restart Web GUI
	@echo "${YELLOW}Restarting Web GUI...${NC}"
	docker-compose restart webgui
	@echo "${GREEN}Web GUI restarted! Open http://localhost:7860${NC}"

# ==============================================================================
# INSTALLATION
# ==============================================================================

install: ## Install production dependencies (without Docker)
	@echo "${GREEN}Installing production dependencies...${NC}"
	pip install -e .
	playwright install

dev-install: ## Install development dependencies
	@echo "${GREEN}Installing development dependencies...${NC}"
	pip install -e ".[dev]"
	playwright install
	pre-commit install

# ==============================================================================
# DOCKER OPERATIONS
# ==============================================================================

build: ## Build Docker images
	@echo "${GREEN}Building Docker images...${NC}"
	docker-compose build

up: ## Start all services
	@echo "${GREEN}Starting AI-Researcher services...${NC}"
	@if [ ! -f .env ]; then \
		echo "${RED}Error: .env file not found!${NC}"; \
		echo "${YELLOW}Please copy .env.example to .env and configure it:${NC}"; \
		echo "  cp .env.example .env"; \
		echo "  nano .env  # Add your API keys"; \
		exit 1; \
	fi
	docker-compose up -d
	@echo "${GREEN}Services started!${NC}"
	@echo "${YELLOW}Waiting for services to be ready...${NC}"
	@sleep 5
	@make health

down: ## Stop all services
	@echo "${YELLOW}Stopping AI-Researcher services...${NC}"
	docker-compose down

restart: ## Restart all services
	@echo "${YELLOW}Restarting services...${NC}"
	docker-compose restart

rebuild: ## Rebuild and restart all services
	@echo "${GREEN}Rebuilding and restarting...${NC}"
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@make health

# ==============================================================================
# MONITORING
# ==============================================================================

logs: ## View logs (use CTRL+C to exit)
	docker-compose logs -f

logs-research: ## View research agent logs
	docker-compose logs -f ai-researcher

logs-redis: ## View Redis logs
	docker-compose logs -f redis

health: ## Check service health
	@echo "${GREEN}Checking service health...${NC}"
	@curl -s http://localhost:7020/health | python3 -m json.tool || echo "${RED}Service not responding${NC}"

status: ## Show container status
	@echo "${GREEN}Container Status:${NC}"
	@docker-compose ps

# ==============================================================================
# DEVELOPMENT
# ==============================================================================

shell: ## Open bash shell in main container
	docker-compose exec ai-researcher /bin/bash

shell-root: ## Open bash shell as root
	docker-compose exec -u root ai-researcher /bin/bash

redis-cli: ## Open Redis CLI
	docker-compose exec redis redis-cli

# ==============================================================================
# USAGE
# ==============================================================================

run-task1: ## Run Level 1 task (Detailed Idea Description)
	@echo "${GREEN}Running Level 1 task...${NC}"
	@if [ -z "$(CATEGORY)" ]; then \
		echo "${RED}Error: CATEGORY not specified${NC}"; \
		echo "Usage: make run-task1 CATEGORY=vq INSTANCE=one_layer_vq"; \
		exit 1; \
	fi
	@if [ -z "$(INSTANCE)" ]; then \
		echo "${RED}Error: INSTANCE not specified${NC}"; \
		echo "Usage: make run-task1 CATEGORY=vq INSTANCE=one_layer_vq"; \
		exit 1; \
	fi
	docker-compose exec ai-researcher python3 research_agent/run_infer_plan.py \
		--category $(CATEGORY) \
		--instance_id $(INSTANCE) \
		--task_level task1

run-task2: ## Run Level 2 task (Reference-Based Ideation)
	@echo "${GREEN}Running Level 2 task...${NC}"
	@if [ -z "$(CATEGORY)" ]; then \
		echo "${RED}Error: CATEGORY not specified${NC}"; \
		echo "Usage: make run-task2 CATEGORY=vq INSTANCE=one_layer_vq"; \
		exit 1; \
	fi
	@if [ -z "$(INSTANCE)" ]; then \
		echo "${RED}Error: INSTANCE not specified${NC}"; \
		echo "Usage: make run-task2 CATEGORY=vq INSTANCE=one_layer_vq"; \
		exit 1; \
	fi
	docker-compose exec ai-researcher python3 research_agent/run_infer_idea.py \
		--category $(CATEGORY) \
		--instance_id $(INSTANCE)

run-paper: ## Generate paper from results (basic)
	@echo "${GREEN}Generating paper...${NC}"
	@if [ -z "$(CATEGORY)" ]; then \
		echo "${RED}Error: CATEGORY not specified${NC}"; \
		echo "Usage: make run-paper CATEGORY=vq INSTANCE=rotation_vq"; \
		exit 1; \
	fi
	@if [ -z "$(INSTANCE)" ]; then \
		echo "${RED}Error: INSTANCE not specified${NC}"; \
		echo "Usage: make run-paper CATEGORY=vq INSTANCE=rotation_vq"; \
		exit 1; \
	fi
	docker-compose exec ai-researcher python3 paper_agent/writing.py \
		--research_field $(CATEGORY) \
		--instance_id $(INSTANCE)

run-enhanced-paper: ## Generate NeurIPS-tier quality paper (recommended!)
	@echo "${GREEN}Generating NeurIPS-tier quality paper...${NC}"
	@echo "${YELLOW}This includes quality checks and improvements${NC}"
	@if [ -z "$(CATEGORY)" ]; then \
		echo "${RED}Error: CATEGORY not specified${NC}"; \
		echo "Usage: make run-enhanced-paper CATEGORY=vq INSTANCE=rotation_vq"; \
		exit 1; \
	fi
	@if [ -z "$(INSTANCE)" ]; then \
		echo "${RED}Error: INSTANCE not specified${NC}"; \
		echo "Usage: make run-enhanced-paper CATEGORY=vq INSTANCE=rotation_vq"; \
		exit 1; \
	fi
	docker-compose exec ai-researcher python3 paper_agent/enhanced_writing.py \
		--research_field $(CATEGORY) \
		--instance_id $(INSTANCE) \
		--quality_threshold $(QUALITY_THRESHOLD) \
		--max_iterations $(MAX_ITERATIONS)

check-paper-quality: ## Check paper quality score
	@echo "${GREEN}Checking paper quality...${NC}"
	@if [ -z "$(CATEGORY)" ]; then \
		echo "${RED}Error: CATEGORY not specified${NC}"; \
		echo "Usage: make check-paper-quality CATEGORY=vq INSTANCE=rotation_vq"; \
		exit 1; \
	fi
	@if [ -z "$(INSTANCE)" ]; then \
		echo "${RED}Error: INSTANCE not specified${NC}"; \
		echo "Usage: make check-paper-quality CATEGORY=vq INSTANCE=rotation_vq"; \
		exit 1; \
	fi
	@cat $(CATEGORY)/target_sections/$(INSTANCE)/quality_report.txt || echo "No quality report found. Run enhanced paper generation first."

# ==============================================================================
# EXAMPLES
# ==============================================================================

example-vq: ## Run Vector Quantization example
	@echo "${GREEN}Running VQ example...${NC}"
	@make run-task1 CATEGORY=vq INSTANCE=one_layer_vq

example-gnn: ## Run Graph Neural Network example
	@echo "${GREEN}Running GNN example...${NC}"
	@make run-task1 CATEGORY=gnn INSTANCE=gnn_nodeformer

example-recommendation: ## Run Recommendation System example
	@echo "${GREEN}Running Recommendation example...${NC}"
	@make run-task1 CATEGORY=recommendation INSTANCE=hgcl

# ==============================================================================
# MAINTENANCE
# ==============================================================================

clean: ## Clean up temporary files and caches
	@echo "${YELLOW}Cleaning up...${NC}"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov/
	rm -rf build/ dist/
	@echo "${GREEN}Cleanup complete!${NC}"

clean-all: clean ## Deep clean (including Docker volumes and images)
	@echo "${RED}Warning: This will remove all Docker containers, volumes, and images${NC}"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker system prune -af --volumes; \
		echo "${GREEN}Deep clean complete!${NC}"; \
	else \
		echo "${YELLOW}Cancelled${NC}"; \
	fi

clean-cache: ## Clean cache directory
	@echo "${YELLOW}Cleaning cache...${NC}"
	rm -rf cache/* cache_*/*
	@echo "${GREEN}Cache cleaned!${NC}"

clean-logs: ## Clean log files
	@echo "${YELLOW}Cleaning logs...${NC}"
	rm -rf logs/*.log
	@echo "${GREEN}Logs cleaned!${NC}"

# ==============================================================================
# BACKUP
# ==============================================================================

backup: ## Backup important data
	@echo "${GREEN}Creating backup...${NC}"
	@mkdir -p backups
	@tar -czf backups/backup_$$(date +%Y%m%d_%H%M%S).tar.gz \
		workplace_paper/ \
		.env \
		benchmark/final/ \
		2>/dev/null || true
	@echo "${GREEN}Backup created in backups/${NC}"

# ==============================================================================
# QUICK START
# ==============================================================================

quick-start: ## Quick start guide
	@echo "${GREEN}==================================${NC}"
	@echo "${GREEN}AI-Researcher Quick Start Guide${NC}"
	@echo "${GREEN}==================================${NC}"
	@echo ""
	@echo "${YELLOW}1. Setup environment:${NC}"
	@echo "   cp .env.example .env"
	@echo "   nano .env  # Add your API keys"
	@echo ""
	@echo "${YELLOW}2. Start services:${NC}"
	@echo "   make up"
	@echo ""
	@echo "${YELLOW}3. Run an example:${NC}"
	@echo "   make example-vq"
	@echo ""
	@echo "${YELLOW}4. Monitor logs:${NC}"
	@echo "   make logs"
	@echo ""
	@echo "${YELLOW}5. Stop services:${NC}"
	@echo "   make down"
	@echo ""
	@echo "For more commands: make help"
