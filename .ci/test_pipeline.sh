#!/bin/bash
#
# Comprehensive Pipeline Validation Test
# Tests all aspects of the Azure DevOps pipeline configuration
#

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   COMPREHENSIVE AZURE DEVOPS PIPELINE VALIDATION           ║"
echo "╔════════════════════════════════════════════════════════════╗"
echo ""

PIPELINE_FILE="stage/deploy_notebooks_stage_v3.yml"
ERROR_COUNT=0
WARNING_COUNT=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: File exists
echo -e "${BLUE}[TEST 1/8]${NC} Checking if pipeline file exists..."
if [ -f "$PIPELINE_FILE" ]; then
    echo -e "${GREEN}✅ PASS${NC} - Pipeline file found"
else
    echo -e "${RED}❌ FAIL${NC} - Pipeline file not found"
    ERROR_COUNT=$((ERROR_COUNT + 1))
    exit 1
fi

# Test 2: YAML syntax validation
echo ""
echo -e "${BLUE}[TEST 2/8]${NC} Validating YAML syntax..."
if python3 -c "import yaml; yaml.safe_load(open('$PIPELINE_FILE'))" 2>/dev/null; then
    echo -e "${GREEN}✅ PASS${NC} - YAML syntax is valid"
else
    echo -e "${RED}❌ FAIL${NC} - YAML syntax error"
    ERROR_COUNT=$((ERROR_COUNT + 1))
fi

# Test 3: Check for modern agent
echo ""
echo -e "${BLUE}[TEST 3/8]${NC} Checking for modern Ubuntu agent..."
if grep -q "ubuntu-latest" "$PIPELINE_FILE"; then
    echo -e "${GREEN}✅ PASS${NC} - Using modern agent (ubuntu-latest)"
elif grep -q "ubuntu-22.04" "$PIPELINE_FILE"; then
    echo -e "${GREEN}✅ PASS${NC} - Using Ubuntu 22.04"
else
    echo -e "${YELLOW}⚠️  WARN${NC} - Not using modern Ubuntu agent"
    WARNING_COUNT=$((WARNING_COUNT + 1))
fi

# Test 4: Check template references exist
echo ""
echo -e "${BLUE}[TEST 4/8]${NC} Checking template file references..."
if [ -f "steps/deploy_notebook_steps_v2.yml" ]; then
    echo -e "${GREEN}✅ PASS${NC} - Template file exists: deploy_notebook_steps_v2.yml"
else
    echo -e "${RED}❌ FAIL${NC} - Template file missing"
    ERROR_COUNT=$((ERROR_COUNT + 1))
fi

# Test 5: Check for security placeholders
echo ""
echo -e "${BLUE}[TEST 5/8]${NC} Checking for security placeholders..."
if grep -q '"x"' "$PIPELINE_FILE"; then
    echo -e "${GREEN}✅ PASS${NC} - Using placeholders for sensitive data"
else
    echo -e "${YELLOW}⚠️  WARN${NC} - Check for hard-coded credentials"
    WARNING_COUNT=$((WARNING_COUNT + 1))
fi

# Test 6: Check for Azure DevOps expressions
echo ""
echo -e "${BLUE}[TEST 6/8]${NC} Checking for Azure DevOps expressions..."
EXPR_COUNT=$(grep -o '\${{' "$PIPELINE_FILE" | wc -l | tr -d ' ')
if [ "$EXPR_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Found $EXPR_COUNT compile-time expressions"
else
    echo -e "${YELLOW}⚠️  WARN${NC} - No compile-time expressions found"
    WARNING_COUNT=$((WARNING_COUNT + 1))
fi

# Test 7: Check file structure
echo ""
echo -e "${BLUE}[TEST 7/8]${NC} Validating pipeline structure..."
HAS_PARAMETERS=$(grep -c "^parameters:" "$PIPELINE_FILE" || true)
HAS_STAGES=$(grep -c "^stages:" "$PIPELINE_FILE" || true)

if [ "$HAS_PARAMETERS" -gt 0 ] && [ "$HAS_STAGES" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Pipeline has required sections (parameters, stages)"
else
    echo -e "${RED}❌ FAIL${NC} - Missing required sections"
    ERROR_COUNT=$((ERROR_COUNT + 1))
fi

# Test 8: Check documentation
echo ""
echo -e "${BLUE}[TEST 8/8]${NC} Checking for inline documentation..."
COMMENT_COUNT=$(grep -c "^  #" "$PIPELINE_FILE" || true)
if [ "$COMMENT_COUNT" -gt 20 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Well documented ($COMMENT_COUNT comment lines)"
else
    echo -e "${YELLOW}⚠️  WARN${NC} - Limited documentation"
    WARNING_COUNT=$((WARNING_COUNT + 1))
fi

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    VALIDATION SUMMARY                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# File statistics
FILE_SIZE=$(wc -c < "$PIPELINE_FILE" | tr -d ' ')
LINE_COUNT=$(wc -l < "$PIPELINE_FILE" | tr -d ' ')

echo "📄 File Statistics:"
echo "   • Size: $FILE_SIZE bytes"
echo "   • Lines: $LINE_COUNT"
echo ""

echo "🧪 Test Results:"
echo "   • Total Tests: 8"
echo -e "   • ${GREEN}Passed: $((8 - ERROR_COUNT - WARNING_COUNT))${NC}"
echo -e "   • ${YELLOW}Warnings: $WARNING_COUNT${NC}"
echo -e "   • ${RED}Failures: $ERROR_COUNT${NC}"
echo ""

# Final verdict
if [ "$ERROR_COUNT" -eq 0 ]; then
    echo "╔════════════════════════════════════════════════════════════╗"
    echo -e "║         ${GREEN}✅ ALL CRITICAL TESTS PASSED!${NC}                    ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 Your pipeline is ready for Azure DevOps!"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. git add .ci/stage/deploy_notebooks_stage_v3.yml"
    echo "   2. git commit -m 'Updated pipeline with modern improvements'"
    echo "   3. git push origin main"
    echo "   4. Trigger pipeline in Azure DevOps"
    echo ""
    exit 0
else
    echo "╔════════════════════════════════════════════════════════════╗"
    echo -e "║         ${RED}❌ VALIDATION FAILED${NC}                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Please fix the errors above before deploying to Azure DevOps."
    echo ""
    exit 1
fi
