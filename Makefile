.PHONY: all setup clean generate-all help install-graphviz

# Default target
help:
	@echo "OpenShift Architecture Diagrams - Make targets:"
	@echo ""
	@echo "  make setup           - Create venv and install dependencies"
	@echo "  make install-graphviz - Install graphviz system dependency"
	@echo "  make generate-all    - Generate all diagrams"
	@echo "  make clean           - Remove generated diagrams and cache"
	@echo "  make help            - Show this help message"
	@echo ""

# Setup virtual environment and install dependencies
setup:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo ""
	@echo "✓ Setup complete! Activate venv with: source venv/bin/activate"

# Install graphviz system dependency (Fedora/RHEL)
install-graphviz:
	@echo "Installing graphviz..."
	@if command -v dnf >/dev/null 2>&1; then \
		sudo dnf install -y graphviz; \
	elif command -v apt-get >/dev/null 2>&1; then \
		sudo apt-get update && sudo apt-get install -y graphviz; \
	elif command -v brew >/dev/null 2>&1; then \
		brew install graphviz; \
	else \
		echo "Please install graphviz manually for your system"; \
		exit 1; \
	fi
	@echo "✓ Graphviz installed"

# Generate all diagrams
generate-all:
	@echo "Generating all diagrams..."
	@mkdir -p output
	@find diagrams -name "*.py" -type f | while read diagram; do \
		echo "Running $$diagram..."; \
		python3 $$diagram || exit 1; \
	done
	@echo ""
	@echo "✓ All diagrams generated in output/"
	@ls -lh output/

# Clean generated files
clean:
	rm -rf output/*.png output/*.pdf output/*.svg
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned generated diagrams and cache"

# Convenience: Generate all (alias)
all: generate-all
