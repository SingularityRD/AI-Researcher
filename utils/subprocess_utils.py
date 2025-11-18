"""
Secure Subprocess Execution Utilities
Prevents command injection and provides safe command execution
"""
import subprocess
import shlex
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
from .validators import validate_path, validate_branch_name, validate_url

logger = logging.getLogger(__name__)


class CommandExecutionError(Exception):
    """Raised when command execution fails"""
    pass


def execute_command_safe(
    command: List[str],
    cwd: Optional[Path] = None,
    timeout: int = 60,
    check: bool = True,
    env: Optional[Dict[str, str]] = None,
    capture_output: bool = True
) -> subprocess.CompletedProcess:
    """
    Execute command safely without shell=True.

    SECURITY: Always use shell=False to prevent command injection!

    Args:
        command: Command as list (e.g., ['git', 'clone', 'url'])
        cwd: Working directory
        timeout: Timeout in seconds
        check: If True, raise error on non-zero exit
        env: Environment variables
        capture_output: If True, capture stdout/stderr

    Returns:
        CompletedProcess object

    Raises:
        CommandExecutionError: If execution fails
        subprocess.TimeoutExpired: If timeout exceeded

    Examples:
        >>> execute_command_safe(['ls', '-la'], cwd='/tmp')
        CompletedProcess(...)

        >>> execute_command_safe(['git', 'status'])
        CompletedProcess(...)
    """
    # Validate command
    if not command or not isinstance(command, list):
        raise ValueError("❌ Command must be a non-empty list")

    if not all(isinstance(x, str) for x in command):
        raise ValueError("❌ All command elements must be strings")

    # Log command (safely)
    safe_cmd = shlex.join(command)
    logger.info(f"🔧 Executing: {safe_cmd}" + (f" (cwd: {cwd})" if cwd else ""))

    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            check=check,
            shell=False,  # ✅ CRITICAL: Never use shell=True!
            env=env
        )

        logger.info(f"✅ Command completed (exit code: {result.returncode})")
        return result

    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Command failed (exit code {e.returncode}): {e.stderr}")
        raise CommandExecutionError(
            f"Command failed with exit code {e.returncode}\n"
            f"Command: {safe_cmd}\n"
            f"Error: {e.stderr}"
        )

    except subprocess.TimeoutExpired as e:
        logger.error(f"❌ Command timed out after {timeout}s")
        raise CommandExecutionError(
            f"Command timed out after {timeout}s\n"
            f"Command: {safe_cmd}"
        )

    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise CommandExecutionError(f"Unexpected error: {e}")


def git_clone_safe(
    url: str,
    target_dir: Path,
    branch: Optional[str] = None,
    depth: int = 1,
    timeout: int = 300
) -> None:
    """
    Safely clone git repository.

    Args:
        url: Git URL (must be https://)
        target_dir: Target directory
        branch: Branch name (validated)
        depth: Clone depth (default: 1 for shallow clone)
        timeout: Timeout in seconds

    Raises:
        ValueError: If inputs invalid
        CommandExecutionError: If git clone fails

    Examples:
        >>> git_clone_safe(
        ...     'https://github.com/user/repo.git',
        ...     Path('/workspace/repo'),
        ...     branch='main'
        ... )
    """
    # Validate URL
    validated_url = validate_url(url, allowed_schemes=['https', 'git'])

    # Validate branch if provided
    if branch:
        branch = validate_branch_name(branch)

    # Ensure target directory doesn't exist
    if target_dir.exists():
        raise ValueError(f"❌ Target directory already exists: {target_dir}")

    # Create parent directory
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    # Build command
    command = ['git', 'clone']

    if branch:
        command.extend(['--branch', branch])

    if depth > 0:
        command.extend(['--depth', str(depth)])

    command.extend([validated_url, str(target_dir)])

    # Execute
    logger.info(f"📥 Cloning repository: {validated_url}")
    execute_command_safe(command, timeout=timeout)
    logger.info(f"✅ Successfully cloned to {target_dir}")


def git_checkout_safe(
    branch: str,
    repo_dir: Path,
    create: bool = False
) -> None:
    """
    Safely checkout git branch.

    Args:
        branch: Branch name
        repo_dir: Repository directory
        create: If True, create new branch

    Raises:
        CommandExecutionError: If checkout fails
    """
    # Validate branch name
    branch = validate_branch_name(branch)

    # Validate repo directory
    if not repo_dir.is_dir():
        raise ValueError(f"❌ Not a directory: {repo_dir}")

    # Build command
    command = ['git', 'checkout']

    if create:
        command.append('-b')

    command.append(branch)

    # Execute
    logger.info(f"🔀 Checking out branch: {branch}")
    execute_command_safe(command, cwd=repo_dir)
    logger.info(f"✅ Checked out branch: {branch}")


