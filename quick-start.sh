#!/bin/bash
#
# AI-Researcher One-Click Setup Script
# Usage: curl -fsSL https://raw.githubusercontent.com/HKUDS/AI-Researcher/main/quick-start.sh | bash
# Or: ./quick-start.sh
#

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         AI-Researcher - Zero-Touch Setup                  ║
║         🚀 Production-Ready in 5 Minutes                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Helper functions
print_step() {
    echo -e "\n${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if running as root (not recommended)
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root is not recommended"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: Check Prerequisites
print_step "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker not found!"
    echo "Install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
print_success "Docker found: $(docker --version)"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_warning "docker-compose not found, trying docker compose plugin"
    if ! docker compose version &> /dev/null; then
        print_error "Docker Compose not found!"
        echo "Install Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi
print_success "Docker Compose found"

# Check Python (optional)
if command -v python3 &> /dev/null; then
    print_success "Python found: $(python3 --version)"
else
    print_warning "Python not found (optional, needed for setup wizard)"
fi

# Check Git
if ! command -v git &> /dev/null; then
    print_warning "Git not found (optional)"
fi

# Step 2: Clone or Update Repository
print_step "Setting up repository..."

if [ ! -d "AI-Researcher" ]; then
    if command -v git &> /dev/null; then
        print_step "Cloning AI-Researcher repository..."
        git clone https://github.com/HKUDS/AI-Researcher.git
        cd AI-Researcher
    else
        print_error "Git not found! Please install git or download the repository manually"
        exit 1
    fi
else
    print_step "AI-Researcher directory already exists, updating..."
    cd AI-Researcher
    if command -v git &> /dev/null; then
        git pull || print_warning "Could not update repository"
    fi
fi

print_success "Repository ready"

# Step 3: Setup .env file
print_step "Setting up environment configuration..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Created .env from .env.example"

        echo ""
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${YELLOW}⚡ QUICK SETUP: Choose your AI provider${NC}"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo "1. Z.AI (GLM-4.6) - Best for Chinese users"
        echo "2. OpenRouter - Access to 100+ models"
        echo "3. OpenAI - GPT-4, GPT-4o"
        echo "4. Skip (configure manually later)"
        echo ""
        read -p "Select option (1-4) [1]: " choice
        choice=${choice:-1}

        case $choice in
            1)
                print_step "Z.AI Configuration"
                echo "Get your API key from: https://api.z.ai/"
                read -p "Enter your Z.AI API key: " zai_key
                if [ ! -z "$zai_key" ]; then
                    # Update .env file
                    if [[ "$OSTYPE" == "darwin"* ]]; then
                        # macOS
                        sed -i '' "s/^ZAI_API_KEY=.*/ZAI_API_KEY=$zai_key/" .env
                        sed -i '' "s/^COMPLETION_MODEL=.*/COMPLETION_MODEL=glm-4.6/" .env
                        sed -i '' "s/^CHEEP_MODEL=.*/CHEEP_MODEL=glm-4-flashx/" .env
                    else
                        # Linux
                        sed -i "s/^ZAI_API_KEY=.*/ZAI_API_KEY=$zai_key/" .env
                        sed -i "s/^COMPLETION_MODEL=.*/COMPLETION_MODEL=glm-4.6/" .env
                        sed -i "s/^CHEEP_MODEL=.*/CHEEP_MODEL=glm-4-flashx/" .env
                    fi
                    print_success "Z.AI configured!"
                fi
                ;;
            2)
                print_step "OpenRouter Configuration"
                echo "Get your API key from: https://openrouter.ai/keys"
                read -p "Enter your OpenRouter API key: " or_key
                if [ ! -z "$or_key" ]; then
                    if [[ "$OSTYPE" == "darwin"* ]]; then
                        sed -i '' "s/^OPENROUTER_API_KEY=.*/OPENROUTER_API_KEY=$or_key/" .env
                        sed -i '' "s/^COMPLETION_MODEL=.*/COMPLETION_MODEL=openrouter\/google\/gemini-2.5-pro-preview-05-20/" .env
                    else
                        sed -i "s/^OPENROUTER_API_KEY=.*/OPENROUTER_API_KEY=$or_key/" .env
                        sed -i "s/^COMPLETION_MODEL=.*/COMPLETION_MODEL=openrouter\/google\/gemini-2.5-pro-preview-05-20/" .env
                    fi
                    print_success "OpenRouter configured!"
                fi
                ;;
            3)
                print_step "OpenAI Configuration"
                echo "Get your API key from: https://platform.openai.com/api-keys"
                read -p "Enter your OpenAI API key: " oai_key
                if [ ! -z "$oai_key" ]; then
                    if [[ "$OSTYPE" == "darwin"* ]]; then
                        sed -i '' "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=$oai_key/" .env
                        sed -i '' "s/^COMPLETION_MODEL=.*/COMPLETION_MODEL=gpt-4o-2024-08-06/" .env
                    else
                        sed -i "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=$oai_key/" .env
                        sed -i "s/^COMPLETION_MODEL=.*/COMPLETION_MODEL=gpt-4o-2024-08-06/" .env
                    fi
                    print_success "OpenAI configured!"
                fi
                ;;
            4)
                print_warning "Skipping API configuration"
                print_step "You'll need to manually edit .env file and add your API key"
                ;;
        esac
    else
        print_error ".env.example not found!"
        exit 1
    fi
else
    print_success ".env file already exists"
fi

# Step 4: Pull Docker images (optional, faster startup)
print_step "Preparing Docker images..."
read -p "Pre-download Docker images? (faster first startup) (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    print_step "Pulling Docker images (this may take a few minutes)..."
    $DOCKER_COMPOSE pull || print_warning "Could not pull images, will build instead"
fi

# Step 5: Start services
print_step "Starting AI-Researcher services..."

$DOCKER_COMPOSE up -d

# Wait for services to be ready
print_step "Waiting for services to start..."
sleep 10

# Check service health
print_step "Checking service health..."

if $DOCKER_COMPOSE ps | grep -q "webgui.*Up"; then
    print_success "Web GUI is running"
else
    print_warning "Web GUI may not be running correctly"
fi

if $DOCKER_COMPOSE ps | grep -q "redis.*Up"; then
    print_success "Redis is running"
else
    print_warning "Redis may not be running correctly"
fi

# Final messages
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ AI-Researcher is ready!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}🌐 Web GUI:${NC}"
echo -e "   ${GREEN}http://localhost:7860${NC}"
echo ""
echo -e "${BLUE}📖 Quick Commands:${NC}"
echo "   make help              # Show all commands"
echo "   make logs              # View logs"
echo "   make down              # Stop services"
echo "   make restart           # Restart services"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "   README.md              # Main documentation"
echo "   SETUP_GUIDE_TR.md      # Turkish setup guide"
echo ""
echo -e "${BLUE}🆘 Need Help?${NC}"
echo "   GitHub: https://github.com/HKUDS/AI-Researcher/issues"
echo "   Slack:  https://join.slack.com/..."
echo ""
echo -e "${YELLOW}⚡ Pro Tip:${NC} Open http://localhost:7860 in your browser to start!"
echo ""

# Offer to open browser (macOS/Linux with xdg-open)
if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Open Web GUI in browser now? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        open "http://localhost:7860"
    fi
elif command -v xdg-open &> /dev/null; then
    read -p "Open Web GUI in browser now? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        xdg-open "http://localhost:7860" &> /dev/null &
    fi
fi

print_success "Setup complete! Happy researching! 🚀"
