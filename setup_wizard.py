#!/usr/bin/env python3
"""
AI-Researcher Setup Wizard
Interactive setup to configure .env file and validate installation
"""
import os
import sys
import shutil
from pathlib import Path
from typing import Optional, Dict, List


class Colors:
    """Terminal colors for pretty output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")


def get_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default"""
    if default:
        prompt_text = f"{Colors.OKBLUE}{prompt} [{default}]: {Colors.ENDC}"
    else:
        prompt_text = f"{Colors.OKBLUE}{prompt}: {Colors.ENDC}"

    value = input(prompt_text).strip()
    return value if value else (default or "")


def yes_no(prompt: str, default: bool = True) -> bool:
    """Ask yes/no question"""
    default_str = "Y/n" if default else "y/N"
    response = get_input(f"{prompt} ({default_str})", "y" if default else "n").lower()
    return response in ('y', 'yes', '') if default else response in ('y', 'yes')


def check_dependencies():
    """Check if required dependencies are installed"""
    print_header("Checking Dependencies")

    dependencies = {
        'docker': 'Docker (for containerization)',
        'python3': 'Python 3.11+ (for local development)',
        'git': 'Git (for version control)'
    }

    missing = []

    for cmd, desc in dependencies.items():
        if shutil.which(cmd):
            print_success(f"{desc} - Found")
        else:
            print_warning(f"{desc} - Not found")
            missing.append(cmd)

    if missing:
        print_warning(f"Optional dependencies missing: {', '.join(missing)}")
        print_info("You can still proceed, but some features may not work.")
        if not yes_no("Continue anyway?", default=True):
            sys.exit(1)
    else:
        print_success("All dependencies found!")


def setup_env_file():
    """Create .env file interactively"""
    print_header("Environment Configuration")

    env_example = Path('.env.example')
    env_file = Path('.env')

    if not env_example.exists():
        print_error(".env.example not found!")
        print_info("Make sure you're running this from the project root directory")
        sys.exit(1)

    if env_file.exists():
        print_warning(".env file already exists!")
        if not yes_no("Overwrite existing .env file?", default=False):
            print_info("Keeping existing .env file")
            return

    print_info("Let's configure your AI-Researcher installation\n")

    # Select API provider
    print(f"{Colors.BOLD}Choose your AI API provider:{Colors.ENDC}")
    print("1. Z.AI (GLM-4.6) - Recommended")
    print("2. OpenRouter (Multi-model support)")
    print("3. OpenAI (GPT-4, GPT-4o)")
    print("4. Anthropic (Claude)")
    print("5. DeepSeek (DeepSeek Chat/Coder)")
    print("6. Skip (I'll configure manually)")

    choice = get_input("Select option (1-6)", "1")

    config: Dict[str, str] = {}

    if choice == "1":
        # Z.AI setup
        print_info("\n🌟 Z.AI Configuration")
        print_info("Get your API key from: https://api.z.ai/")
        config['ZAI_API_KEY'] = get_input("Enter your Z.AI API key")
        config['ZAI_API_BASE'] = 'https://api.z.ai/api/paas/v4'
        config['COMPLETION_MODEL'] = 'glm-4.6'
        config['CHEEP_MODEL'] = 'glm-4-flashx'

    elif choice == "2":
        # OpenRouter setup
        print_info("\n🌐 OpenRouter Configuration")
        print_info("Get your API key from: https://openrouter.ai/keys")
        config['OPENROUTER_API_KEY'] = get_input("Enter your OpenRouter API key")
        config['OPENROUTER_API_BASE'] = 'https://openrouter.ai/api/v1'
        config['COMPLETION_MODEL'] = get_input(
            "Main model",
            "openrouter/google/gemini-2.5-pro-preview-05-20"
        )
        config['CHEEP_MODEL'] = get_input(
            "Cheap model",
            "openrouter/google/gemini-2.5-flash-preview-05-20"
        )

    elif choice == "3":
        # OpenAI setup
        print_info("\n🤖 OpenAI Configuration")
        print_info("Get your API key from: https://platform.openai.com/api-keys")
        config['OPENAI_API_KEY'] = get_input("Enter your OpenAI API key")
        config['OPENAI_API_BASE'] = 'https://api.openai.com/v1'
        config['COMPLETION_MODEL'] = get_input("Main model", "gpt-4o-2024-08-06")
        config['CHEEP_MODEL'] = get_input("Cheap model", "gpt-4o-mini")

    elif choice == "4":
        # Anthropic setup
        print_info("\n🧠 Anthropic Configuration")
        print_info("Get your API key from: https://console.anthropic.com/")
        config['ANTHROPIC_API_KEY'] = get_input("Enter your Anthropic API key")
        config['ANTHROPIC_API_BASE'] = 'https://api.anthropic.com'
        config['COMPLETION_MODEL'] = get_input(
            "Main model",
            "claude-3-5-sonnet-20241022"
        )
        config['CHEEP_MODEL'] = get_input("Cheap model", "claude-3-5-haiku-20241022")

    elif choice == "5":
        # DeepSeek setup
        print_info("\n🔍 DeepSeek Configuration")
        print_info("Get your API key from: https://platform.deepseek.com/")
        config['DEEPSEEK_API_KEY'] = get_input("Enter your DeepSeek API key")
        config['DEEPSEEK_API_BASE'] = 'https://api.deepseek.com/v1'
        config['COMPLETION_MODEL'] = 'deepseek-chat'
        config['CHEEP_MODEL'] = 'deepseek-chat'

    elif choice == "6":
        print_info("Skipping API configuration")
        print_info("You'll need to manually edit .env file later")

    # Basic configuration
    print_info("\n⚙️  Basic Configuration")
    config['CATEGORY'] = get_input("Research category", "vq")
    config['INSTANCE_ID'] = get_input("Instance ID", "one_layer_vq")
    config['TASK_LEVEL'] = get_input("Task level (task1/task2)", "task1")

    # GPU configuration
    if yes_no("\nDo you have an NVIDIA GPU?", default=True):
        gpu_choice = get_input('GPU devices (0, 0,1, or "all")', "0")
        config['GPUS'] = f'"{gpu_choice}"' if gpu_choice != 'all' else '"all"'
    else:
        config['GPUS'] = 'None'

    # Proxy configuration
    if yes_no("\nDo you need to use a proxy?", default=False):
        config['HTTPS_PROXY'] = get_input("HTTPS Proxy (e.g., http://proxy:port)")
        config['HTTP_PROXY'] = config['HTTPS_PROXY']

    # Create .env file
    print_info("\n📝 Creating .env file...")

    # Read template
    with open(env_example, 'r') as f:
        env_content = f.read()

    # Replace values
    for key, value in config.items():
        # Find the line with the key and replace it
        import re
        pattern = rf'^{key}=.*$'
        replacement = f'{key}={value}'
        env_content = re.sub(pattern, replacement, env_content, flags=re.MULTILINE)

    # Write .env file
    with open(env_file, 'w') as f:
        f.write(env_content)

    print_success(".env file created successfully!")