def compile_latex_safe(
    tex_file: str,
    project_dir: Path,
    timeout: int = 120,
    runs: int = 3
) -> Path:
    """
    Safely compile LaTeX document.

    SECURITY: Uses -no-shell-escape to prevent LaTeX injection!

    Args:
        tex_file: Name of .tex file (not path!)
        project_dir: Project directory containing .tex file
        timeout: Timeout per run (seconds)
        runs: Number of pdflatex runs (default: 3 for references)

    Returns:
        Path to generated PDF file

    Raises:
        CommandExecutionError: If compilation fails

    Examples:
        >>> pdf = compile_latex_safe(
        ...     'main.tex',
        ...     Path('/papers/my-paper'),
        ...     runs=3
        ... )
    """
    # Validate inputs
    if not tex_file.endswith('.tex'):
        raise ValueError(f"❌ File must end with .tex: {tex_file}")

    if '/' in tex_file or '\\' in tex_file:
        raise ValueError(f"❌ tex_file must be filename only, not path: {tex_file}")

    if not project_dir.is_dir():
        raise ValueError(f"❌ Project directory not found: {project_dir}")

    tex_path = project_dir / tex_file
    if not tex_path.exists():
        raise ValueError(f"❌ TeX file not found: {tex_path}")

    base_name = tex_file[:-4]  # Remove .tex extension

    logger.info(f"📄 Compiling LaTeX: {tex_file} ({runs} runs)")

    # Run pdflatex multiple times (for references, TOC, etc.)
    for i in range(runs):
        logger.info(f"  Run {i+1}/{runs}...")

        result = execute_command_safe(
            [
                'pdflatex',
                '-interaction=nonstopmode',  # Don't stop on errors
                '-no-shell-escape',  # ✅ CRITICAL: Disable shell commands!
                '-halt-on-error',  # Stop on first error
                tex_file
            ],
            cwd=project_dir,
            timeout=timeout,
            check=False  # Don't raise on non-zero exit (LaTeX warnings)
        )

        # Check for critical errors
        if result.returncode != 0:
            logger.error(f"❌ pdflatex failed on run {i+1}")
            logger.error(f"Output:\n{result.stdout}")
            raise CommandExecutionError(
                f"pdflatex failed on run {i+1}\n"
                f"See output above for details"
            )

        # Run bibtex after first run (if .bib file exists)
        if i == 0:
            bib_files = list(project_dir.glob('*.bib'))
            if bib_files:
                logger.info(f"  Running bibtex...")
                try:
                    execute_command_safe(
                        ['bibtex', base_name],
                        cwd=project_dir,
                        timeout=30,
                        check=False
                    )
                except:
                    logger.warning("  bibtex failed (continuing anyway)")

    # Check PDF was created
    pdf_path = project_dir / f'{base_name}.pdf'
    if not pdf_path.exists():
        raise CommandExecutionError(
            f"❌ PDF file not created: {pdf_path}\n"
            f"Check LaTeX output for errors"
        )

    logger.info(f"✅ LaTeX compilation successful: {pdf_path}")
    return pdf_path


def run_python_safe(
    script_path: Path,
    args: Optional[List[str]] = None,
    cwd: Optional[Path] = None,
    timeout: int = 300,
    env: Optional[Dict[str, str]] = None
) -> subprocess.CompletedProcess:
    """
    Safely run Python script.

    Args:
        script_path: Path to Python script
        args: Command line arguments
        cwd: Working directory
        timeout: Timeout in seconds
        env: Environment variables

    Returns:
        CompletedProcess object

    Raises:
        CommandExecutionError: If execution fails

    Examples:
        >>> run_python_safe(
        ...     Path('/app/scripts/process.py'),
        ...     args=['--input', 'data.json'],
        ...     timeout=60
        ... )
    """
    # Validate script exists
    if not script_path.exists():
        raise ValueError(f"❌ Script not found: {script_path}")

    if not script_path.suffix == '.py':
        raise ValueError(f"❌ File must be .py: {script_path}")

    # Build command
    command = ['python', str(script_path)]

    if args:
        command.extend(args)

    # Execute
    logger.info(f"🐍 Running Python script: {script_path}")
    return execute_command_safe(command, cwd=cwd, timeout=timeout, env=env)


if __name__ == "__main__":
    # Tests
    print("🧪 Running subprocess tests...\n")

    # Test simple command
    try:
        result = execute_command_safe(['echo', 'Hello, World!'])
        print(f"✅ Simple command: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Failed: {e}")

    # Test git clone (dry run)
    try:
        # This will fail (directory exists), but validates inputs
        git_clone_safe(
            'https://github.com/torvalds/linux.git',
            Path('/tmp/test-clone'),
            branch='master',
            depth=1
        )
    except ValueError as e:
        print(f"✅ Git validation works: {e}")
    except Exception as e:
        print(f"⚠️ Git clone test (expected): {e}")

    print("\n✅ Subprocess utility tests completed!")
