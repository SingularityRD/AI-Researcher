"""
Secure Secrets Management System
Handles API keys and sensitive credentials safely
"""
import os
import logging
from typing import Optional, Dict
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class SecretsManager:
    """Secure secrets management with validation and fallback"""

    # Supported API providers
    SUPPORTED_PROVIDERS = {
        'openrouter': {
            'key_env': 'OPENROUTER_API_KEY',
            'base_url_env': 'OPENROUTER_API_BASE',
            'default_base_url': 'https://openrouter.ai/api/v1'
        },
        'openai': {
            'key_env': 'OPENAI_API_KEY',
            'base_url_env': 'OPENAI_API_BASE',
            'default_base_url': 'https://api.openai.com/v1'
        },
        'anthropic': {
            'key_env': 'ANTHROPIC_API_KEY',
            'base_url_env': 'ANTHROPIC_API_BASE',
            'default_base_url': 'https://api.anthropic.com'
        },
        'deepseek': {
            'key_env': 'DEEPSEEK_API_KEY',
            'base_url_env': 'DEEPSEEK_API_BASE',
            'default_base_url': 'https://api.deepseek.com/v1'
        },
        'zai': {
            'key_env': 'ZAI_API_KEY',
            'base_url_env': 'ZAI_API_BASE',
            'default_base_url': 'https://api.z.ai/api/paas/v4'
        }
    }

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize secrets manager.

        Args:
            env_file: Path to .env file (defaults to project root/.env)
        """
        self._load_env(env_file)

    def _load_env(self, env_file: Optional[str] = None) -> None:
        """Load environment variables from .env file"""
        if env_file is None:
            # Look for .env in project root
            current_dir = Path(__file__).parent.parent
            env_file = current_dir / '.env'
        else:
            env_file = Path(env_file)

        if not env_file.exists():
            logger.warning(
                f".env file not found at {env_file}. "
                "Using system environment variables only."
            )
            return

        load_dotenv(env_file, override=True)
        logger.info(f"Environment variables loaded from {env_file}")

    def get_secret(self, key: str, required: bool = True) -> Optional[str]:
        """
        Get secret from environment variables.

        Args:
            key: Environment variable name
            required: If True, raises ValueError if not found

        Returns:
            Secret value or None

        Raises:
            ValueError: If required=True and secret not found
        """
        value = os.getenv(key)

        if value is None and required:
            raise ValueError(
                f"❌ Required secret '{key}' not found!\n"
                f"Please set it in .env file or environment variables.\n"
                f"Example: {key}=your_api_key_here"
            )

        # Validate not placeholder
        if value and 'your_' in value.lower() and '_here' in value.lower():
            raise ValueError(
                f"❌ '{key}' contains placeholder value!\n"
                f"Please replace '{value}' with your actual API key."
            )

        return value

    def get_provider_config(self, provider: str) -> Dict[str, str]:
        """
        Get API configuration for a provider.

        Args:
            provider: Provider name (openrouter, openai, zai, etc.)

        Returns:
            Dict with 'api_key' and 'base_url'

        Raises:
            ValueError: If provider not supported or API key missing
        """
        provider = provider.lower()

        if provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"❌ Unsupported provider: {provider}\n"
                f"Supported providers: {', '.join(self.SUPPORTED_PROVIDERS.keys())}"
            )

        config = self.SUPPORTED_PROVIDERS[provider]

        # Get API key
        api_key = self.get_secret(config['key_env'], required=True)

        # Get base URL (optional, use default if not set)
        base_url = os.getenv(
            config['base_url_env'],
            config['default_base_url']
        )

        return {
            'api_key': api_key,
            'base_url': base_url,
            'provider': provider
        }

    def validate_all_required_secrets(self) -> Dict[str, bool]:
        """
        Validate all configured secrets.

        Returns:
            Dict of {provider: is_valid}
        """
        results = {}

        for provider, config in self.SUPPORTED_PROVIDERS.items():
            try:
                api_key = os.getenv(config['key_env'])
                if api_key and 'your_' not in api_key.lower():
                    results[provider] = True
                else:
                    results[provider] = False
            except:
                results[provider] = False

        return results

    def get_github_token(self) -> Optional[str]:
        """Get GitHub token (optional)"""
        return self.get_secret('GITHUB_AI_TOKEN', required=False)


# Singleton instance
_secrets_manager: Optional[SecretsManager] = None


def get_secrets() -> SecretsManager:
    """Get singleton SecretsManager instance"""
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = SecretsManager()
    return _secrets_manager


def get_api_config_for_model(model_name: str) -> Dict[str, str]:
    """
    Get API configuration based on model name.

    Args:
        model_name: Model name (e.g., 'openrouter/google/gemini-2.5-pro', 'glm-4.6')

    Returns:
        Dict with API configuration

    Examples:
        >>> get_api_config_for_model('openrouter/google/gemini-2.5-pro')
        {'api_key': 'sk-...', 'base_url': 'https://openrouter.ai/api/v1', 'provider': 'openrouter'}

        >>> get_api_config_for_model('glm-4.6')
        {'api_key': 'your-key', 'base_url': 'https://api.z.ai/api/paas/v4', 'provider': 'zai'}
    """
    secrets = get_secrets()

    # Detect provider from model name
    model_lower = model_name.lower()

    if model_lower.startswith('openrouter/') or 'openrouter' in model_lower:
        return secrets.get_provider_config('openrouter')
    elif model_lower.startswith('gpt-') or model_lower.startswith('o1-'):
        return secrets.get_provider_config('openai')
    elif model_lower.startswith('claude-'):
        return secrets.get_provider_config('anthropic')
    elif model_lower.startswith('deepseek-'):
        return secrets.get_provider_config('deepseek')
    elif model_lower.startswith('glm-') or 'z.ai' in model_lower:
        return secrets.get_provider_config('zai')
    else:
        # Default to OpenRouter (supports many models)
        logger.warning(f"Unknown model provider for '{model_name}', using OpenRouter")
        return secrets.get_provider_config('openrouter')


if __name__ == "__main__":
    # Test
    secrets = get_secrets()
    print("✅ Secrets manager initialized")

    # Validate all secrets
    validation_results = secrets.validate_all_required_secrets()
    print("\n🔍 API Key Validation:")
    for provider, is_valid in validation_results.items():
        status = "✅" if is_valid else "❌"
        print(f"  {status} {provider.upper()}")