def validate_installation():
    """Validate the installation"""
    print_header("Validating Installation")

    # Check .env file
    if not Path('.env').exists():
        print_error(".env file not found!")
        print_info("Run this script again or copy .env.example to .env")
        return False

    # Try to import utilities
    try:
        sys.path.insert(0, str(Path.cwd()))
        from utils.secrets_manager import get_secrets

        secrets = get_secrets()
        validation_results = secrets.validate_all_required_secrets()

        print_info("API Key Validation:")
        found_valid = False
        for provider, is_valid in validation_results.items():
            if is_valid:
                print_success(f"{provider.upper()} - Valid")
                found_valid = True
            else:
                print_warning(f"{provider.upper()} - Not configured or invalid")

        if not found_valid:
            print_error("No valid API keys found!")
            print_info("Please configure at least one API provider in .env file")
            return False

        print_success("Validation passed!")
        return True

    except Exception as e:
        print_error(f"Validation failed: {e}")
        return False


def show_next_steps():
    """Show next steps to user"""
    print_header("Next Steps")

    print(f"{Colors.BOLD}Your AI-Researcher is ready!{Colors.ENDC}\n")

    print(f"{Colors.OKCYAN}Option 1: Web GUI (Recommended):{Colors.ENDC}")
    print("  make up          # Start services")
    print("  make webgui      # Start web interface")
    print("  # Open http://localhost:7860 in your browser\n")

    print(f"{Colors.OKCYAN}Option 2: Command Line:{Colors.ENDC}")
    print("  make up              # Start services")
    print("  make run-research    # Run research agent")
    print("  make run-paper       # Generate paper\n")

    print(f"{Colors.OKCYAN}Useful Commands:{Colors.ENDC}")
    print("  make help            # Show all commands")
    print("  make health          # Check system health")
    print("  make logs            # View logs")
    print("  make down            # Stop all services\n")

    print(f"{Colors.BOLD}Documentation:{Colors.ENDC}")
    print("  README.md            # Main documentation")
    print("  SETUP_GUIDE_TR.md    # Turkish setup guide")
    print("  QUICKSTART.md        # Quick start guide\n")


def main():
    """Main setup wizard"""
    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         AI-Researcher Setup Wizard                        ║
║         Production-Ready Configuration                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}
""")

    print_info("This wizard will help you set up AI-Researcher")
    print_info("Make sure you're running this from the project root directory\n")

    if not yes_no("Continue with setup?", default=True):
        print_info("Setup cancelled")
        sys.exit(0)

    # Step 1: Check dependencies
    check_dependencies()

    # Step 2: Setup .env file
    setup_env_file()

    # Step 3: Validate installation
    is_valid = validate_installation()

    # Step 4: Show next steps
    show_next_steps()

    if is_valid:
        print_success("\n✨ Setup completed successfully!")
        print_info("You can now start using AI-Researcher")
    else:
        print_warning("\n⚠️  Setup completed with warnings")
        print_info("Please review the errors above and fix them")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nSetup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
