# List of subdirectories
SUBDIRS = $(shell find . -maxdepth 1 -type d -not -name '.*')

# Invoke make test for all children directories
test:
	@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir test; \
	done

.PHONY: test
