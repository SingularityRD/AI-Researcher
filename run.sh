#!/bin/bash

###############################################################################
# AI-Researcher Quick Run Script
# Usage: ./run.sh [command] [options]
###############################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}=================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_env_file() {
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        echo ""
        print_info "Creating .env from .env.example..."
        cp .env.example .env
        print_warning "Please edit .env and add your API keys:"
        echo ""
        echo "  nano .env"
        echo ""
        echo "Required: OPENROUTER_API_KEY or OPENAI_API_KEY"
        exit 1
    fi
}

check_api_key() {
    if ! grep -q "OPENROUTER_API_KEY=.*[^your_]" .env && \
       ! grep -q "OPENAI_API_KEY=.*[^your_]" .env && \
       ! grep -q "ANTHROPIC_API_KEY=.*[^your_]" .env; then
        print_error "No valid API key found in .env!"
        echo ""
        print_warning "Please add at least one API key to .env:"
        echo "  - OPENROUTER_API_KEY (recommended)"
        echo "  - OPENAI_API_KEY"
        echo "  - ANTHROPIC_API_KEY"
        exit 1
    fi
    print_success "API key found"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed!"
        echo "Install from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker is installed"

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed!"
        echo "Install from: https://docs.docker.com/compose/install/"
        exit 1
    fi
    print_success "Docker Compose is installed"
}

wait_for_health() {
    print_info "Waiting for services to be healthy..."
    local max_attempts=30
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -sf http://localhost:7020/health > /dev/null 2>&1; then
            print_success "Services are healthy!"
            return 0
        fi
        attempt=$((attempt + 1))
        echo -n "."
        sleep 2
    done

    print_error "Services failed to become healthy"
    print_warning "Check logs with: make logs"
    return 1
}

show_usage() {
    cat << EOF
${GREEN}AI-Researcher Quick Run Script${NC}

${YELLOW}Usage:${NC}
  ./run.sh <command> [options]

${YELLOW}Commands:${NC}
  setup          - Initial setup (create .env, check dependencies)
  start          - Start all services
  stop           - Stop all services
  restart        - Restart all services
  logs           - View logs
  health         - Check service health
  status         - Show container status

  example-vq     - Run Vector Quantization example
  example-gnn    - Run Graph Neural Network example
  example-rec    - Run Recommendation System example

  task1          - Run Level 1 task (requires CATEGORY and INSTANCE)
  task2          - Run Level 2 task (requires CATEGORY and INSTANCE)
  paper          - Generate paper (requires CATEGORY and INSTANCE)

  shell          - Open shell in container
  clean          - Clean up temporary files
  backup         - Create backup

  help           - Show this help

${YELLOW}Examples:${NC}
  ./run.sh setup
  ./run.sh start
  ./run.sh example-vq
  ./run.sh task1 vq rotation_vq
  ./run.sh paper vq rotation_vq

${YELLOW}Environment:${NC}
  Edit .env file to configure API keys and settings

${YELLOW}Documentation:${NC}
  README.md       - Full documentation
  QUICKSTART.md   - Quick start guide

EOF
}

# Main script
main() {
    case "${1:-help}" in
        setup)
            print_header "AI-Researcher Setup"
            check_docker
            check_env_file
            check_api_key
            print_success "Setup complete!"
            echo ""
            print_info "Next step: ./run.sh start"
            ;;

        start)
            print_header "Starting AI-Researcher"
            check_env_file
            check_api_key

            print_info "Building and starting services..."
            docker-compose up -d

            wait_for_health

            echo ""
            print_success "AI-Researcher is ready!"
            echo ""
            print_info "Try an example: ./run.sh example-vq"
            print_info "View logs: ./run.sh logs"
            ;;

        stop)
            print_header "Stopping AI-Researcher"
            docker-compose down
            print_success "Services stopped"
            ;;

        restart)
            print_header "Restarting AI-Researcher"
            docker-compose restart
            wait_for_health
            print_success "Services restarted"
            ;;

        logs)
            print_header "Viewing Logs (Ctrl+C to exit)"
            docker-compose logs -f
            ;;

        health)
            print_header "Service Health Check"
            if curl -sf http://localhost:7020/health | python3 -m json.tool; then
                print_success "Service is healthy"
            else
                print_error "Service is not responding"
                exit 1
            fi
            ;;

        status)
            print_header "Container Status"
            docker-compose ps
            ;;

        example-vq)
            print_header "Running Vector Quantization Example"
            print_info "Category: vq, Instance: one_layer_vq"
            docker-compose exec ai-researcher python3 research_agent/run_infer_plan.py \
                --category vq \
                --instance_id one_layer_vq \
                --task_level task1
            ;;

        example-gnn)
            print_header "Running Graph Neural Network Example"
            print_info "Category: gnn, Instance: gnn_nodeformer"
            docker-compose exec ai-researcher python3 research_agent/run_infer_plan.py \
                --category gnn \
                --instance_id gnn_nodeformer \
                --task_level task1
            ;;

        example-rec)
            print_header "Running Recommendation System Example"
            print_info "Category: recommendation, Instance: hgcl"
            docker-compose exec ai-researcher python3 research_agent/run_infer_plan.py \
                --category recommendation \
                --instance_id hgcl \
                --task_level task1
            ;;

        task1)
            if [ -z "$2" ] || [ -z "$3" ]; then
                print_error "Missing arguments!"
                echo "Usage: ./run.sh task1 <CATEGORY> <INSTANCE>"
                echo "Example: ./run.sh task1 vq rotation_vq"
                exit 1
            fi
            print_header "Running Level 1 Task"
            print_info "Category: $2, Instance: $3"
            docker-compose exec ai-researcher python3 research_agent/run_infer_plan.py \
                --category "$2" \
                --instance_id "$3" \
                --task_level task1
            ;;

        task2)
            if [ -z "$2" ] || [ -z "$3" ]; then
                print_error "Missing arguments!"
                echo "Usage: ./run.sh task2 <CATEGORY> <INSTANCE>"
                echo "Example: ./run.sh task2 vq one_layer_vq"
                exit 1
            fi
            print_header "Running Level 2 Task"
            print_info "Category: $2, Instance: $3"
            docker-compose exec ai-researcher python3 research_agent/run_infer_idea.py \
                --category "$2" \
                --instance_id "$3"
            ;;

        paper)
            if [ -z "$2" ] || [ -z "$3" ]; then
                print_error "Missing arguments!"
                echo "Usage: ./run.sh paper <CATEGORY> <INSTANCE>"
                echo "Example: ./run.sh paper vq rotation_vq"
                exit 1
            fi
            print_header "Generating Paper"
            print_info "Category: $2, Instance: $3"
            docker-compose exec ai-researcher python3 paper_agent/writing.py \
                --research_field "$2" \
                --instance_id "$3"
            ;;

        shell)
            print_header "Opening Shell"
            docker-compose exec ai-researcher /bin/bash
            ;;

        clean)
            print_header "Cleaning Up"
            find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
            find . -type f -name "*.pyc" -delete
            rm -rf .pytest_cache .mypy_cache
            print_success "Cleanup complete"
            ;;

        backup)
            print_header "Creating Backup"
            mkdir -p backups
            timestamp=$(date +%Y%m%d_%H%M%S)
            backup_file="backups/backup_${timestamp}.tar.gz"
            tar -czf "$backup_file" \
                workplace_paper/ \
                .env \
                benchmark/final/ \
                2>/dev/null || true
            print_success "Backup created: $backup_file"
            ;;

        help|--help|-h)
            show_usage
            ;;

        *)
            print_error "Unknown command: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
