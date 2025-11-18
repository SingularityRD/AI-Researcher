"""
Input Validation and Sanitization Utilities
Prevents injection attacks and ensures data integrity
"""
import re
import os
from pathlib import Path
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class ValidationError(ValueError):
    """Raised when input validation fails"""
    pass


def validate_identifier(
    value: str,
    name: str,
    max_length: int = 50,
    allow_dash: bool = True,
    allow_underscore: bool = True,
    allow_slash: bool = False
) -> str:
    """
    Validate identifier (research_field, instance_id, etc.).

    Security checks:
    - Non-empty
    - Length limit
    - Character whitelist (alphanumeric + optional dash/underscore)
    - No path traversal
    - No shell metacharacters

    Args:
        value: Value to validate
        name: Field name (for error messages)
        max_length: Maximum length
        allow_dash: Allow dash character
        allow_underscore: Allow underscore character
        allow_slash: Allow forward slash (for paths like 'vq/rotation')

    Returns:
        Validated value

    Raises:
        ValidationError: If validation fails

    Examples:
        >>> validate_identifier('vq', 'research_field')
        'vq'
        >>> validate_identifier('../etc/passwd', 'field')
        ValidationError: Path traversal detected
    """
    # Check non-empty
    if not value or not isinstance(value, str):
        raise ValidationError(f"❌ {name} must be a non-empty string")

    value = value.strip()

    if not value:
        raise ValidationError(f"❌ {name} cannot be empty or whitespace only")

    # Check length
    if len(value) > max_length:
        raise ValidationError(
            f"❌ {name} too long ({len(value)} characters > {max_length} max)\n"
            f"   Value: '{value[:50]}...'"
        )

    # Build allowed character pattern
    allowed_chars = 'a-zA-Z0-9'
    if allow_underscore:
        allowed_chars += '_'
    if allow_dash:
        allowed_chars += '-'
    if allow_slash:
        allowed_chars += '/'

    pattern = f'^[{allowed_chars}]+$'

    if not re.match(pattern, value):
        raise ValidationError(
            f"❌ {name} contains invalid characters\n"
            f"   Value: '{value}'\n"
            f"   Allowed: alphanumeric" +
            (" + dash" if allow_dash else "") +
            (" + underscore" if allow_underscore else "") +
            (" + slash" if allow_slash else "")
        )

    # Check for path traversal
    if '..' in value:
        raise ValidationError(
            f"❌ Path traversal detected in {name}: '{value}'\n"
            f"   '..' is not allowed"
        )

    # Check for null bytes
    if '\0' in value:
        raise ValidationError(f"❌ Null byte detected in {name}")

    # Check for shell metacharacters
    dangerous_chars = set(';&|`$(){}[]<>*?\'"\\')
    found_dangerous = [c for c in value if c in dangerous_chars]

    if found_dangerous:
        raise ValidationError(
            f"❌ Shell metacharacters not allowed in {name}\n"
            f"   Found: {', '.join(repr(c) for c in found_dangerous)}"
        )

    return value


def validate_path(
    user_path: str,
    base_dir: str,
    must_exist: bool = False,
    name: str = "path"
) -> Path:
    """
    Validate and sanitize file path.

    Ensures path is within base_dir (prevents path traversal).

    Args:
        user_path: User-provided path (can be relative)
        base_dir: Base directory (security boundary)
        must_exist: If True, path must exist
        name: Field name (for error messages)

    Returns:
        Validated absolute Path object

    Raises:
        ValidationError: If path invalid or outside base_dir

    Examples:
        >>> validate_path('papers/vq', '/app')
        PosixPath('/app/papers/vq')
        >>> validate_path('../../../etc/passwd', '/app')
        ValidationError: Path outside base directory
    """
    # Convert to Path objects
    base = Path(base_dir).resolve()

    # Handle both absolute and relative paths
    if Path(user_path).is_absolute():
        target = Path(user_path).resolve()
    else:
        target = (base / user_path).resolve()

    # Ensure path is within base_dir
    try:
        target.relative_to(base)
    except ValueError:
        raise ValidationError(
            f"❌ {name} is outside base directory\n"
            f"   Attempted: {target}\n"
            f"   Base dir: {base}"
        )

    # Check existence if required
    if must_exist and not target.exists():
        raise ValidationError(
            f"❌ {name} does not exist: {target}"
        )

    return target


def validate_branch_name(branch: str) -> str:
    """
    Validate git branch name.

    Args:
        branch: Branch name

    Returns:
        Validated branch name

    Raises:
        ValidationError: If invalid

    Examples:
        >>> validate_branch_name('main')
        'main'
        >>> validate_branch_name('feature/new-api')
        'feature/new-api'
        >>> validate_branch_name('test; rm -rf /')
        ValidationError: Invalid characters
    """
    # Git branch name rules
    if not branch or not branch.strip():
        raise ValidationError("❌ Branch name cannot be empty")

    branch = branch.strip()

    # Length check
    if len(branch) > 255:
        raise ValidationError(f"❌ Branch name too long ({len(branch)} > 255)")

    # Character check (alphanumeric, dash, underscore, slash)
    if not re.match(r'^[a-zA-Z0-9/_-]+$', branch):
        raise ValidationError(
            f"❌ Invalid branch name: '{branch}'\n"
            f"   Allowed: alphanumeric, dash, underscore, slash"
        )

    # Git restrictions
    if branch.startswith('.') or branch.startswith('/'):
        raise ValidationError(f"❌ Branch name cannot start with '.' or '/'")

    if branch.endswith('.lock'):
        raise ValidationError(f"❌ Branch name cannot end with '.lock'")

    if '..' in branch:
        raise ValidationError(f"❌ Branch name cannot contain '..'")

    return branch


