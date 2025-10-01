#!/usr/bin/env bash
# ===================================
# MEGA Project Health Check Script
# ===================================
# Validates project structure, configuration, and dependencies

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0

# Check function
check() {
    local description="$1"
    local command="$2"
    local level="${3:-error}"  # error or warning
    
    echo -n "Checking $description... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
        ((CHECKS_PASSED++))
        return 0
    else
        if [ "$level" = "warning" ]; then
            echo -e "${YELLOW}⚠${NC}"
            ((CHECKS_WARNING++))
        else
            echo -e "${RED}✗${NC}"
            ((CHECKS_FAILED++))
        fi
        return 1
    fi
}

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}MEGA Project Health Check${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# ===================================
# 1. Environment Checks
# ===================================
echo -e "${BLUE}1. Environment${NC}"
check "Python version (>=3.11)" "python3 --version | grep -E 'Python 3\.(1[1-9]|[2-9][0-9])'"
check "pip installed" "command -v pip"
check "git installed" "command -v git"
check "pytest installed" "command -v pytest" "warning"
check "ruff installed" "command -v ruff" "warning"
check "black installed" "command -v black" "warning"
echo ""

# ===================================
# 2. File Structure
# ===================================
echo -e "${BLUE}2. File Structure${NC}"
check ".gitignore exists" "test -f .gitignore"
check "README.md exists" "test -f README.md"
check "SECURITY.md exists" "test -f SECURITY.md"
check "CONTRIBUTING.md exists" "test -f CONTRIBUTING.md"
check "CHANGELOG.md exists" "test -f CHANGELOG.md"
check "Makefile exists" "test -f Makefile"
check "pytest.ini exists" "test -f pytest.ini"
check "pyproject.toml exists" "test -f pyproject.toml"
echo ""

# ===================================
# 3. GitHub Workflows
# ===================================
echo -e "${BLUE}3. GitHub Workflows${NC}"
check "workflows directory exists" "test -d .github/workflows"
check "CI workflow exists" "test -f .github/workflows/ci.yml"
check "CodeQL workflow exists" "test -f .github/workflows/codeql.yml"
check "Secrets workflow exists" "test -f .github/workflows/secrets.yml"
check "Dependabot config exists" "test -f .github/dependabot.yml"
check "PR template exists" "test -f .github/PULL_REQUEST_TEMPLATE.md"
check "Issue templates exist" "test -d .github/ISSUE_TEMPLATE"
echo ""

# ===================================
# 4. Package Structure
# ===================================
echo -e "${BLUE}4. Package Structure${NC}"
check "packages directory exists" "test -d packages"
check "common-utils package" "test -d packages/common-utils"
check "adaptive-engine package" "test -d packages/adaptive-engine"
check "case-generator package" "test -d packages/case-generator"
check "multi-agent package" "test -d packages/multi-agent"
check "cli package" "test -d packages/cli"

# Check all packages have pyproject.toml with build-system
for pkg in packages/*/; do
    pkg_name=$(basename "$pkg")
    check "$pkg_name has pyproject.toml" "test -f $pkg/pyproject.toml"
    if [ -f "$pkg/pyproject.toml" ]; then
        check "$pkg_name build-system configured" "grep -q '\[build-system\]' $pkg/pyproject.toml"
    fi
done
echo ""

# ===================================
# 5. Configuration Files
# ===================================
echo -e "${BLUE}5. Configuration Files${NC}"
check "mega.config.yaml exists" "test -f mega.config.yaml"
check "requirements-dev.txt exists" "test -f requirements-dev.txt"
check ".env.example exists" "test -f .env.example" "warning"
check "pre-commit config exists" "test -f .pre-commit-config.yaml"
echo ""

# ===================================
# 6. Documentation
# ===================================
echo -e "${BLUE}6. Documentation${NC}"
check "docs directory exists" "test -d docs"
check "architecture.md exists" "test -f docs/architecture.md"
check "security.md exists" "test -f docs/security.md"
check "implementation.md exists" "test -f docs/implementation.md"
check "roadmap.md exists" "test -f docs/roadmap.md"
echo ""

# ===================================
# 7. YAML Validation
# ===================================
if command -v python3 > /dev/null 2>&1; then
    echo -e "${BLUE}7. YAML Validation${NC}"
    
    # Check if PyYAML is available
    if python3 -c "import yaml" 2>/dev/null; then
        for yaml_file in .github/workflows/*.yml .github/*.yml mega.config.yaml; do
            if [ -f "$yaml_file" ]; then
                file_name=$(basename "$yaml_file")
                check "$file_name is valid YAML" "python3 -c \"import yaml; yaml.safe_load(open('$yaml_file'))\""
            fi
        done
    else
        echo -e "${YELLOW}PyYAML not installed - skipping YAML validation${NC}"
        ((CHECKS_WARNING++))
    fi
    echo ""
fi

# ===================================
# 8. Git Status
# ===================================
echo -e "${BLUE}8. Git Status${NC}"
check "git repository initialized" "test -d .git"
check "current branch" "git branch --show-current"
if git branch --show-current > /dev/null 2>&1; then
    current_branch=$(git branch --show-current)
    echo "  Current branch: ${GREEN}$current_branch${NC}"
fi
echo ""

# ===================================
# Summary
# ===================================
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "Passed:   ${GREEN}$CHECKS_PASSED${NC}"
echo -e "Failed:   ${RED}$CHECKS_FAILED${NC}"
echo -e "Warnings: ${YELLOW}$CHECKS_WARNING${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All critical checks passed!${NC}"
    echo ""
    echo "Recommendations:"
    [ $CHECKS_WARNING -gt 0 ] && echo "- Address warnings for optimal setup"
    echo "- Run 'make install' to install dependencies"
    echo "- Run 'make all' to verify code quality"
    echo "- Run 'make pre-commit' to install git hooks"
    exit 0
else
    echo -e "${RED}✗ Some critical checks failed${NC}"
    echo ""
    echo "Please fix the failed checks before proceeding."
    echo "See CONTRIBUTING.md for setup instructions."
    exit 1
fi
