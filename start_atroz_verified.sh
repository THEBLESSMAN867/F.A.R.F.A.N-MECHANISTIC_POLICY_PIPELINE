#!/bin/bash
# ============================================================================
# AtroZ Dashboard Verified Start Script
# ============================================================================
# 
# This script performs verification checks before starting the AtroZ dashboard
# server, ensuring all components are properly configured and functional.
#
# Author: AtroZ Deployment Team
# Version: 1.0.0
# ============================================================================

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTHON_CMD=${PYTHON_CMD:-python3}
PORT=${ATROZ_API_PORT:-5000}
HOST=${ATROZ_API_HOST:-0.0.0.0}
DEBUG=${ATROZ_DEBUG:-false}

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# ============================================================================
# Utility Functions
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_header() {
    echo ""
    echo "============================================================================"
    echo "$1"
    echo "============================================================================"
}

# ============================================================================
# Verification Functions
# ============================================================================

check_python_version() {
    log_info "Checking Python version..."
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
        log_error "Python 3.10+ required, found $PYTHON_VERSION"
        return 1
    fi
    
    log_success "Python $PYTHON_VERSION"
    return 0
}

check_dependencies() {
    log_info "Checking Python dependencies..."
    
    REQUIRED_PACKAGES=(
        "flask"
        "flask_cors"
        "flask_socketio"
        "jwt"
        "werkzeug"
    )
    
    MISSING=()
    
    for package in "${REQUIRED_PACKAGES[@]}"; do
        if ! $PYTHON_CMD -c "import $package" 2>/dev/null; then
            MISSING+=("$package")
        fi
    done
    
    if [ ${#MISSING[@]} -gt 0 ]; then
        log_error "Missing dependencies: ${MISSING[*]}"
        log_info "Install with: pip install -r requirements_atroz.txt"
        return 1
    fi
    
    log_success "All required dependencies installed"
    return 0
}

check_directory_structure() {
    log_info "Checking directory structure..."
    
    REQUIRED_DIRS=(
        "src/saaaaaa/api"
        "src/saaaaaa/api/static"
        "src/saaaaaa/api/static/css"
        "src/saaaaaa/api/static/js"
    )
    
    MISSING_DIRS=()
    
    cd "$PROJECT_ROOT"
    
    for dir in "${REQUIRED_DIRS[@]}"; do
        if [ ! -d "$dir" ]; then
            MISSING_DIRS+=("$dir")
        fi
    done
    
    if [ ${#MISSING_DIRS[@]} -gt 0 ]; then
        log_error "Missing directories: ${MISSING_DIRS[*]}"
        return 1
    fi
    
    log_success "Directory structure valid"
    return 0
}

check_critical_files() {
    log_info "Checking critical files..."
    
    REQUIRED_FILES=(
        "src/saaaaaa/api/api_server.py"
        "src/saaaaaa/api/pdet_colombia_data.py"
        "src/saaaaaa/api/auth_admin.py"
        "src/saaaaaa/api/pipeline_connector.py"
        "src/saaaaaa/api/static/index.html"
        "src/saaaaaa/api/static/css/atroz-dashboard.css"
        "src/saaaaaa/api/static/js/atroz-dashboard.js"
    )
    
    MISSING_FILES=()
    
    cd "$PROJECT_ROOT"
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$file" ]; then
            MISSING_FILES+=("$file")
        fi
    done
    
    if [ ${#MISSING_FILES[@]} -gt 0 ]; then
        log_error "Missing files: ${MISSING_FILES[*]}"
        return 1
    fi
    
    log_success "All critical files present"
    return 0
}

test_pdet_data() {
    log_info "Testing PDET Colombia dataset..."
    
    cd "$PROJECT_ROOT"
    
    OUTPUT=$($PYTHON_CMD -c "
from src.saaaaaa.api.pdet_colombia_data import get_statistics
stats = get_statistics()
print(f\"Subregions: {stats['total_subregions']}\")
print(f\"Municipalities: {stats['total_municipalities']}\")
print(f\"Departments: {stats['total_departments']}\")
" 2>&1)
    
    if [ $? -ne 0 ]; then
        log_error "PDET data test failed"
        echo "$OUTPUT"
        return 1
    fi
    
    # Verify expected counts
    if ! echo "$OUTPUT" | grep -q "Subregions: 16"; then
        log_error "Expected 16 subregions"
        return 1
    fi
    
    if ! echo "$OUTPUT" | grep -q "Municipalities: 170"; then
        log_error "Expected 170 municipalities"
        return 1
    fi
    
    log_success "PDET dataset valid (16 subregions, 170 municipalities)"
    return 0
}

test_auth_module() {
    log_info "Testing authentication module..."
    
    cd "$PROJECT_ROOT"
    
    $PYTHON_CMD -c "
from src.saaaaaa.api.auth_admin import auth_manager, validate_password

# Test password validation
valid, error = validate_password('weak')
assert not valid, 'Should reject weak password'

valid, error = validate_password('StrongP@ssw0rd123!')
assert valid, 'Should accept strong password'

# Test auth manager initialization
assert auth_manager.user_store is not None
print('Authentication module OK')
" 2>&1
    
    if [ $? -ne 0 ]; then
        log_error "Authentication module test failed"
        return 1
    fi
    
    log_success "Authentication module functional"
    return 0
}

test_pipeline_connector() {
    log_info "Testing pipeline connector..."
    
    cd "$PROJECT_ROOT"
    
    $PYTHON_CMD -c "
from src.saaaaaa.api.pipeline_connector import pipeline_connector

# Check initialization
assert pipeline_connector.output_dir.exists()
assert pipeline_connector.results_dir.exists()
assert pipeline_connector.manifests_dir.exists()

print('Pipeline connector OK')
" 2>&1
    
    if [ $? -ne 0 ]; then
        log_error "Pipeline connector test failed"
        return 1
    fi
    
    log_success "Pipeline connector initialized"
    return 0
}

check_port_available() {
    log_info "Checking if port $PORT is available..."
    
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        log_error "Port $PORT is already in use"
        log_info "Kill existing process or choose a different port with ATROZ_API_PORT"
        return 1
    fi
    
    log_success "Port $PORT is available"
    return 0
}

create_output_directories() {
    log_info "Creating output directories..."
    
    cd "$PROJECT_ROOT"
    
    mkdir -p output/analysis_results
    mkdir -p output/verification_manifests
    mkdir -p output/uploads
    mkdir -p cache
    
    log_success "Output directories created"
    return 0
}

# ============================================================================
# Main Verification Sequence
# ============================================================================

run_verification() {
    print_header "AtroZ Dashboard - Pre-Flight Verification"
    
    VERIFICATION_STEPS=(
        "check_python_version"
        "check_dependencies"
        "check_directory_structure"
        "check_critical_files"
        "test_pdet_data"
        "test_auth_module"
        "test_pipeline_connector"
        "check_port_available"
        "create_output_directories"
    )
    
    FAILED_STEPS=()
    
    for step in "${VERIFICATION_STEPS[@]}"; do
        if ! $step; then
            FAILED_STEPS+=("$step")
        fi
        echo ""
    done
    
    print_header "Verification Summary"
    
    if [ ${#FAILED_STEPS[@]} -gt 0 ]; then
        log_error "Verification failed! ${#FAILED_STEPS[@]} step(s) failed:"
        for step in "${FAILED_STEPS[@]}"; do
            echo "  - $step"
        done
        echo ""
        log_error "Please fix the issues above before starting the server"
        return 1
    else
        log_success "All verification checks passed!"
        return 0
    fi
}

# ============================================================================
# Server Start
# ============================================================================

start_server() {
    print_header "Starting AtroZ Dashboard Server"
    
    log_info "Configuration:"
    echo "  Host: $HOST"
    echo "  Port: $PORT"
    echo "  Debug: $DEBUG"
    echo "  Python: $($PYTHON_CMD --version)"
    echo ""
    
    cd "$PROJECT_ROOT"
    
    # Set environment variables
    export ATROZ_API_PORT=$PORT
    export ATROZ_API_HOST=$HOST
    export ATROZ_DEBUG=$DEBUG
    export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"
    
    log_info "Starting server..."
    echo ""
    echo "============================================================================"
    echo "                     AtroZ Dashboard Server"
    echo "============================================================================"
    echo ""
    echo "  Dashboard URL: http://localhost:$PORT/"
    echo "  Admin URL:     http://localhost:$PORT/admin/"
    echo "  API Docs:      http://localhost:$PORT/api/v1/"
    echo ""
    echo "  Press Ctrl+C to stop the server"
    echo ""
    echo "============================================================================"
    echo ""
    
    # Start the server
    $PYTHON_CMD -m saaaaaa.api.api_server
}

# ============================================================================
# Main Script
# ============================================================================

main() {
    # Parse arguments
    SKIP_VERIFICATION=false
    SHOW_HELP=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-verification)
                SKIP_VERIFICATION=true
                shift
                ;;
            --help|-h)
                SHOW_HELP=true
                shift
                ;;
            --port)
                PORT="$2"
                shift 2
                ;;
            --debug)
                DEBUG=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                SHOW_HELP=true
                shift
                ;;
        esac
    done
    
    if [ "$SHOW_HELP" = true ]; then
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --skip-verification    Skip pre-flight verification checks"
        echo "  --port PORT            Specify server port (default: 5000)"
        echo "  --debug                Enable debug mode"
        echo "  --help, -h             Show this help message"
        echo ""
        echo "Environment Variables:"
        echo "  ATROZ_API_PORT         Server port (default: 5000)"
        echo "  ATROZ_API_HOST         Server host (default: 0.0.0.0)"
        echo "  ATROZ_DEBUG            Debug mode (default: false)"
        echo "  PYTHON_CMD             Python command (default: python3)"
        echo ""
        exit 0
    fi
    
    # Run verification unless skipped
    if [ "$SKIP_VERIFICATION" = false ]; then
        if ! run_verification; then
            exit 1
        fi
        echo ""
    else
        log_warning "Skipping verification checks"
        echo ""
    fi
    
    # Start server
    start_server
}

# Run main function
main "$@"