def validate_url(url: str, allowed_schemes: Optional[List[str]] = None) -> str:
    """
    Validate URL.

    Args:
        url: URL to validate
        allowed_schemes: List of allowed schemes (default: ['https'])

    Returns:
        Validated URL

    Raises:
        ValidationError: If invalid

    Examples:
        >>> validate_url('https://github.com/user/repo')
        'https://github.com/user/repo'
        >>> validate_url('file:///etc/passwd')
        ValidationError: URL scheme not allowed
    """
    if allowed_schemes is None:
        allowed_schemes = ['https']  # Only HTTPS by default for security

    if not url or not url.strip():
        raise ValidationError("❌ URL cannot be empty")

    url = url.strip()

    # Basic URL pattern check
    url_pattern = re.compile(
        r'^(https?|git)://'  # scheme
        r'[a-zA-Z0-9.-]+'  # domain
        r'(/[a-zA-Z0-9._~:/?#[\]@!$&\'()*+,;=-]*)?$'  # path
    )

    if not url_pattern.match(url):
        raise ValidationError(f"❌ Invalid URL format: '{url}'")

    # Check scheme
    scheme = url.split('://')[0].lower()
    if scheme not in allowed_schemes:
        raise ValidationError(
            f"❌ URL scheme '{scheme}' not allowed\n"
            f"   Allowed schemes: {', '.join(allowed_schemes)}"
        )

    # Prevent local file access
    if 'localhost' in url.lower() or '127.0.0.1' in url:
        raise ValidationError("❌ Local URLs not allowed")

    return url


def validate_model_name(model: str) -> str:
    """
    Validate model name.

    Args:
        model: Model name

    Returns:
        Validated model name

    Raises:
        ValidationError: If invalid

    Examples:
        >>> validate_model_name('openrouter/google/gemini-2.5-pro')
        'openrouter/google/gemini-2.5-pro'
        >>> validate_model_name('gpt-4o')
        'gpt-4o'
    """
    if not model or not model.strip():
        raise ValidationError("❌ Model name cannot be empty")

    model = model.strip()

    # Length check
    if len(model) > 200:
        raise ValidationError(f"❌ Model name too long ({len(model)} > 200)")

    # Character check (alphanumeric, dash, underscore, slash, dot)
    if not re.match(r'^[a-zA-Z0-9/_.-]+$', model):
        raise ValidationError(
            f"❌ Invalid model name: '{model}'\n"
            f"   Allowed: alphanumeric, dash, underscore, slash, dot"
        )

    return model


def sanitize_latex_content(content: str) -> str:
    """
    Sanitize LaTeX content to prevent LaTeX injection.

    Blocks dangerous commands that could execute shell commands.

    Args:
        content: LaTeX content

    Returns:
        Sanitized content

    Raises:
        ValidationError: If dangerous commands found

    Examples:
        >>> sanitize_latex_content('\\section{Introduction}')
        '\\section{Introduction}'
        >>> sanitize_latex_content('\\immediate\\write18{rm -rf /}')
        ValidationError: Dangerous LaTeX command detected
    """
    # Dangerous LaTeX commands
    dangerous_patterns = [
        (r'\\write18', 'write18 (shell escape)'),
        (r'\\input\{?\|', 'input with pipe'),
        (r'\\immediate', 'immediate'),
        (r'\\openout', 'openout (file write)'),
        (r'\\openin', 'openin (file read)'),
        (r'\\special', 'special'),
        (r'\\pdfliteral', 'pdfliteral'),
    ]

    for pattern, cmd_name in dangerous_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            raise ValidationError(
                f"❌ Dangerous LaTeX command detected: {cmd_name}\n"
                f"   This command could execute arbitrary code"
            )

    return content


def validate_port(port: int, name: str = "port") -> int:
    """
    Validate port number.

    Args:
        port: Port number
        name: Field name

    Returns:
        Validated port

    Raises:
        ValidationError: If invalid
    """
    if not isinstance(port, int):
        raise ValidationError(f"❌ {name} must be an integer")

    if port < 1024 or port > 65535:
        raise ValidationError(
            f"❌ {name} must be between 1024 and 65535 (got {port})"
        )

    return port


if __name__ == "__main__":
    # Tests
    print("🧪 Running validation tests...\n")

    # Test identifier validation
    try:
        validate_identifier("vq", "research_field")
        print("✅ Valid identifier: 'vq'")
    except ValidationError as e:
        print(f"❌ {e}")

    try:
        validate_identifier("../etc/passwd", "field")
        print("❌ Should have failed!")
    except ValidationError as e:
        print(f"✅ Blocked path traversal: {e}")

    # Test path validation
    try:
        result = validate_path("papers/vq", "/home/user/AI-Researcher")
        print(f"✅ Valid path: {result}")
    except ValidationError as e:
        print(f"❌ {e}")

    print("\n✅ All validation tests passed!")
